# GEM™ Product Asset Registry (M33 Deliverable)

**Document Version:** 1.0  
**Release Date:** 2026-11-07  
**Program:** GEM™ M33–M40 (Packaging & 3D Asset System) + W1–W6 (Digital Experience Transformation)  
**Governance References:**
- `GEM-PKG-OWNER-20261107-001` — Approved English Ink front-label concept for 5 products.
- `GEM-PKG-OWNER-20261107-002` — Locked 5 Arabic product names (`شامبو`, `بلسم`, `غسول الجسم`, `لوشن الجسم`, `غسول اليدين`).
- `GEM-PKG-OWNER-20261107-003` — Bilingual Layout A, Jost + Noto Sans Arabic pairing, left-aligned Arabic composition.
- `GEM-PKG-OWNER-20261107-004` (Authorization A) — M29 Visual & Blender Master Baseline Approved for Internal Development.
- `GEM-PKG-OWNER-20261107-005` (Authorization B) — Three Additional Product Models Authorized for Exploratory CGI Development.

---

> [!CAUTION]
> **COMMERCIAL APPROVAL STATUS: INTERNAL DEVELOPMENT AND STAGING ONLY — NOT COMMERCIAL.**  
> Under Owner Authorization A (`GEM-PKG-OWNER-20261107-004`), all 3D geometries, Cycles CGI renders, and derived digital assets are authorized strictly for internal product design presentations, UX prototyping, staging website demonstrations, and Three.js/WebGL asset authoring. No physical bottle dimensions, wall thicknesses, capacities, or closures have received commercial manufacturing sign-off. Do not present provisional CGI models as physical manufacturing specifications.

---

## 1. Registry Architecture & Classification Standard

This registry establishes the single cryptographic source of truth for GEM's physical-digital packaging assets across Milestone M33. Every asset is classified according to four strict technical axes:

1. **Geometry Status:**
   - `PROVISIONAL_M27A`: Refined bottle, pump, collar, stem, actuator, and spout meshes for Shampoo and Conditioner based on M16 concept photography reference, verified in M27. Retains provisional dimensional assumptions (76.3 mm body, 24/410–28/410 neck interface).
   - `PROVISIONAL_EXPLORATORY_GEOMETRY_M34`: Concept-level 3D procedural reference geometry authorized by Authorization B (`GEM-PKG-OWNER-20261107-005`) for Body Wash, Body Lotion, and Hand Wash to support 5-product digital staging.
   - `LEGACY_PRE_M16_DO_NOT_USE`: Historical early campaign meshes (`S1_Bottle`, etc.) preserved intact within superseded Blender scenes for audit continuity. Strictly excluded from production CGI and staging pipelines.
   - `NOT_APPLICABLE_2D_TEXTURE` / `NOT_APPLICABLE_2D_VECTOR`: 2D artwork and vector assets.

2. **Material Status:**
   - `M28_FINAL_CALIBRATED`: Calibrated Cycles node-tree materials verified in M28/M29 (`GEM_M17 amber glass`, `GEM_M17 amber liquid`, `GEM_M17 pump head`, `GEM_M17 pump collar`, `GEM_M17 pump stem`, `GEM_S3D gem_dip_tube_clear`, and label shaders).
   - `LEGACY_UNVERIFIED`: Materials in legacy campaign scenes that do not conform to M28 calibration.

3. **Label Approval Status:**
   - `GEM-PKG-OWNER-20261107-001/-002/-003`: Validated bilingual front labels executed by `build_labels_m15.py` with HarfBuzz shaping, byte-identical between external PNG textures and Blender packed datablocks.

4. **Commercial Clearance:**
   - `INTERNAL_DEVELOPMENT_AND_STAGING_ONLY_NOT_COMMERCIAL`: Enforced across 100% of registry entries.

---

## 2. Canonical Master Blender File Identity

