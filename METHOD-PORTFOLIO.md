# Method Portfolio — Stage 1

This is a consolidated engineering inventory for the PattNG/Xray ecosystem. It deliberately separates:
- profiles runnable with the currently available Xray configuration features;
- techniques that require a later Xray-core or client/TUN change;
- techniques that cannot work as requested because TLS authentication forbids them.

## Stage-1 runnable profile pack

File: `Subscription/All-Methods-Stage1.json`

It contains the three current, importable profiles:
1. `Serverless-v67-OOB-BASELINE` — known-good OOB control. Preserve unchanged.
2. `Serverless-v71-TLS-WarnAlert` — prepends the TLS warning alert record `15 03 03 00 02 01 50`.
3. `Serverless-v72-TLS-WarnAlert-OOB` — the same alert preface combined with the existing OOB path.

Important: profiles 2 and 3 are research-derived candidates, not field-proven. The pre-ClientHello alert variant was accepted by only 9.42% of the paper's Tranco top-10k server evaluation. The Iran-censor result does not mean broad server compatibility. Do not treat these as production profiles until full HTTPS data transfer succeeds.

## Independent method families — next implementation stage

| ID | Method | Mechanism | Can current config do it? | Required work |
|---|---|---|---|---|
| M01 | OOB baseline | Existing TCP OOB dial mode | Yes | Keep as control; do not alter |
| M02 | TLS warning-alert preface | Inject a TLS Alert record before ClientHello | Yes | Already in Stage-1 pack; field test required |
| M03 | TLS record-version override | Change outer TLS record version while preserving ClientHello bytes | No | New FinalMask transform in Xray core |
| M04 | SNI-aware TLS-record fragmentation | Parse ClientHello and split at a boundary selected relative to the SNI extension | No | Incremental ClientHello parser + record writer in Xray core |
| M05 | SNI removal / SNI hostname transformation | Rebuild ClientHello and its transcript with a changed or absent SNI | No | Must be implemented by the TLS client; transparent direct-stream rewrite is invalid |
| M06 | Domain-fronting / SNI mismatch | Harmless front SNI plus target HTTP Host routed by a cooperating CDN/service | Not as a generic direct outbound | A compatible fronting provider and TLS/HTTP-aware client/relay |
| M07 | TLS 1.3 CCS injection | Insert a compatibility ChangeCipherSpec at a protocol-valid handshake position | No | Stateful TLS-flight-aware transform; raw preface insertion is not equivalent |
| M08 | HTTP-prefix tunnel transport | Start with a plausible HTTP request prefix, then switch to the tunnel protocol | No | New client/server transport and controlled endpoint; cannot be done by a generic direct config |
| M09 | TCP-level desynchronization | Manipulate packet sequence/overlap/TTL so censor and endpoint parse different streams | No | Packet-level TUN implementation; root is not inherently required if the VPN app owns TUN |
| M10 | QUIC Initial/ECH techniques | ECH privacy or QUIC CRYPTO-frame/Initial fragmentation | Not with current TCP FinalMask | QUIC-aware transport/core implementation; validate against the actual Iranian ISP |
| M11 | MITM DomainFronting | Local TLS termination, then fronted upstream request | Separate existing project | Requires a locally trusted CA for normal browser HTTPS; non-root Android browser scope only |

## SNI spoofing: precise boundary

There are two fundamentally different things often called “SNI spoofing”:

1. **TLS-client-generated SNI mismatch:** the TLS client sends one SNI while the encrypted HTTP Host names another. This is only useful when the receiving front/CDN accepts the mismatch and routes the Host correctly. It is not a universal way to connect to arbitrary origins.
2. **Transparent rewriting of an app's ClientHello:** changing the SNI after the app has generated its TLS ClientHello changes bytes covered by the handshake transcript. A blind stream proxy cannot safely do this and still complete the handshake. It requires TLS-client integration or TLS termination.

The current Serverless direct outbound forwards application TLS; it does not own the app's TLS transcript. Therefore no honest config-only SNI rewrite profile can be supplied for the current core.

## MITM without a certificate

A genuine HTTPS MITM decrypts and re-signs TLS. The client must trust the signing CA (or explicitly disable certificate verification, which is unsafe and not a general solution). The existing MITM-DomainFronting project explicitly asks the user to create and trust a personal CA. It supports non-root Android browser usage, not arbitrary independent apps. A certificate-free, trust-preserving MITM for arbitrary HTTPS is not possible under normal TLS authentication.

The certificate-free alternatives are not MITM: TLS record manipulation, packet-level desynchronization, ECH, or a cooperating domain-fronting endpoint. They do not decrypt arbitrary HTTPS.

## Evidence and validation

The 2025 IEEE S&P paper *Transport Layer Obscurity: Circumventing SNI Censorship on the TLS-Layer* reports 38 techniques grouped into 11 categories and tests against TLS servers plus censors in Iran and China. It emphasizes that a censor bypass is not enough: the destination server must also accept the modified handshake and return the intended page.

Selected reported Tranco top-10k acceptance rates:
- TLS record-header version set to TLS 1.3: 99.11%
- TLS record fragmentation in message body: 92.80%
- TLS record fragmentation in message header: 86.66%
- Internal warning alert before ClientHello: 9.42%
- CCS + TLS 1.3: 4.63%

These are paper measurements, not current success rates on the user's ISP or current web destinations. The paper's Iran measurement used its own vantage point and should not be generalized to every Iranian operator or to current network conditions.

A separate 2025 Iran study reports that censorship behavior differs by ISP and that some Iranian ASes used protocol allowlisting; HTTP GET prefixes survived longer in that particular experiment than TLS/SSH prefixes. That is evidence for researching an HTTP-prefix tunnel, not a ready-to-use generic profile.

## Required acceptance test for every candidate

Do not mark a profile as working based on ping or TCP connect. Record:
1. DNS resolution;
2. TCP establishment;
3. TLS handshake and certificate validation;
4. HTTP status and actual response body;
5. multiple unrelated sites and CDNs;
6. YouTube playback and large downloads;
7. 5–10 minute stability and reconnect;
8. ISP, IPv4/IPv6, destination, and time.

## Safety and compatibility invariants

- The stable subscription `Subscription/Serverless-for-Iran.json` is not changed by this experiment.
- OOB is retained as an unchanged control.
- No claim is made that the alert profiles have been live-tested from the user's network.
- Methods M03–M10 are recorded as core/client work items, not disguised as runnable JSON profiles.
- The client/app is not modified in this stage.
