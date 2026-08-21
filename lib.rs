//! Focused Core Contract v0.1 parity implementation.
//!
//! This crate intentionally provides only deterministic canonicalization,
//! content IDs, and the small invariant subset shared with the Python
//! reference vectors. It does not import the broader Sovereign Engine runtime.

use serde_json::{Map, Value};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, HashMap};

pub const MAX_SAFE_JSON_INTEGER: i64 = 9_007_199_254_740_991;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ContractError {
    pub code: &'static str,
    pub message: String,
}

impl ContractError {
    fn new(code: &'static str, message: impl Into<String>) -> Self {
        Self { code, message: message.into() }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Evaluation {
    pub status: String,
    pub reason_codes: Vec<String>,
}

fn json_string(value: &str) -> Result<String, ContractError> {
    serde_json::to_string(value).map_err(|error| ContractError::new("E_CANONICALIZATION", error.to_string()))
}

fn utf16_key(value: &str) -> Vec<u16> {
    value.encode_utf16().collect()
}

fn serialize_object(object: &Map<String, Value>) -> Result<String, ContractError> {
    let mut keys: Vec<&String> = object.keys().collect();
    keys.sort_by_key(|key| utf16_key(key));
    let mut fields = Vec::with_capacity(keys.len());
    for key in keys {
        fields.push(format!("{}:{}", json_string(key)?, serialize(&object[key])?));
    }
    Ok(format!("{{{}}}", fields.join(",")))
}

fn serialize(value: &Value) -> Result<String, ContractError> {
    match value {
        Value::Null => Ok("null".to_owned()),
        Value::Bool(true) => Ok("true".to_owned()),
        Value::Bool(false) => Ok("false".to_owned()),
        Value::String(string) => json_string(string),
        Value::Array(values) => values
            .iter()
            .map(serialize)
            .collect::<Result<Vec<_>, _>>()
            .map(|items| format!("[{}]", items.join(","))),
        Value::Object(object) => serialize_object(object),
        Value::Number(number) => {
            if let Some(integer) = number.as_i64() {
                if integer.abs() > MAX_SAFE_JSON_INTEGER {
                    return Err(ContractError::new("E_CANONICALIZATION", "raw JSON integer exceeds the safe range"));
                }
                Ok(integer.to_string())
            } else if let Some(integer) = number.as_u64() {
                if integer > MAX_SAFE_JSON_INTEGER as u64 {
                    return Err(ContractError::new("E_CANONICALIZATION", "raw JSON integer exceeds the safe range"));
                }
                Ok(integer.to_string())
            } else {
                Err(ContractError::new("E_CANONICALIZATION", "raw floating-point JSON numbers are forbidden"))
            }
        }
    }
}

pub fn canonicalize(value: &Value) -> Result<Vec<u8>, ContractError> {
    Ok(serialize(value)?.into_bytes())
}

pub fn derive_id(canonical_body: &Value) -> Result<String, ContractError> {
    let digest = Sha256::digest(canonicalize(canonical_body)?);
    Ok(format!("sov:sha256:{digest:x}"))
}

fn body<'a>(record: &'a Value) -> Result<&'a Value, ContractError> {
    record.get("canonical_body").ok_or_else(|| ContractError::new("E_SCHEMA_INVALID", "record lacks canonical_body"))
}

fn string_at<'a>(value: &'a Value, path: &[&str]) -> Result<&'a str, ContractError> {
    let mut current = value;
    for key in path {
        current = current.get(*key).ok_or_else(|| ContractError::new("E_SCHEMA_INVALID", format!("missing {}", path.join("."))))?;
    }
    current.as_str().ok_or_else(|| ContractError::new("E_SCHEMA_INVALID", format!("{} is not a string", path.join("."))))
}

fn object_kind(record: &Value) -> Result<&str, ContractError> {
    string_at(body(record)?, &["object_kind"])
}

fn lookup<'a>(records: &'a HashMap<String, Value>, object_id: &str) -> Result<&'a Value, ContractError> {
    records.get(object_id).ok_or_else(|| ContractError::new("E_REFERENCE_MISSING", format!("unknown object {object_id}")))
}