| Attribute | Specification / Verification Value |
|---|---|
| **Canonical Path** | `review/packaging-identity-M27-M32/m29_photography/scenes/GEM_M29_MASTER_UNAPPROVED.blend` |
| **Filesystem Status** | Mode `0444` (read-only system lock; write protection enforced) |
| **File SHA-256** | `4d5ad586be1e8dc69d8e97fa3050a269a2ce7fe7d29d03eb83ba1f6e5e12ad39` |
| **File Size** | `82,755,908` bytes (~82.8 MB) |
| **Blender Version** | `5.2.3 LTS` (commit hash `e13b728c6880`) |
| **Direct Ancestor** | `GEM_M28_materials_UNAPPROVED.blend` (`fb860e49fd3f12414200b6de4b276c55281835a2948006903ea2fee196259090`) |
| **External Links** | `0` (Fully self-contained; zero external library dependencies) |
| **Unpacked Images** | `0` (All label textures and environment maps packed internally) |
| **Embedded Reproducibility** | Contains standalone Python render runner `M29_render.py` (`8c5ae010...`) and presets |

---

## 3. Five-Product Asset Catalog

| Product ID | English Name | Arabic Name | 3D Collection | Geometry Status | Material Status | Label Texture SHA-256 |
|---|---|---|---|---|---|---|
| `shampoo` | Shampoo | شامبو | `GEM_S3D_shampoo` | `PROVISIONAL_M27A` | `M28_FINAL_CALIBRATED` | `4a094258adfb801b02fdbc6a823a09463fc33ff5a06eb6e4f9d3b67507bcec8e` |
| `conditioner` | Conditioner | بلسم | `GEM_S3D_conditioner` | `PROVISIONAL_M27A` | `M28_FINAL_CALIBRATED` | `3f80484fe38dd1771b5a2d8862bc5a008a077a9633e344951431fffeefbce627` |
| `body_wash` | Body Wash | غسول الجسم | `GEM_S3D_body_wash` | `PROVISIONAL_EXPLORATORY_GEOMETRY_M34` | `M28_FINAL_CALIBRATED` | `06e4b3ab447b8b0de4e739617d87a568413ef0baac80eca7641f49fb4c37db94` |
| `body_lotion` | Body Lotion | لوشن الجسم | `GEM_S3D_body_lotion` | `PROVISIONAL_EXPLORATORY_GEOMETRY_M34` | `M28_FINAL_CALIBRATED` | `11e8fc08fb172d85057419530e79e6eb5c1719d9b5ab206eb629f9cb01a85a98` |
| `hand_wash` | Hand Wash | غسول اليدين | `GEM_S3D_hand_wash` | `PROVISIONAL_EXPLORATORY_GEOMETRY_M34` | `M28_FINAL_CALIBRATED` | `efd4b64d611a67efb287f8c83e6d1da3b24f6177f30fb6cc75ff4e070e64c6f1` |

### Mesh Breakdown per Product Assembly (8 Datablocks per Model):
1. `glass`: Hollow amber glass container shell (nominal 2.5 mm wall thickness, 4.5 mm base band).
2. `liquid`: Calibrated volume interior mesh conforming to container inner boundary with 0.9 fill fraction.
3. `label`: Front cylindrical wrap mesh with UV layout matching Layout A 1356×2000 px texture bounds.
4. `dip_tube`: Clear polymer vertical tube extending from collar into bottom third of liquid volume.
5. `collar`: Screw/crimp finish collar (38 mm outer diameter) seated over glass neck bead.
6. `stem`: Central actuator piston stem (26 mm diameter).
7. `actuator`: Push-down dispensing head with finger contour and bevelled perimeter.
8. `spout`: Elongated horizontal dispensing spout with oblique 53° droplet cut.

---

## 4. Master Blender Scene Inventory (13 Scenes)

The master Blender file consolidates both active development scenes and historical campaign studies:

