"""Generate web static fallback plates (WebP + PNG) from M29 finals and M34 renders.
Serves no-WebGL, mobile battery-saver, and prefers-reduced-motion fallbacks.
Writes plates to m35_web_assets/plates/ and manifest to plates_manifest.json.
"""
from PIL import Image
import os
import json
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
M35_DIR = os.path.dirname(HERE)
PLATES_DIR = os.path.join(M35_DIR, "plates")
M34_RENDERS = os.path.join(M35_DIR, "..", "m34_five_product_3d", "renders")
M29_FINALS = os.path.join(M35_DIR, "..", "..", "packaging-identity-M27-M32", "m29_photography", "renders", "final")

os.makedirs(PLATES_DIR, exist_ok=True)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

PLATE_SOURCES = [
    # 5 Products - Studio Hero Fallbacks
    {
        "key": "gem_shampoo_hero",
        "source": os.path.join(M29_FINALS, "hero_shampoo.png"),
        "fallback_source": os.path.join(M34_RENDERS, "studio_shampoo.png"),
        "role": "Single product interactive viewer fallback (Shampoo)",
        "product": "shampoo",
        "category": "hero_fallback",
        "max_dim": 1600
    },
    {
        "key": "gem_conditioner_hero",
        "source": os.path.join(M29_FINALS, "hero_conditioner.png"),
        "fallback_source": os.path.join(M34_RENDERS, "studio_conditioner.png"),
        "role": "Single product interactive viewer fallback (Conditioner)",
        "product": "conditioner",
        "category": "hero_fallback",
        "max_dim": 1600
    },
    {
        "key": "gem_body_wash_hero",
        "source": os.path.join(M34_RENDERS, "studio_body_wash.png"),
        "fallback_source": None,
        "role": "Single product interactive viewer fallback (Body Wash)",
        "product": "body_wash",
        "category": "hero_fallback",
        "max_dim": 1600
    },
    {
        "key": "gem_body_lotion_hero",
        "source": os.path.join(M34_RENDERS, "studio_body_lotion.png"),
        "fallback_source": None,
        "role": "Single product interactive viewer fallback (Body Lotion)",
        "product": "body_lotion",
        "category": "hero_fallback",
        "max_dim": 1600
    },
    {
        "key": "gem_hand_wash_hero",
        "source": os.path.join(M34_RENDERS, "studio_hand_wash.png"),
        "fallback_source": None,
        "role": "Single product interactive viewer fallback (Hand Wash)",
        "product": "hand_wash",
        "category": "hero_fallback",
        "max_dim": 1600
    },
    # Multi-product scene plates
    {
        "key": "gem_family_five_lineup",
        "source": os.path.join(M34_RENDERS, "family_five_lineup.png"),
        "fallback_source": None,
        "role": "Master five-product hospitality amenity collection hero",
        "product": "all_five",
        "category": "scene_hero",
        "max_dim": 2000
    },
    {
        "key": "gem_family_pair",
        "source": os.path.join(M29_FINALS, "family_pair.png"),
        "fallback_source": None,
        "role": "Shampoo and Conditioner paired hospitality suite plate",
        "product": "shampoo_conditioner_pair",
        "category": "scene_hero",
        "max_dim": 2000
    },
    {
        "key": "gem_bathroom_editorial",
        "source": os.path.join(M29_FINALS, "bathroom_editorial.png"),
        "fallback_source": None,
        "role": "Limestone niche bathroom editorial hero plate",
        "product": "hospitality_bathroom",
        "category": "architectural_editorial",
        "max_dim": 2000
    },
    {
        "key": "gem_editorial_window",
        "source": os.path.join(M29_FINALS, "editorial_window.png"),
        "fallback_source": None,
        "role": "Morning aperture window editorial plate",
        "product": "hospitality_window",
        "category": "architectural_editorial",
        "max_dim": 2000
    },
    # Catalog light background plates
    {
        "key": "gem_catalog_light_shampoo",
        "source": os.path.join(M29_FINALS, "catalog_light_shampoo.png"),
        "fallback_source": None,
        "role": "Clean light ecommerce catalog presentation (Shampoo)",
        "product": "shampoo",
        "category": "catalog_light",
        "max_dim": 1600
    },
    {
        "key": "gem_catalog_light_conditioner",
        "source": os.path.join(M29_FINALS, "catalog_light_conditioner.png"),
        "fallback_source": None,
        "role": "Clean light ecommerce catalog presentation (Conditioner)",
        "product": "conditioner",
        "category": "catalog_light",
        "max_dim": 1600
    }
]

def build_plates():
    manifest = {
        "milestone": "M35",
        "authorization": "GEM-PKG-OWNER-20261107-005",
        "purpose": "Web static fallback plates (no-WebGL, mobile battery-saver, prefers-reduced-motion)",
        "plates": []
    }
    
    for item in PLATE_SOURCES:
        src = item["source"]
        if not os.path.isfile(src) and item["fallback_source"]:
            src = item["fallback_source"]
            
        if not os.path.isfile(src):
            print(f"Warning: Source not found for {item['key']}: {src}")
            continue
            
        im = Image.open(src)
        w, h = im.size
        
        # Scale if larger than max_dim
        max_d = item.get("max_dim", 2000)
        if max(w, h) > max_d:
            scale = max_d / max(w, h)
            nw = int(round(w * scale))
            nh = int(round(h * scale))
            im_scaled = im.resize((nw, nh), Image.Resampling.LANCZOS)
        else:
            nw, nh = w, h
            im_scaled = im
            
        out_webp = os.path.join(PLATES_DIR, f"{item['key']}.webp")
        out_png = os.path.join(PLATES_DIR, f"{item['key']}.png")
        
        # Save WebP (Quality 90, method 6)
        im_scaled.save(out_webp, "WEBP", quality=90, method=6)
        webp_bytes = os.path.getsize(out_webp)
        webp_sha = sha256_file(out_webp)
        
        # Save PNG (Optimized)
        im_scaled.save(out_png, "PNG", optimize=True)
        png_bytes = os.path.getsize(out_png)
        png_sha = sha256_file(out_png)
        
        print(f"Generated {item['key']}: {nw}x{nh} -> WebP {webp_bytes/1024:.1f} KB, PNG {png_bytes/1024:.1f} KB")
        
        manifest["plates"].append({
            "key": item["key"],
            "role": item["role"],
            "product": item["product"],
            "category": item["category"],
            "dimensions": [nw, nh],
            "source_path": os.path.relpath(src, M35_DIR),
            "webp": {
                "file": f"{item['key']}.webp",
                "bytes": webp_bytes,
                "sha256": webp_sha
            },
            "png": {
                "file": f"{item['key']}.png",
                "bytes": png_bytes,
                "sha256": png_sha
            }
        })
        
    manifest_path = os.path.join(PLATES_DIR, "plates_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"\nPlates generated: {len(manifest['plates'])}. Manifest: {manifest_path}")

if __name__ == "__main__":
    build_plates()
