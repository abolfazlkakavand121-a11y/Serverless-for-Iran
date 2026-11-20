# Method Execution Pack v1

This package converts every non-control method in Method-Blueprints-v1 into a method-specific configuration object and an explicit runtime adapter contract.

## What this is (and is not)

- Contains **25 separate profiles**, one for every non-OOB method in the research catalog.
- Each profile has a unique ID, runtime/config format, concrete parameters, implementation owner, required components, invariants, and validation sequence.
- All profiles are disabled by default. The existing OOB baseline is referenced only as an immutable control.
- This is **not** a single importable Xray subscription. Several methods fundamentally require changes to Xray TLS internals, a TLS ClientHello builder, PattNG's Android VPNService/TUN engine, QUIC packet processing, a cooperating server, a CDN/provider, or Conjure station infrastructure.
- Do not import this JSON into Xray/PattNG as though it were an Xray outbound. The adapters named in the pack must be implemented first.

## Profile classes

| Runtime class | Profiles |
|---|---|
| Xray FinalMask TLS record engine | TLS-REC-001, TLS-REC-002, TLS-REC-003, TLS-REC-016, TLS-REC-017 |
| TLS ClientHello builder | TLS-REC-004, TLS-CH-005, TLS-CH-006, TLS-CH-018 through TLS-CH-025 |
| TLS handshake state machine | TLS-HS-007 |
| Existing experimental header adapter | TLS-HS-008 |
| Dedicated client/server transports | TLS-TR-009, HTTP-TR-010, HTTP-TR-011 |
| Android VPNService/TUN | TCP-TUN-012 |
| Provider-dependent fronting | FRONT-013 |
| QUIC packet/CRYPTO engine | QUIC-014 |
| Refraction Networking infrastructure | REFRACT-015 |

## Important compatibility distinctions

- TLS record header mutation does not alter the authenticated ClientHello handshake bytes.
- ClientHello content changes must be made by the TLS client before transcript hashing; blind post-generation mutation is unsafe.
- Malformed vectors (record content-type, nested length fields, duplicate/invalid SNI forms) are research probes, not recommended live profiles.
- TLSMasq is a relay-by-default pluggable transport, not HTTPS MITM.
- HTTP prefix, HTTP/2 tunnel, fronting and Conjure require cooperating server/provider/infrastructure; client-only config cannot make them work.
- TCP desynchronization belongs to a packet-aware TUN implementation, not a stream-only proxy.
- QUIC Initial processing requires QUIC packet protection and CRYPTO stream awareness.

## Validation

The pack is machine-readable and should be schema-validated. That only proves configuration structure. No profile is considered working until it passes local protocol interoperability, remote HTTP body tests, target-network testing, YouTube/large-transfer testing, sustained stability, and reconnect checks.
