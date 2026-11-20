# TLS experiment notes

This branch contains an isolated experiment subscription. It does not modify the stable subscription.

## Profiles

- `Serverless-v70-OOB-CONTROL`: the known-good OOB control profile, copied without changing its behavior.
- `Serverless-v71-TLS-WarnAlert`: sends one TLS warning-alert record before the application's original ClientHello using the existing `header-custom` finalmask.
- `Serverless-v72-TLS-WarnAlert-OOB`: combines the same warning-alert preface with the existing OOB TCP path.

The injected record is the Censor-Scanner paper's `ALERT_INTERNAL_WARN` record: alert payload bytes `01 50` (warning level, internal_error description), carried in the TLS Alert record prefix `15 03 03 00 02 01 50`. It is not a fake certificate, does not decrypt traffic, and does not alter the ClientHello bytes or its transcript.

## Evidence and limitations

The 2025 IEEE S&P paper [*Transport Layer Obscurity: Circumventing SNI Censorship on the TLS-Layer*](https://doi.org/10.1109/SP61157.2025.00151), with its [Censor-Scanner implementation](https://github.com/tls-attacker/Censor-Scanner), reports that an internal warning alert before ClientHello bypassed the tested Iranian censor, but the technique had limited server acceptance: 9.42% in the paper's Tranco top-10k evaluation. Treat this as a targeted experiment, not a general-purpose profile. The paper also recommends checking that the real server accepts the modified handshake, not merely that the censor did not block it.

The alert-only profile and the alert+OOB profile are hypotheses for testing on the user's actual Iranian access network. They have not been live-tested from that network. A valid JSON document and known Xray mask syntax are not proof of network success.

## Why SNI spoofing / certificate-free MITM are not included as working profiles

A transparent Xray direct outbound forwards the application's TLS stream. It cannot arbitrarily rewrite the SNI extension, remove it, or replace the hostname and still preserve the TLS handshake transcript. Those changes must be made by the TLS client implementation itself, or by a TLS-terminating MITM trusted by the application. The research paper explicitly distinguishes transcript-preserving record-level changes from ClientHello-content changes.

The upstream [MITM-DomainFronting project](https://github.com/patterniha/MITM-DomainFronting) requires a locally trusted CA certificate and documents browser-only use on non-root Android. A certificate-free MITM that decrypts arbitrary HTTPS traffic is not possible under normal TLS authentication. Do not describe SNI spoofing, domain fronting, and TLS interception as the same mechanism.

## Candidate methods for the next core/client stage

1. **TLS record-header version override** — change only the outer TLS record version to TLS 1.3 while preserving the handshake bytes. The paper reports 99.11% acceptance in its Tranco evaluation and success against the Iranian censor. This needs a new FinalMask capability; it is not supported by the current config parser.
2. **SNI-aware record fragmentation** — parse ClientHello and place a TLS record boundary immediately before, inside, or after the SNI field. This is structurally different from fixed byte-count splits and needs a ClientHello-aware core implementation.
3. **SNI omission / hostname transformation** — promising in the paper, but requires the TLS client to build the altered ClientHello and compute the transcript over those exact bytes, or a trusted MITM. Not a config-only transparent-proxy feature.
4. **TUN-level TCP desynchronization** — inject carefully constructed decoy/out-of-window TCP segments while leaving the real TLS stream intact. This could avoid a CA certificate and Android root, but needs packet-level control in the VPN/TUN client rather than FinalMask's stream-level `net.Conn`.

## Test discipline

For each profile, record separately:
- DNS resolution result;
- TCP connect and TLS handshake result;
- HTTP response status and whether the requested content is actually returned;
- YouTube playback / large downloads;
- 5–10 minute stability and reconnect behavior;
- whether the result changes by ISP, destination CDN, IPv4/IPv6, and time.

A ping or a successful TCP connect is not a successful method. Keep the stable OOB subscription untouched.
