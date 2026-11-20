# Method Portfolio — Blueprint v1

The canonical target configurations are in [Subscription/Method-Blueprints-v1.json](Subscription/Method-Blueprints-v1.json).

**This file is an engineering catalog, not an importable Xray subscription.** Each entry has a unique method ID, target config, runtime owner, client/server dependencies, fallback behavior, and validation constraints.

## Current state discovered in repositories

- The stable subscription `Subscription/Serverless-for-Iran.json` is not modified.
- The known-good OOB profile remains the control and is not modified.
- The experiment branch's `All-Methods-Stage1.json` contains only the three existing OOB / TLS Alert profiles. It is not a complete method pack and must not be represented as one.
- Xray branch `feature/tls-record-fragment` already implements a fixed-offset TLS record split using `type: tls-record` and `settings: { "splitAt": 2 }`. Its tests cover byte preservation, incomplete-write pass-through, client-only operation, and local TLS handshake interoperability.
- This fixed-offset feature is not SNI-aware fragmentation, record-version override, ClientHello rewriting, or TCP packet desynchronization.
- Xray branch `research/tls-mutation-lab` contains a controlled first-flight probe; it is not a production transport.

## Method families

| Family | Methods | Runtime owner |
|---|---|---|
| TLS record | outer record version override; SNI-aware record boundaries; per-fragment record versions | Xray FinalMask |
| TLS ClientHello | padding; trailing-dot SNI; no-SNI construction | TLS client / uTLS integration |
| TLS handshake | state-aware CCS; warning-alert research candidate | TLS state machine / existing FinalMask |
| Pluggable transport | TLSMasq relay-by-default | dedicated client + listener |
| HTTP transport | authenticated HTTP-prefix; HTTP/2 stream tunnel | dedicated client + server |
| Packet layer | TCP desynchronization | PattNG VPNService/TUN |
| Fronting | provider-backed SNI/authority separation | TLS client + cooperating provider |
| QUIC | Initial / CRYPTO-frame mutation | QUIC core |
| Refraction | Conjure client/station | external station infrastructure |

## Priority

P0: TLS record-version override and SNI-aware fragmentation.

P1: TLSMasq, authenticated HTTP-prefix transport, TCP TUN desynchronization, and differential record versions.

P2: ClientHello padding, hostname form variants, no-SNI, HTTP/2, provider-backed fronting, and QUIC.

P3: CCS and Conjure deployment integration.

Priority is an implementation order, not an effectiveness ranking.

## Rules

1. Never call a blueprint importable until its runtime parser and implementation exist.
2. Never claim live ISP success without target-network measurements.
3. A server's acceptance rate is not a censorship-bypass probability.
4. Keep OOB unchanged as a control.
5. No blind SNI rewrite, no certificate-validation bypass, and no fake certificate-free HTTPS MITM.
6. Every profile must pass TLS certificate validation, real HTTP response checks, multi-site tests, YouTube, large transfer, and sustained stability before promotion.
