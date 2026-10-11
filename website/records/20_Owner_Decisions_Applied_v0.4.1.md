# 20 · Owner decisions applied — v0.4.1 (2026-10-11)

Decisions WD-12 to WD-15 are recorded verbatim in record 10.

## Changes
| Path | v0.4 → v0.4.1 (SHA-256, first 12) | Change |
|---|---|---|
| site/assets/js/site.js | 5b816141ddc4 → b6752ba06d78 | `DELIVERY.mailto = "mish3labdul@gmail.com"` (WD-12) |
| site/index.html | a0a97bf36452 → b760d3a0f344 | Enquiry copy now describes the email hand-off; in the drafted result, "Open in your email app" comes first, then "Copy enquiry" (one filled button) |
| site/privacy.html | 1dce5a400843 → dfebc76d894f | "Sending an enquiry" section rewritten for the hand-off; field list updated to the v0.4 form |
| qa/run_qa.py | 10d1c4bd71cb → 1f9ea3b4e40a | The C1 check now asserts the hand-off is hidden until drafting, is addressed to the owner address, carries exactly the draft as its body, and is withdrawn on any edit. The link is read, never followed. |

## New copy (PROPOSED: written after the WD-14 approval)
- Enquiry lead: "Your draft stays on this page until you choose to send it from your own email app."
- Under the button: "Creates a draft to copy or send from your email app. Nothing is sent from this page."
- Drafted result: "Copy it, or open it in your email app and send it from there."
- Privacy notice, "Sending an enquiry": "If you choose “Open in your email app”, the draft opens in your own email program, addressed to GEM. Nothing leaves your device unless you send it from there. The details you send (your name, email address, organisation or property, and message) will be used only to reply to your enquiry. GEM’s approved notice will say how long enquiries are kept and how to ask for them to be corrected or deleted."

## Verification
Run `records/qa-runs/20261011T095042Z`: **450 checks, 450 PASS** (Chromium). The run before it (`…094908Z`, also 450/450) is marked SUPERSEDED because the button order changed afterwards. No email was sent and no network request carried form data.

## Open
- The footer and privacy-page contact blocks still show the WD-03 temporary details (`hello@gem.example`), while the hand-off goes to the owner address. Decide whether that address should also appear there, or wait for GEM's final contact details.
- Privacy wording is still proposed best practice (WD-02) and needs legal review before public launch. A personal Gmail address as the business enquiry address is the owner's choice. It is visible in the page source once published.
- Screen-reader and cross-browser testing postponed (WD-15).
