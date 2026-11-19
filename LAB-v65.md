# Serverless v65 — FragC true TLS split

This is an isolated experiment based on the upstream v64 FragA profile.

Changes from v64:
- Replaced the two-layer TLS fragment chain with one `tlshello` fragment mask on the three TLS-fragment outbounds.
- Uses a 1 ms inter-record delay. In the pinned Xray implementation, a zero-delay TLS-hello fragment chain is coalesced into one write; a nonzero delay exercises separate writes. TCP may still coalesce writes on the wire, so packet capture/runtime testing is required.
- Removed the merge mask from the general direct TCP outbound and TLS-fragment/try outbounds. The general direct path no longer adds the extra 30 ms buffering, and the TLS ClientHello fragments are not buffered by merge before being written.
- The Cloudflare try outbound now falls back to the Cloudflare-specific fragment outbound.
- No OOB is used. DNS and routing are otherwise inherited from v64 FragA.

This is a diagnostic experiment, not a guaranteed censorship bypass. Direct outbound cannot defeat destination-IP blocking or replace a relay. Keep v64 profiles as controls.
