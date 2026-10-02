from __future__ import annotations

from typing import Dict, List


class ValidationStatus:
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"
    NOT_VERIFIED = "NOT VERIFIED"


def validate_inputs(required_fields: List[str], input_map: Dict[str, object]) -> dict:
    missing = [field for field in required_fields if field not in input_map or input_map[field] is None]
    if missing:
        return {"status": ValidationStatus.FAIL, "missing": missing}
    return {"status": ValidationStatus.PASS, "missing": []}
