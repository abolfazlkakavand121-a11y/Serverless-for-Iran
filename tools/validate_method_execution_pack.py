#!/usr/bin/env python3
"""Validate method execution pack structure using only Python stdlib."""
import json
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1] / "Subscription" / "Method-Execution-Pack-v1.json"
EXPECTED = {
    "TLS-REC-001", "TLS-REC-002", "TLS-REC-003", "TLS-REC-004",
    "TLS-CH-005", "TLS-CH-006", "TLS-HS-007", "TLS-HS-008",
    "TLS-TR-009", "HTTP-TR-010", "HTTP-TR-011", "TCP-TUN-012",
    "FRONT-013", "QUIC-014", "REFRACT-015", "TLS-REC-016",
    "TLS-REC-017", "TLS-CH-018", "TLS-CH-019", "TLS-CH-020",
    "TLS-CH-021", "TLS-CH-022", "TLS-CH-023", "TLS-CH-024",
    "TLS-CH-025",
}

def main():
    try:
        data = json.loads(PACK.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot load execution pack: {exc}", file=sys.stderr)
        return 1
    errors = []
    if data.get("format") != "serverless-method-execution-pack":
        errors.append("unexpected format")
    if data.get("format_version") != 1:
        errors.append("unsupported format_version")
    profiles = data.get("profiles")
    if not isinstance(profiles, list):
        errors.append("profiles must be an array")
        profiles = []
    ids = []
    for i, p in enumerate(profiles):
        if not isinstance(p, dict):
            errors.append(f"profiles[{i}] must be an object")
            continue
        pid = p.get("profile_id")
        if isinstance(pid, str):
            ids.append(pid)
        for key in ("name", "family", "implementation_status", "config_format",
                    "parameters", "execution_contract", "validation", "requires"):
            if key not in p:
                errors.append(f"{pid or i}: missing {key}")
        if p.get("default_enabled") is not False:
            errors.append(f"{pid}: must remain disabled by default")
        if not isinstance(p.get("parameters"), dict):
            errors.append(f"{pid}: parameters must be an object")
        if not isinstance(p.get("validation"), list) or not p["validation"]:
            errors.append(f"{pid}: validation must be a non-empty array")
    if len(ids) != len(set(ids)):
        errors.append("duplicate profile IDs")
    if set(ids) != EXPECTED:
        errors.append(f"profile ID set mismatch; missing={sorted(EXPECTED-set(ids))}, extra={sorted(set(ids)-EXPECTED)}")
    safety = data.get("safety", {})
    if safety.get("existing_oob_unchanged") is not True:
        errors.append("existing OOB must be explicitly preserved")
    if safety.get("external_secrets_only") is not True:
        errors.append("secrets must remain external references")
    if data.get("control_profile", {}).get("id") != "BASE-OOB-001":
        errors.append("immutable OOB control reference missing")
    if errors:
        for e in errors:
            print("FAIL:", e, file=sys.stderr)
        return 1
    print(f"PASS: {len(profiles)} method profiles; all IDs unique; configs structurally valid.")
    print("NOTE: structural validation is not Xray importability or network-effectiveness testing.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
