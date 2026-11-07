"""Render M34 deliverables on Metal GPU:
1. Five individual studio hero preview renders (studio_<product>.png, 960x1200, 64 spp)
2. Five-product hospitality lineup render (family_five_lineup.png, 2000x1125, 96 spp)
Records render report JSON in m34_five_product_3d/renders/render_report.json
"""
import bpy
import os
import time
import math
import hashlib
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
M34_DIR = os.path.dirname(HERE)
RENDERS_DIR = os.path.join(M34_DIR, "renders")
REPORT_PATH = os.path.join(RENDERS_DIR, "render_report.json")

PRODUCTS = ('shampoo', 'conditioner', 'body_wash', 'body_lotion', 'hand_wash')
POSITIONS = {
    'hand_wash': -0.18,
    'shampoo': -0.09,
    'conditioner': 0.00,
    'body_wash': 0.09,
    'body_lotion': 0.18
}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def setup_metal_gpu(sc):
    sc.cycles.device = 'GPU'
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'METAL'
        prefs.get_devices()
        for d in prefs.devices:
            d.use = (d.type == 'METAL')
        print("Configured Metal GPU device successfully.")
    except Exception as e:
        print("Note on GPU setup:", e)

def render_all():
    os.makedirs(RENDERS_DIR, exist_ok=True)
    sc = bpy.data.scenes.get('M8_Lookdev')
    if not sc:
        raise RuntimeError("Scene M8_Lookdev not found!")
    
    setup_metal_gpu(sc)
    report = {
        "milestone": "M34",
        "authorization": "GEM-PKG-OWNER-20261107-005",
        "renders": []
    }
    
    hero_cam = bpy.data.objects.get('M29 cam hero_shampoo')
    if not hero_cam:
        raise RuntimeError("Hero camera not found!")
    
    # 1. Render Individual Studio Heroes
    for prod in PRODUCTS:
        out_path = os.path.join(RENDERS_DIR, f"studio_{prod}.png")
        print(f"\n--- Rendering studio hero for {prod} -> {out_path} ---")
        
        # Position active product at origin, hide others
        for p in PRODUCTS:
            col = bpy.data.collections.get(f"GEM_S3D_{p}")
            if p == prod:
                col.hide_render = False
                bpy.data.objects[f"GEM_{p}_root"].location = (0.0, 0.0, 0.0)
            else:
                col.hide_render = True
                
        sc.camera = hero_cam
        sc.render.resolution_x = 960
        sc.render.resolution_y = 1200
        sc.render.resolution_percentage = 100
        sc.cycles.samples = 64
        sc.render.filepath = out_path
        
        bpy.context.view_layer.update()
        t0 = time.time()
        bpy.ops.render.render(write_still=True, scene=sc.name)
        dt = round(time.time() - t0, 2)
        
        file_bytes = os.path.getsize(out_path)
        file_sha = sha256_file(out_path)
        print(f"Completed {prod} in {dt}s ({file_bytes} bytes, sha={file_sha[:16]}...)")
        
        report["renders"].append({
            "job": f"studio_{prod}",
            "product": prod,
            "kind": "single_studio_hero",
            "file": os.path.basename(out_path),
            "resolution": [960, 1200],
            "samples": 64,
            "render_seconds": dt,
            "bytes": file_bytes,
            "sha256": file_sha
        })

    # 2. Render 5-Product Hospitality Lineup
    lineup_path = os.path.join(RENDERS_DIR, "family_five_lineup.png")
    print(f"\n--- Rendering 5-product lineup -> {lineup_path} ---")
    
    # Unhide all products and place across X
    for p in PRODUCTS:
        col = bpy.data.collections.get(f"GEM_S3D_{p}")
        col.hide_render = False
        bpy.data.objects[f"GEM_{p}_root"].location = (POSITIONS[p], 0.0, 0.0)
        
    lineup_cam = bpy.data.objects.get('M34 cam family_five')
    if not lineup_cam:
        cam_data = bpy.data.cameras.new('M34 cam family_five')
        lineup_cam = bpy.data.objects.new('M34 cam family_five', cam_data)
        sc.collection.objects.link(lineup_cam)
        
    sc.camera = lineup_cam
    lineup_cam.data.lens = 100.0
    lineup_cam.data.dof.use_dof = False
    
    d = 1.52
    y_rad = math.radians(-4.0)
    e_rad = math.radians(3.5)
    lineup_cam.location = (
        d * math.sin(y_rad) * math.cos(e_rad),
        -d * math.cos(y_rad) * math.cos(e_rad),
        0.098 + d * math.sin(e_rad)
    )
    target = Vector((0.0, 0.0, 0.098))
    lineup_cam.rotation_euler = (target - lineup_cam.location).to_track_quat('-Z', 'Y').to_euler()
    
    sc.render.resolution_x = 2000
    sc.render.resolution_y = 1125
    sc.render.resolution_percentage = 100
    sc.cycles.samples = 96
    sc.render.filepath = lineup_path
    
    bpy.context.view_layer.update()
    t0 = time.time()
    bpy.ops.render.render(write_still=True, scene=sc.name)
    dt = round(time.time() - t0, 2)
    
    lineup_bytes = os.path.getsize(lineup_path)
    lineup_sha = sha256_file(lineup_path)
    print(f"Completed lineup in {dt}s ({lineup_bytes} bytes, sha={lineup_sha[:16]}...)")
    
    report["renders"].append({
        "job": "family_five_lineup",
        "product": "all_five",
        "kind": "hospitality_five_lineup",
        "file": os.path.basename(lineup_path),
        "resolution": [2000, 1125],
        "samples": 96,
        "render_seconds": dt,
        "bytes": lineup_bytes,
        "sha256": lineup_sha
    })
    
    # Restore default roots
    for p in PRODUCTS:
        bpy.data.objects[f"GEM_{p}_root"].location = (POSITIONS[p], 0.0, 0.0)
        bpy.data.collections.get(f"GEM_S3D_{p}").hide_render = False
    bpy.context.view_layer.update()
    
    with open(REPORT_PATH, "w") as f:
        import json
        json.dump(report, f, indent=2)
    print(f"\nRender report written to: {REPORT_PATH}")

if __name__ == "__main__":
    render_all()