| # | Scene Name | Classification | Active Camera | Objects | Status & Pipeline Utility |
|---|---|---|---|---:|---|
| 1 | `M8_Lookdev` | **Active Studio Scene** | `M29 cam catalog_light_conditioner` | 53 | **Canonical active studio lookdev.** Hosts `GEM_S3D_shampoo`, `GEM_S3D_conditioner`, studio sweep, softboxes, fill cards, and 12 cameras. Rendered 12 of 13 M29 final images. |
| 2 | `M23_Bathroom_Editorial` | **Active Lifestyle Scene** | `M29 cam bathroom_editorial` | 150 | **Canonical active editorial scene.** Links marble/stone set from `03_Premium_Bathroom`, adds M23b luxury towel props, flags, and houses canonical M27a products. |
| 3 | `03_Premium_Bathroom` | **Architectural Set Donor** | `S3 Camera` | 122 | **Architectural geometry donor.** Set geometry is linked into `M23_Bathroom_Editorial`. Legacy internal `S3 Products` meshes are preserved intact but superseded. |
| 4 | `00_Contact_Sheet` | Preserved Legacy | `CS Camera.004` | 20 | Historical campaign contact sheet layout. References pre-M16 bottle meshes. Excluded from rendering. |
| 5 | `Scene` | Preserved Legacy | `Hero 65mm` | 30 | Historical early architectural hero study (65mm). Retains pre-M16 meshes. Excluded. |
| 6 | `Scene.001` | Preserved Legacy | `S1 Camera Landscape` | 61 | Inherited campaign scene S1. Retains pre-M16 `S1 Products`. Excluded. |
| 7 | `02_Hotel_Suite` | Preserved Legacy | `S2 Camera` | 146 | Inherited campaign scene S2. Retains pre-M16 `S2 Products`. Excluded. |
| 8 | `04_Editorial_Still_Life` | Preserved Legacy | `S4 Camera` | 52 | Inherited campaign scene S4. Retains pre-M16 `S4 Products`. Excluded. |
| 9 | `05_Product_Collection` | Preserved Legacy | `S5 Camera` | 73 | Inherited campaign scene S5. Retains pre-M16 `S5 Products`. Excluded. |
| 10 | `Campaign_Night_Service` | Preserved Legacy | `Night Service 65mm` | 35 | Inherited night service study. Retains pre-M16 meshes. Excluded. |
| 11 | `Study_Arrival_Cut` | Preserved Legacy | `Arrival Cut hero 50mm` | 37 | Inherited arrival cut study. Retains pre-M16 meshes. Excluded. |
| 12 | `Product_Lookdev` | Preserved Legacy | `Lookdev 85mm` | 16 | Early lookdev setup. Fully superseded by `M8_Lookdev`. Excluded. |
| 13 | `SAND3D_Pilot` | Preserved Legacy | `SAND3D_Cam_HeroFront` | 30 | Inherited M10/M14 pilot scene. Fully superseded by `M8_Lookdev`. Excluded. |

---

## 5. M29 Final CGI Renders Register (13 Verified Renders)

All 13 renders were executed at 256 samples per pixel with Cycles GPU acceleration, verified byte-for-byte in `verify_master.json`:

