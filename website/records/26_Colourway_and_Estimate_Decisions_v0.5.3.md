# Owner website decisions — colourways and room estimates

Recorded 12 October 2026 from direct answers in this chat. Working website **v0.5.3**.

| ID | Owner answer verbatim | Implementation |
|---|---|---|
| WD-20 | "Keep both and refine documents accordingly" | Retain amber hand wash in GEM-WEB-B01 (amenity-family) and ivory hand wash in GEM-WEB-B04 (guest-arrangement) as concept variations. Identify the variation in each public caption and this current supporting record. All master and derivative image bytes are unchanged. |
| WD-21 | "Remove the custom ceiling; accept positive whole-number estimates" | Remove the 100,000-room validation ceiling. Accept trimmed ASCII decimal digits containing at least one non-zero digit; preserve the entered estimate in the draft without numeric conversion or rounding. Reject empty, zero, negative, decimal and scientific-notation input. This is an enquiry estimate, not a supply-capacity claim. |

[Colourway asset register](colourway-concept-register-v0.5.3.csv) identifies both original masters and their six public derivatives by full SHA-256. These are retained generated concepts, not confirmed SKU colours, production artwork or photographs. No replacement imagery or document export is created. The released V3.0 controlled documents remain exact copies.

This supersedes the website colourway owner-choice gap in historical record 17 and the room-ceiling deferral in record 24. Historical records retain their original wording. Final product colour selection remains pending. The “Amenities Collection” lid wording remains an unapproved placeholder; retaining the two colourways does not approve that name. Working package names, pending availability/specifications and draft-only enquiry-address placement from WD-18/WD-19 remain in force.

Prior public sources and QA scripts are preserved under `archive/website-v0.5.2-before-colourway-and-estimate-decisions/`, with exact paths and hashes in the inventory/migration register. Version lineage is in `site-revisions.json`. Business/legal identity and public contact details, privacy acceptance, hosting, cross-browser/native human validation, email-client behaviour and existing release restrictions remain pending.
