# M35 Milestone Report: Blender-to-Web Asset Optimization

**Milestone:** M35 (Track A — Packaging & 3D Asset System)  
**Date:** 2026-11-07  
**Authorization:** Authorization B (`GEM-PKG-OWNER-20261107-005`)  
**Accountable Engineer:** Blender/3D Asset & Web GLTF Pipeline Engineer (Pro tier)  
**Technical Verdict:** `PASS` (All models and plates verified within budgets)

---

## 1. Executive Summary

Milestone M35 delivers the automated, repeatable Blender-to-Web GLTF/GLB export and optimization pipeline for all five GEM™ products. The pipeline converts the high-polygon Cycles studio master scene into ultra-compact, high-fidelity real-time 3D assets specifically engineered for 60 fps Three.js WebGL execution across mobile, tablet, and desktop viewports.

### Key Optimization Metrics Achieved:

| Target Parameter | Web Budget / Limit | Achieved Result | Margin / Status |
|---|---|---|---|
| **Polygon / Triangle Count** | `< 25,000` triangles | **20,460 triangles** | **-18.2% under budget (PASS)** |
| **GLB File Size** | `< 1,500 KB` (< 1.5 MB) | **699.5 KB – 709.8 KB** | **-52.7% under budget (PASS)** |
| **Pivot Placement** | Bottom-Center `(0, 0, 0)` | **X=0.000m, Y=0.000m, Z=0.0002m** | **Exact Centering (PASS)** |
| **Realtime Transmission** | `KHR_materials_transmission` | **Active on Glass & Liquid** | **Standard Three.js Physical Material (PASS)** |
| **Label Resolution & Integrity** | Approved M15 Texture | **Crisp 1356x2000 Embedded** | **Zero z-fighting, clean UVs (PASS)** |
| **Static Fallback Plates** | WebP + PNG pairs | **11 WebP (17–60 KB) + 11 PNG** | **Ultra-lightweight fallback (PASS)** |

---

## 2. Web GLB Asset Inventory (`m35_web_assets/glb/`)

All five GLBs are self-contained binary glTF 2.0 containers with embedded geometry buffers and packed textures (zero external HTTP requests required):

| Product | GLB Filename | Triangles | File Size (Bytes) | Size (KB) | SHA-256 Checksum | Three.js Materials |
|---|---|---|---|---|---|---|
| `shampoo` | `gem_shampoo.glb` | 20,460 | 717,164 | 700.4 KB | `e1182e42d04ce613...` | Amber Glass, Liquid, Satin Pump, Label |
| `conditioner` | `gem_conditioner.glb` | 20,460 | 716,320 | 699.5 KB | `44df10b3151de490...` | Amber Glass, Liquid, Satin Pump, Label |
| `body_wash` | `gem_body_wash.glb` | 20,460 | 726,876 | 709.8 KB | `b83fea548b9e0603...` | Amber Glass, Liquid, Satin Pump, Label |
| `body_lotion` | `gem_body_lotion.glb` | 20,460 | 723,968 | 707.0 KB | `de0da50ae0753954...` | Amber Glass, Liquid, Satin Pump, Label |
| `hand_wash` | `gem_hand_wash.glb` | 20,460 | 723,716 | 706.8 KB | `f123f01dfc6f647f...` | Amber Glass, Liquid, Satin Pump, Label |

---

## 3. Polygon Allocation per Part

The decimation strategy selectively reduces high-density cylindrical sweeps while strictly preserving the front label's curvature and UV continuity:

| Part Name | Raw Studio Polys | Web Decimate Ratio | Web Polygons | Role & Quality Rationale |
|---|---|---|---|---|
| `glass` | 133,920 | 0.08 | 10,713 | Retains smooth cylindrical profile and inner liquid interface |
| `liquid` | 34,920 | 0.08 | 2,793 | Internal meniscus volume for amber depth shading |
| `collar` | 22,680 | 0.08 | 1,814 | Threaded pump collar silhouette |
| `stem` | 4,954 | 0.15 | 742 | Vertical dispenser stem |
| `actuator` | 12,960 | 0.10 | 1,347 | Ergonomic pump head contour |
| `spout` | 17,030 | 0.10 | 1,703 | Curved dispenser spout and orifice |
| `dip_tube` | 188 | 1.00 | 188 | Lightweight internal dip tube |
| `label` | 1,160 | 1.00 | 1,160 | **100% pristine:** no vertex decimation to preserve UVs and prevent text warping |
| **Total** | **227,892** | — | **20,460** | **-91.0% polygon reduction vs studio master** |

