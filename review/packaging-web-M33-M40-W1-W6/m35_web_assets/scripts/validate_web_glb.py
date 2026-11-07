"""Validation script for GEM web GLBs (gem_<product>.glb).
Verifies:
1. Binary glTF magic, version 2, chunk structure (JSON + BIN)
2. File size < 1.5 MB budget
3. Polygon / triangle counts < 25,000 budget
4. Bottom-center pivot at (0,0,0) and correct metric bounding box
5. Material and texture presence (KHR_materials_transmission, label texture)
Outputs m35_web_assets/checks/validate_glb_report.json
"""
import struct
import json
import os
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
M35_DIR = os.path.dirname(HERE)
GLB_DIR = os.path.join(M35_DIR, "glb")
CHECKS_DIR = os.path.join(M35_DIR, "checks")
REPORT_PATH = os.path.join(CHECKS_DIR, "validate_glb_report.json")

PRODUCTS = ('shampoo', 'conditioner', 'body_wash', 'body_lotion', 'hand_wash')
REQUIRED_PARTS = ('glass', 'liquid', 'label', 'collar', 'stem', 'actuator', 'spout', 'dip_tube')

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def validate_glb(glb_path, prod):
    result = {
        "product": prod,
        "file": os.path.basename(glb_path),
        "status": "PASS",
        "checks": {}
    }
    
    if not os.path.isfile(glb_path):
        result["status"] = "FAIL"
        result["error"] = "File not found"
        return result
        
    size_bytes = os.path.getsize(glb_path)
    result["size_bytes"] = size_bytes
    result["size_kb"] = round(size_bytes / 1024, 1)
    result["sha256"] = sha256_file(glb_path)
    
    # Check 1: Size budget (< 1.5 MB)
    pass_size = (size_bytes < 1500000)
    result["checks"]["size_budget_lt_1_5mb"] = {
        "actual_bytes": size_bytes,
        "limit_bytes": 1500000,
        "passed": pass_size
    }
    if not pass_size:
        result["status"] = "FAIL"
        
    with open(glb_path, "rb") as f:
        data = f.read()
        
    # Check 2: Binary header
    magic, ver, total_len = struct.unpack_from('<4sII', data, 0)
    magic_ok = (magic == b'glTF')
    ver_ok = (ver == 2)
    len_ok = (total_len == size_bytes)
    result["checks"]["binary_header"] = {
        "magic": magic.decode('ascii', errors='ignore'),
        "version": ver,
        "total_length": total_len,
        "passed": (magic_ok and ver_ok and len_ok)
    }
    if not (magic_ok and ver_ok and len_ok):
        result["status"] = "FAIL"
        
    # Check 3: Chunks
    chunk0_len, chunk0_type = struct.unpack_from('<II', data, 12)
    chunk0_ok = (chunk0_type == 0x4E4F534A) # JSON
    chunk0_data = data[20 : 20 + chunk0_len]
    doc = json.loads(chunk0_data)
    
    chunk1_offset = 20 + chunk0_len
    chunk1_len, chunk1_type = struct.unpack_from('<II', data, chunk1_offset)
    chunk1_ok = (chunk1_type == 0x004E4942) # BIN
    
    result["checks"]["chunk_structure"] = {
        "json_chunk_len": chunk0_len,
        "bin_chunk_len": chunk1_len,
        "passed": (chunk0_ok and chunk1_ok)
    }
    if not (chunk0_ok and chunk1_ok):
        result["status"] = "FAIL"
        
    # Check 4: Nodes & Parts
    node_names = [n.get('name') for n in doc.get('nodes', [])]
    missing_parts = []
    for part in REQUIRED_PARTS:
        expected_node = f"GEM_{prod}_{part}"
        if expected_node not in node_names:
            missing_parts.append(expected_node)
            
    parts_ok = (len(missing_parts) == 0 and len(node_names) == 8)
    result["checks"]["product_parts"] = {
        "expected_parts_count": 8,
        "actual_parts_count": len(node_names),
        "parts_found": node_names,
        "missing_parts": missing_parts,
        "passed": parts_ok
    }
    if not parts_ok:
        result["status"] = "FAIL"
        
    # Check 5: Triangle / Polygon count from indices accessors
    total_indices = 0
    total_triangles = 0
    for m in doc.get('meshes', []):
        for p in m.get('primitives', []):
            idx = p.get('indices')
            if idx is not None:
                acc = doc['accessors'][idx]
                total_indices += acc['count']
                total_triangles += acc['count'] // 3
                
    poly_ok = (total_triangles < 25000)
    result["checks"]["polygon_budget_lt_25k"] = {
        "triangles": total_triangles,
        "indices": total_indices,
        "limit_triangles": 25000,
        "passed": poly_ok
    }
    if not poly_ok:
        result["status"] = "FAIL"
        
    # Check 6: Pivot centering & Bounding Box (transformed to world)
    # Each node has mesh with scale ~0.001 and optional translation
    mins = []
    maxs = []
    for node in doc.get('nodes', []):
        trans = node.get('translation') or [0.0, 0.0, 0.0]
        scale = node.get('scale') or [1.0, 1.0, 1.0]
        mesh_idx = node.get('mesh')
        if mesh_idx is not None:
            mesh = doc['meshes'][mesh_idx]
            for p in mesh.get('primitives', []):
                pos_idx = p['attributes']['POSITION']
                acc = doc['accessors'][pos_idx]
                # min and max in local mesh coords
                l_min = acc['min']
                l_max = acc['max']
                # transform to world coords: (local * scale) + translation
                w_min = [l_min[i] * scale[i] + trans[i] for i in range(3)]
                w_max = [l_max[i] * scale[i] + trans[i] for i in range(3)]
                mins.append(w_min)
                maxs.append(w_max)
                
    world_min = [min(m[i] for m in mins) for i in range(3)]
    world_max = [max(m[i] for m in maxs) for i in range(3)]
    
    # In GLTF Y-up: X is width, Y is height, Z is depth
    center_x = (world_min[0] + world_max[0]) / 2.0
    base_y = world_min[1]
    center_z = (world_min[2] + world_max[2]) / 2.0
    
    width = world_max[0] - world_min[0]
    height = world_max[1] - world_min[1]
    depth = world_max[2] - world_min[2]
    
    pivot_x_ok = abs(center_x) < 0.005 # centered within 5mm
    pivot_y_ok = abs(base_y) < 0.005   # base at Y=0 within 5mm
    dim_ok = (0.06 < width < 0.09) and (0.18 < height < 0.26)
    
    pivot_ok = (pivot_x_ok and pivot_y_ok and dim_ok)
    result["checks"]["pivot_and_bounds"] = {
        "world_bounds_min": [round(c, 4) for c in world_min],
        "world_bounds_max": [round(c, 4) for c in world_max],
        "center_x_m": round(center_x, 4),
        "base_y_m": round(base_y, 4),
        "center_z_m": round(center_z, 4),
        "width_m": round(width, 4),
        "height_m": round(height, 4),
        "depth_m": round(depth, 4),
        "passed": pivot_ok
    }
    if not pivot_ok:
        result["status"] = "FAIL"
        
    # Check 7: PBR Materials & Extensions
    mat_names = [m.get('name') for m in doc.get('materials', [])]
    ext_used = doc.get('extensionsUsed', [])
    trans_ok = 'KHR_materials_transmission' in ext_used
    
    # Check label texture
    has_textures = len(doc.get('textures', [])) > 0
    has_images = len(doc.get('images', [])) > 0
    
    materials_ok = (trans_ok and has_textures and has_images)
    result["checks"]["pbr_materials_and_textures"] = {
        "materials": mat_names,
        "extensions_used": ext_used,
        "has_transmission_extension": trans_ok,
        "texture_count": len(doc.get('textures', [])),
        "image_count": len(doc.get('images', [])),
        "passed": materials_ok
    }
    if not materials_ok:
        result["status"] = "FAIL"
        
    return result

def run_validation():
    os.makedirs(CHECKS_DIR, exist_ok=True)
    overall_report = {
        "milestone": "M35",
        "overall_verdict": "PASS",
        "budget_thresholds": {
            "max_file_size_bytes": 1500000,
            "max_triangles": 25000,
            "pivot_tolerance_m": 0.005
        },
        "products": {}
    }
    
    for prod in PRODUCTS:
        glb_path = os.path.join(GLB_DIR, f"gem_{prod}.glb")
        res = validate_glb(glb_path, prod)
        overall_report["products"][prod] = res
        if res["status"] != "PASS":
            overall_report["overall_verdict"] = "FAIL"
            
    with open(REPORT_PATH, "w") as f:
        json.dump(overall_report, f, indent=2)
        
    print(f"Validation complete. Overall verdict: {overall_report['overall_verdict']}")
    print(f"Report written: {REPORT_PATH}")

if __name__ == "__main__":
    run_validation()
