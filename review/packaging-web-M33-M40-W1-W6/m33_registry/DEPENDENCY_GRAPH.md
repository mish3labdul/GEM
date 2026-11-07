# GEM™ Asset Pipeline Dependency Graph (M33 Deliverable)

**Document Version:** 1.0  
**Release Date:** 2026-11-07  
**Scope:** M15 Artwork to M29 Master Scene, M34 Expansion, M35 3D/Static Pipeline, and W1–W6 Digital Staging  

---

## 1. End-to-End Asset Lineage & Dependency Flowchart

The following flowchart illustrates the strict unidirectional dependency flow across all packaging milestones, from approved typography and vector masters to web deployment:

```mermaid
flowchart TD
    subgraph S_M15["M15: Artwork & Typography (Approved)"]
        A_FONTS["Jost Regular & Noto Sans Arabic"]
        A_AUTH["Authorizations -001, -002, -003"]
        A_BUILD["build_labels_m15.py (HarfBuzz exact)"]
        A_SVG["5x SVG Masters (v1.0)"]
        A_PNG["5x PNG Textures (1356x2000 px)"]
        A_FONTS --> A_BUILD
        A_AUTH --> A_BUILD
        A_BUILD --> A_SVG
        A_BUILD --> A_PNG
    end

    subgraph S_M27["M27a: Provisional 3D Geometry"]
        G_REF["Concept Silhouette Photo Reference"]
        G_MESH["Provisional M27a Meshes (Shampoo & Conditioner)"]
        G_GAP["78 Missing / 21 Provisional Dimensions"]
        G_REF --> G_MESH
        G_GAP -.-> G_MESH
    end

    subgraph S_M28["M28: Calibrated Cycles Materials"]
        M_AMBER["GEM_M17 Amber Glass Shader"]
        M_LIQUID["GEM_M17 Amber Liquid Shader"]
        M_PUMP["GEM_M17 Pump Head, Collar & Stem Shaders"]
        M_LBL["GEM_S3D Label Artwork Shaders"]
        A_PNG --> M_LBL
    end

    subgraph S_M29["M29: Consolidated Master Baseline (Auth A)"]
        B_MASTER["GEM_M29_MASTER_UNAPPROVED.blend (0444 Read-Only)"]
        B_SCN_M8["M8_Lookdev Scene (Active Studio)"]
        B_SCN_M23["M23_Bathroom_Editorial Scene (Active Editorial)"]
        B_DONOR["03_Premium_Bathroom Scene (Donor Set)"]
        B_LEGACY["10 Preserved Legacy Scenes (pre-M16 DO NOT USE)"]
        R_13["13 Verified CGI Renders (256 spp Cycles)"]

        G_MESH --> B_MASTER
        M_AMBER --> B_MASTER
        M_LIQUID --> B_MASTER
        M_PUMP --> B_MASTER
        M_LBL --> B_MASTER

        B_MASTER --> B_SCN_M8
        B_MASTER --> B_SCN_M23
        B_MASTER --> B_DONOR
        B_MASTER --> B_LEGACY
        B_SCN_M8 --> R_13
        B_SCN_M23 --> R_13
    end

    subgraph S_M34["M34: 5-Product 3D Geometry Expansion (Auth B)"]
        E_AUTH["GEM-PKG-OWNER-20261107-005 (Auth B)"]
        E_3D["Exploratory Models: Body Wash, Lotion, Hand Wash"]
        E_COLLECT["GEM_M34_five_product_collection_UNAPPROVED.blend"]
        
        B_MASTER --> E_COLLECT
        E_AUTH --> E_COLLECT
        A_PNG --> E_COLLECT
        E_COLLECT --> E_3D
    end

    subgraph S_M35["M35: Web Asset Optimization & GLB Pipeline"]
        W_GLB["Three.js Optimized GLB / GLTF Models (Draco / KTX2)"]
        W_IMG["WebP / AVIF Responsive Image Formats (1x / 2x / 3x)"]
        W_POST["Web Editorial Crop Variants (Square, Hero 16:9, Mobile 4:5)"]
        
        R_13 --> W_IMG
        R_13 --> W_POST
        E_COLLECT --> W_GLB
        B_MASTER --> W_GLB
    end

    subgraph S_WEB["W1–W6: Digital Transformation Staging (Auth E)"]
        WEB_STAGE["Isolated Branch: development/website-transformation-w1-w6-20261107"]
        WEB_3D["Interactive WebGL / Three.js Bottle Customizer"]
        WEB_CATALOG["High-DPI Responsive Product Showcase & Editorial Lookbook"]
        WEB_PREVIEW["Local Preview Loopback: port 4173 (serve.py)"]

        W_GLB --> WEB_3D
        W_IMG --> WEB_CATALOG
        W_POST --> WEB_CATALOG
        WEB_3D --> WEB_STAGE
        WEB_CATALOG --> WEB_STAGE
        WEB_STAGE --> WEB_PREVIEW
    end

    classDef approved fill:#e6f4ea,stroke:#137333,stroke-width:2px;
    classDef provisional fill:#fef7e0,stroke:#b06000,stroke-width:2px;
    classDef legacy fill:#fce8e6,stroke:#c5221f,stroke-width:2px;
    classDef web fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px;

    class A_FONTS,A_AUTH,A_BUILD,A_SVG,A_PNG approved;
    class G_MESH,M_AMBER,M_LIQUID,M_PUMP,M_LBL,B_MASTER,B_SCN_M8,B_SCN_M23,R_13,E_3D,E_COLLECT provisional;
    class B_DONOR,B_LEGACY legacy;
    class W_GLB,W_IMG,W_POST,WEB_STAGE,WEB_3D,WEB_CATALOG,WEB_PREVIEW web;
```