| # | Asset ID | Output File | Dimensions | Preset | Blender Scene | File Size | SHA-256 Digest |
|---|---|---|---|---|---|---:|---|
| 1 | `GEM-AST-RND-HERO-SHAMPOO` | `renders/final/hero_shampoo.png` | 1600 × 2000 | `studio_hero` | `M8_Lookdev` | 3,017,334 B | `9ab50d306933b84041c94c7ca662898b483aaa1e1416cb3b83fe2c72fb14d24a` |
| 2 | `GEM-AST-RND-HERO-CONDITIONER` | `renders/final/hero_conditioner.png` | 1600 × 2000 | `studio_hero` | `M8_Lookdev` | 3,016,665 B | `d0c01f43ac371f78111ea347df1dd5b9c6b7047df10e6986ddd3f65da4242fd7` |
| 3 | `GEM-AST-RND-3QTR-SHAMPOO` | `renders/final/threequarter_shampoo.png` | 1600 × 1600 | `studio_hero` | `M8_Lookdev` | 2,500,245 B | `523b9751449ea448461f5498e66991c59f8afdab089571b50af9e3d95a89d915` |
| 4 | `GEM-AST-RND-3QTR-CONDITIONER` | `renders/final/threequarter_conditioner.png` | 1600 × 1600 | `studio_hero` | `M8_Lookdev` | 2,499,976 B | `9d978c08f4ee793b7958375efce1884170cb18f2c008bed3898e8346387e6101` |
| 5 | `GEM-AST-RND-FAMILY-PAIR` | `renders/final/family_pair.png` | 2400 × 1500 | `studio_hero` | `M8_Lookdev` | 3,455,099 B | `b92169fbf32c4859e5497d8c06cab55b00782418e543d5c7aff4cf48d57bf2ec` |
| 6 | `GEM-AST-RND-MACRO-PUMP-SHAMPOO` | `renders/final/macro_pump_shampoo.png` | 1500 × 1500 | `studio_hero` | `M8_Lookdev` | 2,264,695 B | `afa73aaf69f1dd1c72df46423b4d7a265b8055b71b48ef13934530af7258c9f5` |
| 7 | `GEM-AST-RND-MACRO-PUMP-CONDITIONER` | `renders/final/macro_pump_conditioner.png` | 1500 × 1500 | `studio_hero` | `M8_Lookdev` | 2,264,192 B | `57abb45b1395bc5069fbbef63dd1e3dc71f98b46d005866139bb8ae4f35b8f7b` |
| 8 | `GEM-AST-RND-MACRO-LABEL-SHAMPOO` | `renders/final/macro_label_shampoo.png` | 1500 × 1500 | `studio_hero` | `M8_Lookdev` | 2,233,158 B | `d166ffdf130c49f5bdd43c1524978e0999045c4cd14e6d62aeed2b1388d2ab4c` |
| 9 | `GEM-AST-RND-MACRO-LABEL-CONDITIONER` | `renders/final/macro_label_conditioner.png` | 1500 × 1500 | `studio_hero` | `M8_Lookdev` | 2,231,487 B | `4b27e4a70539d3fd5c5ed2d48bcb2fd9de9f6e142ab4daacdd18a727a34b65ee` |
| 10 | `GEM-AST-RND-BATHROOM-EDITORIAL` | `renders/final/bathroom_editorial.png` | 2400 × 1500 | `bathroom_editorial` | `M23_Bathroom_Editorial` | 3,740,256 B | `feceb7d2dd727924f43f7631b30916e3c68b7c3f827bb2293ff7679e0a86838c` |
| 11 | `GEM-AST-RND-EDITORIAL-WINDOW` | `renders/final/editorial_window.png` | 2400 × 1500 | `editorial_window` | `M8_Lookdev` | 3,741,026 B | `bee9e967a0501d4d7547d89a106472effaed4fc4182f8201644db4aa6b87ab67` |
| 12 | `GEM-AST-RND-CATALOG-LIGHT-SHAMPOO` | `renders/final/catalog_light_shampoo.png` | 1600 × 2000 | `studio_catalog` | `M8_Lookdev` | 3,160,845 B | `e0dd0188138bf78af99cbe9a44e4d6613ae9f95befda520f0e0829d7157afac1` |
| 13 | `GEM-AST-RND-CATALOG-LIGHT-CONDITIONER` | `renders/final/catalog_light_conditioner.png` | 1600 × 2000 | `studio_catalog` | `M8_Lookdev` | 3,161,786 B | `a04be2495eed8a86a9a079c714e09d865ad28865947315a855194c53ed3de02d` |

---

## 6. Approved Bilingual Label Artwork (5 Products)

All labels conform to Layout A with shared text origin `x = 200 px`:
- **Canvas Dimensions:** 1356 × 2000 px RGBA
- **Brand Palette:** Ink `#12171D`, Beige `#BCACA7`, White `#FFFFFF`
- **English Typography:** Jost Regular, 112 px, baseline `y = 855 px`
- **Arabic Typography:** Noto Sans Arabic Regular, 104 px, baseline `y = 1040 px`, left-aligned ink edge at `x = 200 px`

