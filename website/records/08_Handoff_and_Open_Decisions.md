# 08 · Handoff — session 1 (2026-10-10)

## State
- Working responsive homepage with shared header and footer: `site/index.html` + `assets/`. Static HTML/CSS/JS, no build step, no dependencies, no third-party requests.
- Records 01–07 in `records/`. All copy and imagery **PROPOSED**; nothing accepted yet.
- Nothing published, deployed, pushed, tagged or merged. The release package and the logo kit folder were not modified.
- A private claude.ai artifact preview may exist (see conversation); it is not shared.

## Owner decisions needed (blocking further pages)
1. **Does a website exist elsewhere?** None was found in the folders or the GitHub repo.
2. **Receiving destination for enquiries** (email address or service) and the privacy text to show beside the form. Until then the button stays "Prepare enquiry".
3. **Contact details, legal entity name and legal/privacy pages** for the footer.
4. **Public web use of the logo kit** (RP01 marks it external issue RESTRICTED, not a production master).
5. **Image rights (VAL-06)** for the three concept/reference studies, and whether rendered studies may appear publicly at all with a "concept study" caption.
6. **Part D product mockups**: may any be shown publicly? They carry unapproved Arabic, a typeset "GEM™" that is not the kit lockup, and the unapproved name "Amenities Collection". Options: keep excluded / re-render without text / commission photography.
7. **Programme options**: may the three CONDITIONAL tiers be shown as "being defined"? Name for the consistent range ("Core Collection" is [REQUIRES OWNER]).
8. **Market statement**: confirm "built for hospitality in Saudi Arabia and the wider GCC" and "An Arabic edition is in preparation".
9. **™ usage** in running text and in the hero mark (Legal/IP).
10. **Alt text approval** for the three images (OD-G03, Accessibility Content Owner).
11. **Tokens note**: confirm the website may implement token values although the token package says "component implementation not authorized".

## Next actions (independent of the decisions)
- Read the executive summaries of AR01, AX01, D3, D7, FD01, HR01, NP01 and ODI01 in the parent folder (only FA01 and OD01 decisions were read this session).
- Build the reference area shell (`/reference/`) from Parts A and B, English only, no downloads.
- Split homepage sections into the planned pages once decisions 2, 6 and 7 land.
- Cross-browser pass (Safari, Firefox) and a VoiceOver/NVDA pass.
- Record the Jost 3.710 / Inter 4.001 builds in Part C slide 15 font control (VAL-05).

## How to run
`cd site && python3 -m http.server 8000` then open http://localhost:8000. Verification: start the server on port 8765 and run `python3 verify_shots.py` and `python3 verify_func.py` (Playwright + Chromium; axe-core path inside `verify_func.py`).
