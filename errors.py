"""Typed failures defined by the Core Contract v0.1."""

from __future__ import annotations


class CoreContractError(ValueError):
    """A deterministic request or contract violation."""

    def __init__(self, code: str, message: str, *, path: str = "") -> None:
        self.code = code
        self.path = path
        detail = f"{code}: {message}"
        if path:
            detail = f"{detail} at {path}"
        super().__init__(detail)


class SchemaValidationError(CoreContractError):
    """JSON Schema validation failed before semantic evaluation."""

    def __init__(self, message: str, *, path: str = "") -> None:
        super().__init__("E_SCHEMA_INVALID", message, path=path)