fn scalar_i64(value: &Value) -> Result<i64, ContractError> {
    let kind = string_at(value, &["kind"])?;
    match kind {
        "integer" => string_at(value, &["value"])?.parse::<i64>().map_err(|_| ContractError::new("E_SCALAR_UNSUPPORTED", "invalid integer scalar")),
        _ => Err(ContractError::new("E_SCALAR_UNSUPPORTED", "parity harness supports integer sparse components only")),
    }
}

fn sparse_components(record: &Value) -> Result<BTreeMap<Vec<usize>, i64>, ContractError> {
    let components = body(record)?.get("content").and_then(|value| value.get("components")).ok_or_else(|| ContractError::new("E_SCHEMA_INVALID", "components missing"))?;
    if string_at(components, &["mode"])? != "sparse_exact" {
        return Err(ContractError::new("E_SCALAR_UNSUPPORTED", "predicate requires sparse_exact components"));
    }
    let entries = components.get("components").and_then(Value::as_array).ok_or_else(|| ContractError::new("E_SCHEMA_INVALID", "component entries missing"))?;
    let mut result = BTreeMap::new();
    for entry in entries {
        let indices = entry.get("indices").and_then(Value::as_array).ok_or_else(|| ContractError::new("E_INDEX_INVALID", "indices missing"))?
            .iter().map(|index| index.as_u64().ok_or_else(|| ContractError::new("E_INDEX_INVALID", "non-integer index")).map(|value| value as usize))
            .collect::<Result<Vec<_>, _>>()?;
        let value = scalar_i64(entry.get("value").ok_or_else(|| ContractError::new("E_SCHEMA_INVALID", "component value missing"))?)?;
        result.insert(indices, value);
    }
    Ok(result)
}

fn evaluate_metric_inverse(input_ids: &[String], records: &HashMap<String, Value>) -> Result<Evaluation, ContractError> {
    if input_ids.len() != 2 { return Ok(Evaluation { status: "unverifiable".into(), reason_codes: vec!["E_SCHEMA_INVALID".into()] }); }
    let metric = lookup(records, &input_ids[0])?;
    let inverse = lookup(records, &input_ids[1])?;
    if object_kind(metric)? != "metric" || !matches!(object_kind(inverse)?, "metric" | "tensor") {
        return Ok(Evaluation { status: "unverifiable".into(), reason_codes: vec!["E_REFERENCE_KIND".into()] });
    }
    let manifold_id = string_at(body(metric)?, &["content", "manifold_id"])?;
    if manifold_id != string_at(body(inverse)?, &["content", "manifold_id"])? {
        return Ok(Evaluation { status: "unverifiable".into(), reason_codes: vec!["E_DIMENSION_MISMATCH".into()] });
    }
    let manifold = lookup(records, manifold_id)?;
    let dimension = body(manifold)?.get("content").and_then(|value| value.get("dimension")).and_then(Value::as_u64)
        .ok_or_else(|| ContractError::new("E_SCHEMA_INVALID", "manifold dimension missing"))? as usize;
    let left = sparse_components(metric)?;
    let right = sparse_components(inverse)?;
    for row in 0..dimension {
        for column in 0..dimension {
            let product: i64 = (0..dimension).map(|index| left.get(&vec![row, index]).unwrap_or(&0) * right.get(&vec![index, column]).unwrap_or(&0)).sum();
            if product != if row == column { 1 } else { 0 } {
                return Ok(Evaluation { status: "fail".into(), reason_codes: vec!["E_PREDICATE_FAILED".into()] });
            }
        }
    }
    Ok(Evaluation { status: "verified".into(), reason_codes: vec!["VERIFIED".into()] })
}

