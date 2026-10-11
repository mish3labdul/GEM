# Booking flow — CONCEPT / IMPLEMENTATION TEST (Part B RC2, slide 26)

**Purpose:** test step order, primary-action logic, errors, validation, focus, responsive behaviour, Arabic/RTL, DatePicker and selected states using existing components only. **Not a live product.** Runtime behaviour is **NOT TESTED** until the component bundle exists (VAL-13, VAL-20).

| Step | Components | Primary action | Error / validation | Focus | RTL | Responsive |
|---|---|---|---|---|---|---|
| 1 Search / availability | Field (property), DatePicker trigger, QuantityStepper summary, Button | "Check availability" | missing property: ERROR label, "Choose a property.", above the field, aria-invalid + aria-describedby | on load: page heading; on error: first invalid field | arrows and step order reverse; property name Latin/Arabic per locale | Compact: single column, full-width primary |
| 2 Dates | DatePicker (range), Button | "Keep dates" | departure before arrival: "Choose an arrival date before the departure date." | into the grid on open; back to the trigger on close | grid flows RTL; Left/Right keys swap; Arabic-Indic digits for ar-SA guest copy | Compact: full-width sheet; Desktop: inline two-month |
| 3 Guests | QuantityStepper × 2, Select (rooms), Button | "Continue" | zero guests: "Choose at least one guest." | step heading on entry | stepper +/− do not mirror; labels start-aligned | Tablet: two-up |
| 4 Room | RoomCard list, Tabs (views), Button | "Continue" (enabled when a card is selected) | none selected: "Choose a room." | selected card announces aria-pressed=true | card order and tabs reverse; prices [PENDING], Latin digits for codes | Desktop: 12 columns, three-up cards; Compact: stacked |
| 5 Confirmation | Alert CONFIRMED, SpecificationTable, Link | none (Link "Review booking") | — | focus to the Alert (role=status) | booking ID GEM-[PENDING] stays LTR in `<bdi>` | table restacks at Compact |

**Rules exercised:** one primary per view (Q11); feedback hierarchy label → title → actionable sentence (slide 19); no colour-only state (V10); 44 px targets (V12); focus ring 2 px / 2 px offset (V08); reduced motion drops movement (V11); no invented price, time or availability promise (F01–F08).

**Result record:** DOCUMENTED (design-level); runtime NOT TESTED; Arabic PENDING NATIVE QA.
