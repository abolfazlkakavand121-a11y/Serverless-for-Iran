#!/usr/bin/env python3
"""Validate the canonical method-blueprint catalog using only Python's stdlib."""
import json
import sys
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / "Subscription" / "Method-Blueprints-v1.json"

def main() -> int:
    try:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot load catalog: {exc}", file=sys.stderr)
        return 1

    errors = []
    if data.get("format") != "serverless-method-blueprints":
        errors.append("unexpected format identifier")
    if data.get("format_version") != 1:
        errors.append("unsupported format_version")
    methods = data.get("methods")
    if not isinstance(methods, list) or not methods:
        errors.append("methods must be a non-empty array")
        methods = []

    ids = []
    for index, method in enumerate(methods):
        where = f"methods[{index}]"
        if not isinstance(method, dict):
            errors.append(f"{where} must be an object")
            continue
        for key in ("id", "name", "family", "status", "runtime", "requirements"):
            if key not in method:
                errors.append(f"{where} missing {key}")
        method_id = method.get("id")
        if isinstance(method_id, str):
            ids.append(method_id)
        runtime = method.get("runtime")
        if not isinstance(runtime, dict):
            errors.append(f"{where}.runtime must be an object")
        else:
            for key in ("component", "config_type", "config"):
                if key not in runtime:
                    errors.append(f"{where}.runtime missing {key}")
            if not isinstance(runtime.get("config"), dict):
                errors.append(f"{where}.runtime.config must be an object")
        requirements = method.get("requirements")
        if not isinstance(requirements, dict) or not isinstance(requirements.get("client"), list) or not isinstance(requirements.get("server"), list):
            errors.append(f"{where}.requirements must contain client[] and server[]")

    if len(ids) != len(set(ids)):
        errors.append("method IDs must be unique")
    if "BASE-OOB-001" not in ids:
        errors.append("known-good OOB control reference is missing")
    contract = data.get("validation_contract")
    for key in ("levels", "must_not_promote_on", "required_tests", "report_fields"):
        if not isinstance(contract, dict) or not isinstance(contract.get(key), list) or not contract[key]:
            errors.append(f"validation_contract.{key} must be a non-empty array")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(methods)} method entries; {len(ids)} unique IDs; blueprint catalog structure valid.")
    print("NOTE: this validates the blueprint format only, not Xray importability or network effectiveness.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
