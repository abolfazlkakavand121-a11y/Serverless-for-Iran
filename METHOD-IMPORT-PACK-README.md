# Method Import Pack v1

This is the **PattNG/Xray importable configuration list**, distinct from `Method-Execution-Pack-v1.json`.

- Root is a JSON array of **4 complete Xray configurations**, so subscription importers can enumerate each item separately.
- Every item is cloned from the existing Serverless fragA baseline, has its own `remarks`, and routes TCP TLS / TCP port 443 through the new `method-tls` outbound.
- The four entries exercise the two currently implemented FinalMask mechanisms:
  1. TLS outer record version 0x0301
  2. TLS outer record version 0x0303
  3. SNI-aware split before the SNI extension
  4. SNI-aware split inside the hostname
- Existing OOB control and the stable `Serverless-for-Iran.json` subscription are not modified.

## Important validation status

The corresponding Xray adapter's targeted unit tests passed and the PattNG ARM64 debug validation APK built successfully. These facts establish that the app/core build contains the implementation; they do **not** establish that any of the four profiles works on every ISP or destination. Iranian-network, YouTube, sustained-transfer and reconnect tests remain required.

The other 21 catalog entries are intentionally **not included as fake Xray configs**. They need additional TLS-client, packet/TUN, QUIC, server, provider or Refraction infrastructure, or are malformed-packet research probes. Their contracts remain in `Method-Execution-Pack-v1.json`.

Import this file as a subscription/list of Xray configs. Do not import `Method-Execution-Pack-v1.json` as an Xray subscription.
