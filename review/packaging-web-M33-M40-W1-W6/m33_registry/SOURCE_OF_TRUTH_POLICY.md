# GEM™ Packaging & 3D Asset Source of Truth Policy (M33 Deliverable)

**Policy ID:** GEM-POL-AST-20261107-001  
**Effective Date:** 2026-11-07  
**Scope:** Packaging Identity, 3D Geometries, Render Assets, Label Artwork, and Web Pipeline Derivatives  
**Governance Authority:** GEM Program Owner  

---

## 1. Purpose and Authority

This policy defines the cryptographic and operational rules governing what constitutes the single source of truth for GEM packaging, 3D product visualizations, label artwork, and web assets. It establishes explicit protocols to prevent superseded, legacy, or unapproved assets from leaking into active design, engineering, or web staging environments.

---

## 2. Canonical vs Superseded File Register

### 2.1 3D Master Scene Files

| Canonical Asset | Path | Hash (SHA-256) | Status & Permission | Superseded Files |
|---|---|---|---|---|
| **Consolidated Visual Master** | `review/packaging-identity-M27-M32/m29_photography/scenes/GEM_M29_MASTER_UNAPPROVED.blend` | `4d5ad586be1e8dc69d8e97fa3050a269a2ce7fe7d29d03eb83ba1f6e5e12ad39` | **CANONICAL (Active Development Baseline).** Locked `0444` (read-only). | All prior `.blend` files from M10 through M28 (listed below). |

**Historical Superseded `.blend` Files (Preserved Intact as Read-Only Evidence):**
1. `review/packaging-identity-20261107/blender/scenes/GEM_packaging_ink_CONCEPT_UNAPPROVED.blend` (`0444`)
2. `review/packaging-identity-20261107/blender/scenes/GEM_packaging_clarity_ink_CONCEPT_UNAPPROVED.blend` (`0444`)
3. `review/packaging-identity-M10/blender/scenes/GEM_M10_bilingual_ink_CONCEPT_UNAPPROVED.blend` (`0444`)
4. `review/packaging-identity-M11-M14/blender/scenes/GEM_M13_bilingual_ink_CONCEPT_UNAPPROVED.blend` (`0444`)
5. `review/packaging-identity-M14-1/blender/scenes/GEM_M14_1_working_copy_UNAPPROVED.blend` (`0444`)
6. `review/packaging-identity-M15-M20/m16_geometry/blender/scenes/GEM_M16_baseline_copy_UNAPPROVED.blend` (`0444`)
7. `review/packaging-identity-M15-M20/m16_geometry/blender/scenes/GEM_M16_geometry_UNAPPROVED.blend` (`0444`)
8. `review/packaging-identity-M15-M20/m17_materials/scenes/GEM_M17_materials_UNAPPROVED.blend` (`0444`)
9. `review/packaging-identity-M21-M26/m22_materials/scenes/GEM_M22_materials_UNAPPROVED.blend` (`0444`)
10. `review/packaging-identity-M21-M26/m23_photography/scenes/GEM_M23_photography_UNAPPROVED.blend` (`0444`)
11. `review/packaging-identity-M27-M32/m27_geometry/blender/scenes/GEM_M27_geometry_UNAPPROVED.blend` (Superseded by M29 integration)
12. `review/packaging-identity-M27-M32/m28_materials/scenes/GEM_M28_materials_UNAPPROVED.blend` (Superseded by M29 integration)

### 2.2 Front-Label Graphic Artwork

| Canonical Asset | Path | Status | Verification Authority |
|---|---|---|---|
| **5x Approved Front-Label PNG Textures** | `review/packaging-identity-M15-M20/m15_artwork/textures/gem_*_ink_bilingual_A_v1.0.png` | **CANONICAL** | Owner Authorizations `-001`, `-002`, `-003` |
| **5x Canonical SVG Vector Masters** | `review/packaging-identity-M15-M20/m15_artwork/svg_masters/gem_*_ink_bilingual_A_v1.0.svg` | **CANONICAL** | Generated via `build_labels_m15.py` |
| **Historical Label Concepts** | Any label graphic in `review/packaging-identity-20261107/` or pre-M15 directories | **SUPERSEDED** | Do not reference or render |

