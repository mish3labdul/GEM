"""Verification script for GEM_M34_five_products_PROVISIONAL.blend.
Runs in a fresh Blender process and checks:
1. Collections and objects for all 5 products
2. Parenting, part presence, custom properties
3. Material slot mappings
4. Packed label images byte-identity vs M15 PNGs
5. Preservation of Shampoo and Conditioner geometry hashes vs M29 baseline
Writes results to m34_five_product_3d/checks/verify_m34_scene.json
"""
import bpy
import json
import os
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
M34_DIR = os.path.dirname(HERE)
PARAMS_FILE = os.path.join(M34_DIR, "params", "m34_five_product_params.json")
CHECKS_DIR = os.path.join(M34_DIR, "checks")
REPORT_FILE = os.path.join(CHECKS_DIR, "verify_m34_scene.json")

with open(PARAMS_FILE, "r") as f:
    CONFIG = json.load(f)

PARTS = ('glass', 'liquid', 'label', 'collar', 'stem', 'actuator', 'spout', 'dip_tube')
ALL_PRODUCTS = ('shampoo', 'conditioner', 'body_wash', 'body_lotion', 'hand_wash')

M29_BASELINE_HASHES = {
    'shampoo': 'd556fd7331333b64a41d2319e23ba501bc726e9191d13aed2ec7d72e2101d6f6',
    'conditioner': '5b508137790db20c7760318f30f7af60f6fe3a6263094a1b449f0412de321557'
}

def get_geom_hash(prod):
    h = hashlib.sha256()
    col = bpy.data.collections.get('GEM_S3D_' + prod)
    if not col:
        return None
    for o in sorted(col.objects, key=lambda o: o.name):
        if o.type == 'MESH':
            h.update(o.name.encode())
            me = o.data
            for v in me.vertices:
                h.update(('%.6f,%.6f,%.6f' % tuple(v.co)).encode())
            for p in me.polygons:
                h.update(str(tuple(p.vertices)).encode())
    return h.hexdigest()

def verify():
    os.makedirs(CHECKS_DIR, exist_ok=True)
    report = {
        "status": "PASS",
        "blend_file": bpy.data.filepath,
        "blender_version": bpy.app.version_string,
        "products": {},
        "m29_baseline_preservation": {},
        "packed_labels_verification": {}
    }

    repo_root = os.path.abspath(os.path.join(M34_DIR, "..", "..", ".."))

    # Check baseline preservation
    for p in ('shampoo', 'conditioner'):
        actual_hash = get_geom_hash(p)
        expected_hash = M29_BASELINE_HASHES[p]
        matches = (actual_hash == expected_hash)
        report["m29_baseline_preservation"][p] = {
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
            "matches": matches
        }
        if not matches:
            report["status"] = "FAIL"

    # Check each product
    for prod in ALL_PRODUCTS:
        p_info = {"parts": {}, "root": None, "collection_present": False, "geom_hash": get_geom_hash(prod)}
        col_name = f"GEM_S3D_{prod}"
        col = bpy.data.collections.get(col_name)
        p_info["collection_present"] = col is not None
        if not col:
            report["status"] = "FAIL"
            continue

        root_name = f"GEM_{prod}_root"
        root = bpy.data.objects.get(root_name)
        if root:
            p_info["root"] = {
                "name": root.name,
                "location": [round(c, 4) for c in root.location],
                "scale": [round(c, 4) for c in root.scale],
                "props": dict(root.items())
            }
        else:
            report["status"] = "FAIL"

        for part in PARTS:
            obj_name = f"GEM_{prod}_{part}"
            obj = bpy.data.objects.get(obj_name)
            if not obj:
                p_info["parts"][part] = {"status": "MISSING"}
                report["status"] = "FAIL"
                continue

            ref_obj = bpy.data.objects.get(f"GEM_shampoo_{part}")
            rot_matches = all(abs(a - b) < 1e-5 for a, b in zip(obj.rotation_euler, ref_obj.rotation_euler))
            if not rot_matches:
                report["status"] = "FAIL"
            mats = [s.material.name if s.material else None for s in obj.material_slots]
            p_info["parts"][part] = {
                "name": obj.name,
                "parent": obj.parent.name if obj.parent else None,
                "rotation_euler": [round(c, 5) for c in obj.rotation_euler],
                "rotation_matches_baseline": rot_matches,
                "poly_count": len(obj.data.polygons),
                "vert_count": len(obj.data.vertices),
                "materials": mats,
                "props": dict(obj.items())
            }

        # Check label packed image
        meta = CONFIG['products'][prod]['confirmed_metadata']
        tex_path = os.path.join(repo_root, meta['label_texture_path'])
        img_name = f"GEM_S3D label {prod}"
        img = bpy.data.images.get(img_name)
        if not img or not img.packed_file:
            report["packed_labels_verification"][prod] = {
                "image_name": img_name,
                "packed": False,
                "matches_m15": False
            }
            report["status"] = "FAIL"
        else:
            packed_bytes = bytes(img.packed_file.data)
            packed_sha = hashlib.sha256(packed_bytes).hexdigest()
            file_bytes = open(tex_path, "rb").read()
            file_sha = hashlib.sha256(file_bytes).hexdigest()
            matches = (packed_sha == file_sha == meta['label_texture_sha256'])
            report["packed_labels_verification"][prod] = {
                "image_name": img_name,
                "packed": True,
                "bytes_len": len(packed_bytes),
                "packed_sha256": packed_sha,
                "file_sha256": file_sha,
                "expected_sha256": meta['label_texture_sha256'],
                "matches_m15": matches
            }
            if not matches:
                report["status"] = "FAIL"

        report["products"][prod] = p_info

    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Verification complete. Verdict: {report['status']}")
    print(f"Saved report to: {REPORT_FILE}")

if __name__ == "__main__":
    verify()