---

## 2. Cryptographic Integrity and Pipeline Gates

| Pipeline Transition | Input Hashes / Artifacts | Output Hashes / Artifacts | Verification Gate & Status |
|---|---|---|---|
| **M15 → M28 Label Integration** | `textures/*.png` (`4a0942...`, `3f8048...`) | `GEM_M28_materials_UNAPPROVED.blend` | Direct node image packing; byte hashes identical (`verify_master.json`: `equal: true`). |
| **M27a + M28 → M29 Master Scene** | `GEM_M27_geometry_UNAPPROVED.blend`<br>`GEM_M28_materials_UNAPPROVED.blend` | `GEM_M29_MASTER_UNAPPROVED.blend`<br>`4d5ad586be1e8dc69d8e97fa3050a269a2ce7fe7d29d03eb83ba1f6e5e12ad39` | Executed via fresh Blender process; mesh vertices and material node-trees match exactly. Master blend locked `0444`. |
| **M29 Master → 13 Final CGI Renders** | Master `.blend` + embedded runner `M29_render.py` | 13 PNG images in `renders/final/*.png` | 256 spp Cycles render; verified against downsampled smoke test (`AB_master_smoke_vs_final.png` MAE 0.615–1.807 < 6.0 threshold). |
| **M29 Master → M34 5-Product 3D** | Master `.blend` + Owner Authorization B (`GEM-PKG-OWNER-20261107-005`) | `GEM_M34_five_product_collection_UNAPPROVED.blend` | Copies calibrated materials and donor geometry; attaches approved M15 labels for Body Wash, Lotion, Hand Wash. Classified as `PROVISIONAL_EXPLORATORY_GEOMETRY_M34`. |
| **M29 / M34 → M35 Web Assets** | 13 Final PNGs + 3D Product Collections | Optimized WebP/AVIF images + Draco-compressed GLB models | Automated asset pipeline generates responsive WebP/AVIF breakpoints and web-ready PBR GLB files. |
| **M35 → W1–W6 Website Staging** | Optimized GLB models + responsive images | Local preview server (`localhost:4173`) | Deployed exclusively on branch `development/website-transformation-w1-w6-20261107`. No production deployment without owner sign-off. |

---

## 3. Exclusion Boundaries

1. **Legacy Mesh Quarantine:** Scenes `00_Contact_Sheet`, `Scene`, `Scene.001`, `02_Hotel_Suite`, `04_Editorial_Still_Life`, `05_Product_Collection`, `Campaign_Night_Service`, `Study_Arrival_Cut`, `Product_Lookdev`, and `SAND3D_Pilot` are quarantined. Any pipeline tool reading mesh datablocks from these scenes will trigger a build error.
2. **Donor Scene Read-Only Isolation:** Scene `03_Premium_Bathroom` is referenced strictly as an architectural set donor. Its internal `S3 Products` collection must never be unlinked or substituted for production rendering.
3. **Exploratory Geometry Boundary:** Geometry created in M34 must remain explicitly tagged as `PROVISIONAL_EXPLORATORY_GEOMETRY_M34` in all GLTF metadata and manifest entries.