### 2.3 Product Visualization Imagery

| Canonical Asset | Path | Status | Authorized Use Scope |
|---|---|---|---|
| **13 M29 Final CGI Renders** | `review/packaging-identity-M27-M32/m29_photography/renders/final/*.png` | **CANONICAL** | Approved for internal development & staging prototypes under Authorization A (`GEM-PKG-OWNER-20261107-004`). |
| **M17, M22, M23 Draft Renders** | Draft render folders in M17, M22, M23 | **SUPERSEDED** | Superseded by M29 256 spp final batch. |

---

## 3. Filesystem Security & Read-Only Protections (`0444`)

1. **Strict Immutability of Milestone Archives:**
   - All directories matching `review/packaging-identity-*` are permanently frozen. No agent, script, or automated tool may create, modify, overwrite, or delete files in these paths.
   - All `.blend` scene files are locked to permission mode `0444` (`chmod 0444`).
2. **Non-Destructive Working Copy Discipline:**
   - Active modeling and scene development must occur in authorized, milestone-specific output folders (e.g. `review/packaging-web-M33-M40-W1-W6/m34_five_product_3d/scenes/`).
   - Working copies must explicitly append `_UNAPPROVED.blend` until formal owner milestone sign-off.
3. **No Direct Overwriting of Master Scenes:**
   - If changes to the canonical master are required, they must be committed as a new versioned milestone artifact (e.g., M34 master) with accompanying hash verification and ledger updates.

---

## 4. Pipeline Ingestion & Anti-Leakage Safeguards

### Rule 1: Legacy Scene Mesh Quarantine
- Inside `GEM_M29_MASTER_UNAPPROVED.blend`, ten legacy campaign scenes (`00_Contact_Sheet`, `Scene`, `Scene.001`, `02_Hotel_Suite`, `04_Editorial_Still_Life`, `05_Product_Collection`, `Campaign_Night_Service`, `Study_Arrival_Cut`, `Product_Lookdev`, `SAND3D_Pilot`) contain pre-M16 bottle meshes.
- **Enforcement:** Export scripts and GLB converters must validate object provenance. Attempting to export geometry from any legacy scene or collection named `S1 Products` through `S5 Products` will abort the build process.

### Rule 2: Architectural Set Isolation
- Scene `03_Premium_Bathroom` is an architectural donor set only. While its stone basin, mirror, and light elements are linked into `M23_Bathroom_Editorial`, its product collection must remain isolated. Only canonical `GEM_S3D_shampoo` and `GEM_S3D_conditioner` collections may be rendered.

### Rule 3: Exploratory 3D Geometry Quarantine (M34 Scope)
- 3D models developed for Body Wash, Body Lotion, and Hand Wash under Authorization B (`GEM-PKG-OWNER-20261107-005`) are classified strictly as `PROVISIONAL_EXPLORATORY_GEOMETRY_M34`.
- **Enforcement:** These meshes must embed custom metadata in exported GLTF/GLB files: `GEM_GEOMETRY_STATUS: PROVISIONAL_EXPLORATORY_GEOMETRY_M34`. They must never be displayed as certified physical products.

### Rule 4: Commercial Misrepresentation Prohibition
- No CGI render, 3D model, or prototype screenshot may be labelled as "commercial photography", "final product specifications", or "factory drawings".
- All user-facing staging environments must maintain the classification: `INTERNAL_DEVELOPMENT_AND_STAGING_ONLY_NOT_COMMERCIAL`.

### Rule 5: Production Deployment Gate (Website)
- Under Owner Authorization E (`GEM-WEB-OWNER-20261107-008`), digital transformation assets are authorized strictly for design, development, and staging on branch `development/website-transformation-w1-w6-20261107`.
- **Enforcement:** No pipeline script or agent may push to `main`, configure production CDN endpoints, or alter live DNS records without separate written owner authorization.
