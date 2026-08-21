use serde_json::Value;
use std::io::{self, BufRead, Write};

fn hex(bytes: &[u8]) -> String {
    bytes.iter().map(|byte| format!("{byte:02x}")).collect()
}

fn main() {
    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut output = io::BufWriter::new(stdout.lock());
    for line in stdin.lock().lines() {
        let line = match line {
            Ok(value) => value,
            Err(error) => {
                let _ = writeln!(output, "{{\"ok\":false,\"code\":\"E_INPUT\",\"message\":{}}}", serde_json::to_string(&error.to_string()).unwrap());
                continue;
            }
        };
        let request: Value = match serde_json::from_str(&line) {
            Ok(value) => value,
            Err(error) => {
                let _ = writeln!(output, "{{\"ok\":false,\"code\":\"E_INPUT\",\"message\":{}}}", serde_json::to_string(&error.to_string()).unwrap());
                continue;
            }
        };
        let value = request.get("value").unwrap_or(&Value::Null);
        match sov_contract_parity::canonicalize(value) {
            Ok(bytes) => {
                let id = sov_contract_parity::derive_id(value).unwrap();
                let response = serde_json::json!({"ok": true, "canonical_hex": hex(&bytes), "id": id});
                writeln!(output, "{}", response).unwrap();
                output.flush().unwrap();
            }
            Err(error) => {
                let response = serde_json::json!({"ok": false, "code": error.code, "message": error.message});
                writeln!(output, "{}", response).unwrap();
                output.flush().unwrap();
            }
        }
    }
}
