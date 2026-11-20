# Method Blueprints v1

This branch starts the canonical method portfolio requested for the Serverless-for-Iran / Xray / PattNG work.

## Important distinction

- `Subscription/Method-Blueprints-v1.json` is the **canonical target configuration catalog**. It is deliberately not an importable Xray subscription. It defines methods that need new core, TLS-client, TUN, server, or infrastructure support.
- Existing Xray-compatible profiles remain separate. Never import the blueprint catalog as a normal subscription.
- A method is not considered working because its JSON parses or because ping succeeds.

## First implementation inventory

The catalog contains 15 independently identified methods across TLS record manipulation, TLS ClientHello construction, handshake state, pluggable transports, HTTP transports, packet/TUN methods, provider-backed fronting, QUIC, and Refraction Networking.

## Priority order

1. **P0:** outer TLS record-version override; SNI-position-aware TLS record fragmentation.
2. **P1:** differential record versions; TLSMasq transport; HTTP-prefix tunnel; TCP TUN desynchronization.
3. **P2:** ClientHello padding; trailing-dot SNI; no-SNI; HTTP/2 tunnel; provider-backed fronting; QUIC Initial/CRYPTO mutation.
4. **P3:** compatibility CCS; warning-alert research profile; Conjure infrastructure integration.

This is an engineering priority, not a claim that a method is effective on a particular ISP.

## Existing Xray work discovered

The `Xray-corexr` repository already has a `feature/tls-record-fragment` branch. Its `tls-record` FinalMask type uses `splitAt` and has tests for:
- record splitting while preserving ClientHello bytes;
- pass-through for incomplete first writes;
- client-only behavior;
- a successful local TLS handshake.

That implementation is a useful starting point, but it is **fixed-offset record splitting**, not SNI-aware fragmentation, record-version override, or a complete incremental parser. Do not label those capabilities as implemented.

The `research/tls-mutation-lab` branch contains a separate first-flight probe. It explicitly warns that a TLS handshake record response is not proof of a completed handshake and that extension mutations require transcript-aware TLS-client integration.

## Safety and compatibility

- Existing OOB control is preserved and must remain unchanged.
- No transparent SNI rewrite is allowed to corrupt the TLS transcript.
- No certificate verification bypass is used as a general workaround.
- TLSMasq is a relay/transport protocol, not HTTPS MITM.
- Domain fronting requires a provider and routing service that explicitly support the model.
- TCP desynchronization belongs in PattNG's VPNService/TUN packet path, not in a byte-stream-only Xray FinalMask.
- QUIC Initial mutation requires QUIC-aware packet protection and CRYPTO framing; TCP TLS filters cannot implement it.

## Validation ladder

A candidate advances only through the levels defined in the JSON catalog: schema validity, Xray parser validity, local protocol interoperability, remote endpoint acceptance, censorship testing on the target network, and sustained application testing. Ping-only and TCP-connect-only results never qualify.
