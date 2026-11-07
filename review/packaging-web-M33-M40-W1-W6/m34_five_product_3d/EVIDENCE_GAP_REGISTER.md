# M34 Evidence & Specification Gap Register — Five-Product Range

**Milestone:** M34 (Five-Product Provisional 3D Expansion)  
**Date:** 2026-11-07  
**Authorization:** Authorization B (`GEM-PKG-OWNER-20261107-005`)  
**Scope:** Shampoo, Conditioner, Body Wash, Body Lotion, Hand Wash

---

## 1. Executive Summary

This register formally catalogs all known technical, physical, regulatory, and typographic evidence gaps for the five-product GEM™ hospitality collection as modeled in `GEM_M34_five_products_PROVISIONAL.blend`.

All five models are classified as **`PROVISIONAL_EXPLORATORY_GEOMETRY`**. They are created under **Authorization B (`GEM-PKG-OWNER-20261107-005`)** solely for internal CGI design studies, digital experience prototypes, and staging website demonstrations. **No model represents owner-approved physical packaging or manufacturing specifications.**

---

## 2. Specification Gap Matrix

| Product Key | English Name | Arabic Name | Geometry Classification | Capacity Evidence Status | Physical Tooling Evidence | Label Content Status | Regulatory & INCI Status | Production Release Gate |
|---|---|---|---|---|---|---|---|---|
| `shampoo` | SHAMPOO | شامبو | `PROVISIONAL` (M27a) | Inferred (~204 mL) | MISSING | Confirmed Front Only (M15 Layout A) | MISSING | **NOT AUTHORIZED** |
| `conditioner` | CONDITIONER | بلسم | `PROVISIONAL` (M27a) | Inferred (~204 mL) | MISSING | Confirmed Front Only (M15 Layout A) | MISSING | **NOT AUTHORIZED** |
| `body_wash` | BODY WASH | غسول الجسم | `PROVISIONAL_EXPLORATORY_GEOMETRY` | Inferred (~204 mL) | MISSING | Confirmed Front Only (M15 Layout A) | MISSING | **NOT AUTHORIZED** |
| `body_lotion` | BODY LOTION | لوشن الجسم | `PROVISIONAL_EXPLORATORY_GEOMETRY` | Inferred (~204 mL) | MISSING | Confirmed Front Only (M15 Layout A) | MISSING | **NOT AUTHORIZED** |
| `hand_wash` | HAND WASH | غسول اليدين | `PROVISIONAL_EXPLORATORY_GEOMETRY` | Inferred (~204 mL) | MISSING | Confirmed Front Only (M15 Layout A) | MISSING | **NOT AUTHORIZED** |

---

## 3. Detailed Gap Breakdown

### GAP-01: Absence of Physical Tooling Drawings & Glass Supplier Specifications
- **Description:** No glassmaker technical drawings (e.g. Owens-Illinois, Gerresheimer, Bormioli Luigi) or engineering specifications exist in the workspace.
- **Impact:** Outer diameter (`76.3 mm`), wall thickness (`2.5 mm`), base push-up depth, and thread finish (`28/410` vs `24/410`) are provisional mathematical approximations derived from front-silhouette reference matching.
- **Safeguard:** Parameter JSON (`m34_five_product_params.json`) explicitly separates confirmed brand metadata from exploratory geometry.

### GAP-02: Nominal Capacity & Liquid Fill Level Unverified
- **Description:** Stated capacity (~204 mL at 90% fill height) is a mathematical voxel/mesh volume integration. No physical fill line or brimful overflow test has occurred.
- **Impact:** Commercial capacity claims (e.g., 200 mL, 250 mL, or 300 mL) cannot be published or marketed.
- **Safeguard:** UI and documentation must display `PROVISIONAL EXPLORATORY CGI` disclaimer on 3D viewers.

### GAP-03: Pump Dispenser Silhouette vs Internal Mechanism
- **Description:** The satin-black pump actuator, collar, stem, lock-tab, and spout are modeled as external solid geometric surfaces based on reference photography. Internal spring, piston, ball valve, and gasket mechanisms are omitted.
- **Impact:** Models cannot be used for mold fabrication or mechanical tolerance checks.
- **Safeguard:** Models are restricted to visualization assets (GLB/GLTF, renderings).

### GAP-04: Absence of Back-Label, INCI, and Regulatory Copy
- **Description:** Only M15 front bilingual labels (Layout A) exist. Mandatory regulatory items (full INCI ingredients list, country of origin, PAO symbol, batch code, net volume statement, hazard warnings) are absent.
- **Impact:** Physical print packaging cannot be commissioned.
- **Safeguard:** Front labels remain concept/presentation artwork only.

### GAP-05: Native Arabic Reader Typographic Review Pending
- **Description:** The Arabic product names are locked by owner decision (`GEM-PKG-OWNER-20261107-002`) and set in Noto Sans Arabic. Formal human native-reader review has not yet been executed.
- **Impact:** Optical letter-spacing or calligraphic nuances have not been validated by an external specialist.
- **Safeguard:** M38 outreach package is prepared under Authorization C (`GEM-PKG-OWNER-20261107-006`) without modifying master artwork.