---

## 4. Web Material Architecture for Three.js

When loaded via Three.js `GLTFLoader`, the models cleanly instantiate standard PBR materials:
1. **Amber Glass (`GEM_WEB_amber_glass`):**
   - `transmission: 1.0` via `KHR_materials_transmission`
   - `ior: 1.50` via `KHR_materials_ior`
   - `roughness: 0.04`
   - `color: #6B3812` (rich amber absorption tint)
2. **Amber Liquid Fill (`GEM_WEB_amber_liquid`):**
   - `transmission: 0.70`
   - `ior: 1.36`
   - `roughness: 0.08`
   - `color: #7A3F0D` (dense amber core)
3. **Satin Black Pump (`GEM_WEB_pump_satin`):**
   - `roughness: 0.45`
   - `metalness: 0.10`
   - `color: #040404` (deep satin architectural black)
4. **Front Label Panel (`GEM_WEB_label_<product>`):**
   - `map`: Crisp bilingual front label texture (M15 Layout A)
   - `roughness: 0.70`
   - Offset proud (`50 μm`) over glass to eliminate z-fighting in WebGL depth buffers.

---

## 5. Static Fallback Plates (`m35_web_assets/plates/`)

To support environments where WebGL is disabled, mobile low-power/battery-saver modes are active, or the user has enabled `prefers-reduced-motion`, 11 responsive fallback plate pairs were generated:

| Plate Key | Visual Context / Role | Dimensions | WebP Size | PNG Size | WebP Savings |
|---|---|---|---|---|---|
| `gem_shampoo_hero` | Interactive 3D Viewer Fallback (Shampoo) | 1280 x 1600 | 21.4 KB | 1.36 MB | 98.4% |
| `gem_conditioner_hero` | Interactive 3D Viewer Fallback (Conditioner) | 1280 x 1600 | 21.2 KB | 1.36 MB | 98.4% |
| `gem_body_wash_hero` | Interactive 3D Viewer Fallback (Body Wash) | 960 x 1200 | 17.4 KB | 757 KB | 97.7% |
| `gem_body_lotion_hero` | Interactive 3D Viewer Fallback (Body Lotion) | 960 x 1200 | 17.6 KB | 757 KB | 97.7% |
| `gem_hand_wash_hero` | Interactive 3D Viewer Fallback (Hand Wash) | 960 x 1200 | 17.4 KB | 757 KB | 97.7% |
| `gem_family_five_lineup` | Master 5-Product Hospitality Lineup | 2000 x 1125 | 53.4 KB | 1.54 MB | 96.5% |
| `gem_family_pair` | Shampoo & Conditioner Suite Plate | 2000 x 1250 | 38.1 KB | 1.72 MB | 97.8% |
| `gem_bathroom_editorial` | Limestone Niche Architectural Editorial | 2000 x 1250 | 60.3 KB | 1.91 MB | 96.8% |
| `gem_editorial_window` | Morning Aperture Editorial | 2000 x 1250 | 48.9 KB | 1.92 MB | 97.5% |
| `gem_catalog_light_shampoo` | E-Commerce Studio White Sweep (Shampoo) | 1280 x 1600 | 24.7 KB | 1.41 MB | 98.2% |
| `gem_catalog_light_conditioner` | E-Commerce Studio White Sweep (Conditioner) | 1280 x 1600 | 23.6 KB | 1.41 MB | 98.3% |

---

## 6. Automated Validation Results (`checks/validate_glb_report.json`)

Automated validation verified all five GLB assets against the program's strict runtime thresholds:
- **glTF Binary Header & Chunk Structure:** `PASS` (Magic `glTF`, version 2, JSON chunk + BIN chunk verified).
- **Part Completeness:** `PASS` (All 8 parts present in every file).
- **Triangle Budget:** `PASS` (20,460 < 25,000 threshold).
- **File Size Budget:** `PASS` (~700 KB < 1,500 KB threshold).
- **Pivot Centering:** `PASS` (Bottom-center resting on Y=0.000m, vertical cylinder axis centered at X=0.000m, Z=0.0002m).
- **Materials & Extensions:** `PASS` (`KHR_materials_transmission` active, embedded textures verified).
- **Overall Pipeline Verdict:** `PASS`.