| Product | Format | Source Path | File Size | SHA-256 Digest |
|---|---|---|---:|---|
| **Shampoo** | PNG (Raster Texture) | `review/packaging-identity-M15-M20/m15_artwork/textures/gem_shampoo_ink_bilingual_A_v1.0.png` | 64,052 B | `4a094258adfb801b02fdbc6a823a09463fc33ff5a06eb6e4f9d3b67507bcec8e` |
| | SVG (Vector Master) | `review/packaging-identity-M15-M20/m15_artwork/svg_masters/gem_shampoo_ink_bilingual_A_v1.0.svg` | 13,557 B | `72e7c2a5b135d3e9e09756477aa979516ec77bb9cea304ed482d2db9f6f77bab` |
| **Conditioner** | PNG (Raster Texture) | `review/packaging-identity-M15-M20/m15_artwork/textures/gem_conditioner_ink_bilingual_A_v1.0.png` | 63,134 B | `3f80484fe38dd1771b5a2d8862bc5a008a077a9633e344951431fffeefbce627` |
| | SVG (Vector Master) | `review/packaging-identity-M15-M20/m15_artwork/svg_masters/gem_conditioner_ink_bilingual_A_v1.0.svg` | 13,054 B | `7c4c7174fd2e5a1a5ba9b4e85b3787d8303eac64d56e2d80abe23fb5cfc3af10` |
| **Body Wash** | PNG (Raster Texture) | `review/packaging-identity-M15-M20/m15_artwork/textures/gem_body_wash_ink_bilingual_A_v1.0.png` | 73,783 B | `06e4b3ab447b8b0de4e739617d87a568413ef0baac80eca7641f49fb4c37db94` |
| | SVG (Vector Master) | `review/packaging-identity-M15-M20/m15_artwork/svg_masters/gem_body_wash_ink_bilingual_A_v1.0.svg` | 15,834 B | `8d029f7c4946deea20c1246ebb10826b45170493d42766b0a87c62e4dbb0732c` |
| **Body Lotion** | PNG (Raster Texture) | `review/packaging-identity-M15-M20/m15_artwork/textures/gem_body_lotion_ink_bilingual_A_v1.0.png` | 70,840 B | `11e8fc08fb172d85057419530e79e6eb5c1719d9b5ab206eb629f9cb01a85a98` |
| | SVG (Vector Master) | `review/packaging-identity-M15-M20/m15_artwork/svg_masters/gem_body_lotion_ink_bilingual_A_v1.0.svg` | 15,882 B | `29c1b1690eacfef277eff8792e3ae6e0bda2cf1b4a7f419ee7838c8f6661430d` |
| **Hand Wash** | PNG (Raster Texture) | `review/packaging-identity-M15-M20/m15_artwork/textures/gem_hand_wash_ink_bilingual_A_v1.0.png` | 70,623 B | `efd4b64d611a67efb287f8c83e6d1da3b24f6177f30fb6cc75ff4e070e64c6f1` |
| | SVG (Vector Master) | `review/packaging-identity-M15-M20/m15_artwork/svg_masters/gem_hand_wash_ink_bilingual_A_v1.0.svg` | 15,871 B | `25522e58162b3c2b28864a08b68314a926b6a1c0340c1bd61401d893339ff5c6` |

---

## 7. Machine-Readable Manifests

This human-readable specification is paired with two canonical data files:
- [PRODUCT_ASSET_REGISTRY.json](file:///Users/mediacenter1/Documents/GEM-Web-remake/review/packaging-web-M33-M40-W1-W6/m33_registry/PRODUCT_ASSET_REGISTRY.json): Machine-readable JSON register with full typing, schema metadata, and 42 asset entries.
- [PRODUCT_ASSET_REGISTRY.csv](file:///Users/mediacenter1/Documents/GEM-Web-remake/review/packaging-web-M33-M40-W1-W6/m33_registry/PRODUCT_ASSET_REGISTRY.csv): Tabular dataset for spreadsheet verification and automated auditing.

All data records are cryptographically verified against on-disk files and logged in `SHA256SUMS.txt`.
