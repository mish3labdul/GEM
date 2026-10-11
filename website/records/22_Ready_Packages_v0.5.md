# 22 · Ready packages section — v0.5 (2026-10-11)

**Owner instruction (13:31 Asia/Riyadh):** "Package set: as proposed. Names: keep as proposed." The slider question was not answered, so the recommended static cards were built. A carousel would need a Part B change-control addition first. Recorded as WD-16 and WD-17 in record 10.
**Status:** the section, its package names and all its copy are **PROPOSED** (names approved as working names). No price, size, units per pack, minimum order or lead time is stated anywhere; each is shown as not yet set or "On quotation".

## What changed
- `#formats` is replaced by **`#packages` "Ready packages"**. Navigation and footer say "Packages" on all three pages.
- **Three package cards**, one radio group where the whole card is the target and arrow keys move the selection:
  - **Room set:** Part D room set. New full-frame 3:2 derivatives `room-set-3x2-{480,800,1200}` from the unchanged original `partD-s20-room-set_1536x1024.png` (`0f85f9d1…`). The 16:9 crop stays on the reference page.
  - **Wall-mounted set:** Part D wall-mounted, 4:5, shown whole inside the shared 3:2 frame on the Ink field and never cropped.
  - **Travel set:** GEM-WEB-B02, with the register caption kept.

  Each card follows the Part B ProductCard order: image, status label, name, then a SpecificationTable (Format, Contains, Price "On quotation", Status), stacked at Compact.
- **Configurator:**
  - "Rooms to supply" is a number-only text field, because the Part B QuantityStepper is for small numbers.
  - "Add arrival stationery" is a Part B Checkbox: 24px box, Ink fill and mark.
  - "Add sampling to brief" is a Part B ToggleButton with `aria-pressed`, a changing label and a status sentence.
  - The primary button reads "Request a quotation" (Part A slide 22).
- **Result:** an INFORMATION alert reading "Quotation request drafted. It has not been sent.", with "Open in your email app" (mailto to the WD-12 address, subject "Quotation request for GEM: [package]") and "Copy request". Any change withdraws the draft. The page sends nothing.
- **Fail-closed** like the enquiry form: submit is prevented first, and the button stays disabled with a visible notice until the script is ready.
- **Programmes moved under the section** as "Need your property's name on the label?", ending with a link to the enquiry with Amenities & Packaging preselected.
- **Arrival image** moved from the old Formats grid to sit beside the configurator as the stationery add-on.

## Proposed copy
Eyebrow "Ready packages" · H2 "Three ways to stock a room." · "Each package holds the five-product pilot family. All three are concepts; we have not yet set prices, sizes or lead times." · names "Room set", "Wall-mounted set", "Travel set" (WD-16) · formats "Pump bottles for the guest bathroom", "Dispensers in wall brackets", "Five travel bottles in a box" · "On quotation" · "For every package, sizes, units per pack and lead times are not yet set. Prices are given on quotation." · "Rooms to supply" / "An estimate is fine." · "Add arrival stationery" / "Welcome card, key sleeve and key card." · "Add sampling to brief" / "Remove sampling from brief" / "Sampling not selected." / "Sampling selected." · "Request a quotation" · "Creates a request to send from your email app. This page sends nothing." · errors "Choose a package." and "Enter the number of rooms, for example 120." · "Your request is missing some details." · "Quotation request drafted. It has not been sent." · "Open it in your email app and send it from there, or copy it." · "Copy request" · "Your choices changed. Request the quotation again to update it." · "Need your property's name on the label?" · "Property Edition and Bespoke Programme are concepts. We have not yet set scope, availability or terms." · "Tell us about your project" · notice "Requesting a quotation needs JavaScript…"

## Deviation from Part B
SpecificationTable says missing values render "[PENDING]". The visitor page instead writes "On quotation" in the cards and states the missing sizes, units and lead times once, in plain words, under the grid. This shows what is missing without bracket codes; the same values stay [PENDING] in the records.

## Verification
Run `records/qa-runs/20261011T103930Z`: **476 checks, 476 PASS** (Chromium). Two development runs are marked SUPERSEDED with reasons. 24 new checks:
- quotation disabled with notice under no-JS and blocked script, and no data-bearing request;
- enabled after init;
- empty submit gives two linked errors and focuses the first;
- a click anywhere on a card selects it;
- arrow keys move the selection;
- the selected card shows a 2px ring;
- invalid rooms produce an error described from the field;
- the sampling toggle changes state, label and status;
- the draft text, mailto address, subject and body match exactly;
- copy works;
- the draft is withdrawn by every control;
- no requests are made.

Each journey check runs at 1440 and 375. Visual review at 1440, 768 and 375. Lab LCP 1.95s (v0.4.2: 1.85s), CLS 0, 305,769 bytes.

## Hashes, v0.4.2 → v0.5 (SHA-256, first 12)
index.html `4a96e359e3f0 → ddddb859cb45` · reference.html `b8acb5702874 → e1d6bf3aebdc` · privacy.html `72c9bd6b9a4e → 11629fb29cb0` · site.css `dfb86e228554 → b1dca59c94a8` · site.js `b6752ba06d78 → b786f195c271` · qa/run_qa.py `→ 78e124c33316` · six `room-set-3x2-*` derivatives added.

## What real purchasing still needs from the owner
Verified sizes, units per pack, price or price bands, minimum order, lead times, VAT treatment, delivery regions, payment terms and sampling policy. With those, "On quotation" can become prices and an order action without redesigning the cards.