fn evaluate_tensor_symmetry(input_ids: &[String], records: &HashMap<String, Value>) -> Result<Evaluation, ContractError> {
    if input_ids.len() != 1 { return Ok(Evaluation { status: "unverifiable".into(), reason_codes: vec!["E_SCHEMA_INVALID".into()] }); }
    let tensor = lookup(records, &input_ids[0])?;
    if object_kind(tensor)? != "tensor" { return Ok(Evaluation { status: "unverifiable".into(), reason_codes: vec!["E_REFERENCE_KIND".into()] }); }
    let content = body(tensor)?.get("content").ok_or_else(|| ContractError::new("E_SCHEMA_INVALID", "tensor content missing"))?;
    let symmetries = content.get("symmetries").and_then(Value::as_array).ok_or_else(|| ContractError::new("E_SCHEMA_INVALID", "symmetries missing"))?;
    if symmetries.is_empty() { return Ok(Evaluation { status: "unverifiable".into(), reason_codes: vec!["E_ASSUMPTION_MISSING".into()] }); }
    let components = sparse_components(tensor)?;
    for symmetry in symmetries {
        let kind = string_at(symmetry, &["kind"])?;
        let slots = symmetry.get("slots").and_then(Value::as_array).ok_or_else(|| ContractError::new("E_SCHEMA_INVALID", "symmetry slots missing"))?;
        if slots.len() != 2 { return Ok(Evaluation { status: "unverifiable".into(), reason_codes: vec!["E_FEATURE_DEFERRED".into()] }); }
        let left_slot = slots[0].as_u64().ok_or_else(|| ContractError::new("E_INDEX_INVALID", "slot not integer"))? as usize;
        let right_slot = slots[1].as_u64().ok_or_else(|| ContractError::new("E_INDEX_INVALID", "slot not integer"))? as usize;
        for (indices, observed) in &components {
            let mut swapped = indices.clone();
            swapped.swap(left_slot, right_slot);
            let peer = *components.get(&swapped).unwrap_or(&0);
            let expected = if kind == "symmetric" { peer } else { -peer };
            if *observed != expected { return Ok(Evaluation { status: "fail".into(), reason_codes: vec!["E_PREDICATE_FAILED".into()] }); }
        }
    }
    Ok(Evaluation { status: "verified".into(), reason_codes: vec!["VERIFIED".into()] })
}

pub fn evaluate(operation_id: &str, input_ids: &[String], records: &HashMap<String, Value>) -> Result<Evaluation, ContractError> {
    match operation_id {
        "metric.inverse.v1" => evaluate_metric_inverse(input_ids, records),
        "tensor.symmetry.v1" => evaluate_tensor_symmetry(input_ids, records),
        _ => Ok(Evaluation { status: "unverifiable".into(), reason_codes: vec!["E_OPERATION_UNKNOWN".into()] }),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn canonical_hash_matches_reference_vector() {
        let value: Value = serde_json::from_str(r#"{"b":1,"a":2}"#).unwrap();
        assert_eq!(canonicalize(&value).unwrap(), b"{\"a\":2,\"b\":1}");
        assert_eq!(derive_id(&value).unwrap(), "sov:sha256:d3626ac30a87e6f7a6428233b3c68299976865fa5508e4267c5415c76af7a772");
    }

    #[test]
    fn cross_language_vectors_match_python_reference() {
        let document: Value = serde_json::from_str(include_str!("../../../tests/core_contract/data/cross_language_invariant_vectors.json")).unwrap();
        let mut records = HashMap::new();
        for record in document["records"].as_array().unwrap() {
            let derived = derive_id(&record["canonical_body"]).unwrap();
            assert_eq!(record["id"].as_str().unwrap(), derived);
            records.insert(derived, record.clone());
        }
        for scenario in document["scenarios"].as_array().unwrap() {
            let operation_id = scenario["operation_id"].as_str().unwrap();
            let input_ids = scenario["input_ids"].as_array().unwrap().iter().map(|value| value.as_str().unwrap().to_owned()).collect::<Vec<_>>();
            let result = evaluate(operation_id, &input_ids, &records).unwrap();
            assert_eq!(result.status, scenario["expected"]["status"].as_str().unwrap(), "scenario {}", scenario["name"].as_str().unwrap());
            let expected_codes = scenario["expected"]["reason_codes"].as_array().unwrap().iter().map(|value| value.as_str().unwrap().to_owned()).collect::<Vec<_>>();
            assert_eq!(result.reason_codes, expected_codes, "scenario {}", scenario["name"].as_str().unwrap());
        }
    }
}
