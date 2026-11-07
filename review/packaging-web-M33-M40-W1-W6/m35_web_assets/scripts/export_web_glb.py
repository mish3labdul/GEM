"""Export web-optimized GLB models for all 5 GEM products.
Applies geometry decimation (target <25,000 tris, <1.5 MB),
sets bottom-center pivot at (0,0,0),
configures clean PBR materials (KHR_materials_transmission / IOR / roughness / metallic),
preserves crisp bilingual front-label UVs and packed textures,
and outputs gem_<product>.glb to m35_web_assets/glb/.
"""
import bpy
import os
import json
import hashlib
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
M35_DIR = os.path.dirname(HERE)
M34_DIR = os.path.join(M35_DIR, "..", "m34_five_product_3d")
SCENE_FILE = os.path.join(M34_DIR, "scenes", "GEM_M34_five_products_PROVISIONAL.blend")
GLB_OUT_DIR = os.path.join(M35_DIR, "glb")

PRODUCTS = ('shampoo', 'conditioner', 'body_wash', 'body_lotion', 'hand_wash')
PARTS = ('glass', 'liquid', 'label', 'collar', 'stem', 'actuator', 'spout', 'dip_tube')

DECIMATE_RATIOS = {
    'glass': 0.08,      # ~10,700 tris
    'liquid': 0.08,     # ~2,800 tris
    'collar': 0.08,     # ~1,800 tris
    'stem': 0.15,       # ~740 tris
    'actuator': 0.10,   # ~1,350 tris
    'spout': 0.10,      # ~1,700 tris
    'dip_tube': 1.0,    # 188 tris (lightweight)
    'label': 1.0        # 1,160 tris (preserve UV and curvature perfectly)
}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def create_web_materials():
    mats = {}
    
    # 1. Amber Glass
    mg = bpy.data.materials.get('GEM_WEB_amber_glass') or bpy.data.materials.new('GEM_WEB_amber_glass')
    mg.use_nodes = True
    bg = mg.node_tree.nodes.get('Principled BSDF')
    bg.inputs['Base Color'].default_value = (0.42, 0.22, 0.07, 1.0)
    bg.inputs['Roughness'].default_value = 0.04
    bg.inputs['Transmission Weight'].default_value = 1.0
    bg.inputs['IOR'].default_value = 1.50
    mats['glass'] = mg
    
    # 2. Amber Liquid
    ml = bpy.data.materials.get('GEM_WEB_amber_liquid') or bpy.data.materials.new('GEM_WEB_amber_liquid')
    ml.use_nodes = True
    bl = ml.node_tree.nodes.get('Principled BSDF')
    bl.inputs['Base Color'].default_value = (0.48, 0.25, 0.05, 1.0)
    bl.inputs['Roughness'].default_value = 0.08
    bl.inputs['Transmission Weight'].default_value = 0.70
    bl.inputs['IOR'].default_value = 1.36
    mats['liquid'] = ml
    
    # 3. Satin Black Pump
    mp = bpy.data.materials.get('GEM_WEB_pump_satin') or bpy.data.materials.new('GEM_WEB_pump_satin')
    mp.use_nodes = True
    bp = mp.node_tree.nodes.get('Principled BSDF')
    bp.inputs['Base Color'].default_value = (0.015, 0.015, 0.016, 1.0)
    bp.inputs['Roughness'].default_value = 0.45
    bp.inputs['Metallic'].default_value = 0.10
    mats['collar'] = mp
    mats['stem'] = mp
    mats['actuator'] = mp
    mats['spout'] = mp
    
    # 4. Dip Tube
    md = bpy.data.materials.get('GEM_WEB_dip_tube') or bpy.data.materials.new('GEM_WEB_dip_tube')
    md.use_nodes = True
    bd = md.node_tree.nodes.get('Principled BSDF')
    bd.inputs['Base Color'].default_value = (0.85, 0.85, 0.85, 1.0)
    bd.inputs['Roughness'].default_value = 0.25
    bd.inputs['Transmission Weight'].default_value = 0.85
    bd.inputs['IOR'].default_value = 1.45
    mats['dip_tube'] = md
    
    return mats

def export_all():
    os.makedirs(GLB_OUT_DIR, exist_ok=True)
    lookdev_scene = bpy.data.scenes.get('M8_Lookdev')
    if lookdev_scene:
        bpy.context.window.scene = lookdev_scene
        
    web_mats = create_web_materials()
    summary = {}
    
    for prod in PRODUCTS:
        glb_path = os.path.join(GLB_OUT_DIR, f"gem_{prod}.glb")
        print(f"\n==========================================")
        print(f"Exporting Web GLB for {prod} -> {glb_path}")
        
        # Deselect all
        for s in bpy.data.scenes:
            for o in s.objects:
                o.select_set(False)
                
        root = bpy.data.objects.get(f"GEM_{prod}_root")
        orig_root_loc = root.location.copy() if root else None
        
        # Prepare label material
        lbl_mat_name = f"GEM_WEB_label_{prod}"
        lbl_mat = bpy.data.materials.get(lbl_mat_name) or bpy.data.materials.new(lbl_mat_name)
        lbl_mat.use_nodes = True
        tree = lbl_mat.node_tree
        tree.nodes.clear()
        
        uv_node = tree.nodes.new('ShaderNodeUVMap')
        uv_node.location = (-400, 200)
        uv_node.uv_map = 'UVMap'
        
        tex_node = tree.nodes.new('ShaderNodeTexImage')
        tex_node.location = (-200, 200)
        img_name = f"GEM_S3D label {prod}"
        tex_node.image = bpy.data.images.get(img_name)
        
        bsdf_node = tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf_node.location = (100, 200)
        bsdf_node.inputs['Roughness'].default_value = 0.70
        bsdf_node.inputs['Metallic'].default_value = 0.0
        
        out_node = tree.nodes.new('ShaderNodeOutputMaterial')
        out_node.location = (400, 200)
        
        tree.links.new(uv_node.outputs['UV'], tex_node.inputs['Vector'])
        tree.links.new(tex_node.outputs['Color'], bsdf_node.inputs['Base Color'])
        tree.links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])
        
        # Track original materials and modifiers
        orig_materials = {}
        added_modifiers = []
        
        try:
            # 1. Center root at (0,0,0)
            if root:
                root.location = (0.0, 0.0, 0.0)
            bpy.context.view_layer.update()
            
            # 2. Select objects and configure web decimation + materials
            mesh_objs = []
            part_poly_counts = {}
            total_polys = 0
            
            for part in PARTS:
                obj = bpy.data.objects.get(f"GEM_{prod}_{part}")
                if not obj:
                    continue
                obj.select_set(True)
                mesh_objs.append(obj)
                
                # Save original material
                orig_materials[part] = [s.material for s in obj.material_slots]
                obj.data.materials.clear()
                
                if part == 'label':
                    obj.data.materials.append(lbl_mat)
                else:
                    obj.data.materials.append(web_mats[part])
                    
                # Add decimate modifier
                ratio = DECIMATE_RATIOS.get(part, 1.0)
                if ratio < 1.0:
                    mod = obj.modifiers.new(name='WebDecimate', type='DECIMATE')
                    mod.ratio = ratio
                    added_modifiers.append((obj, mod))
                    
                # Count evaluated polys
                dg = bpy.context.evaluated_depsgraph_get()
                obj_eval = obj.evaluated_get(dg)
                polys = len(obj_eval.data.polygons)
                part_poly_counts[part] = polys
                total_polys += polys
                
            print(f"Total evaluated polygons across 8 parts: {total_polys}")
            bpy.context.view_layer.objects.active = mesh_objs[0]
            
            # 3. Export GLB
            bpy.ops.export_scene.gltf(
                filepath=glb_path,
                use_selection=True,
                use_active_scene=True,
                export_format='GLB',
                export_apply=True,  # Applies decimate modifiers
                export_materials='EXPORT',
                export_image_format='AUTO'
            )
            
            file_bytes = os.path.getsize(glb_path)
            file_sha = sha256_file(glb_path)
            print(f"Exported {prod} GLB: {file_bytes} bytes ({file_bytes/1024:.1f} KB), SHA={file_sha[:16]}...")
            
            # Verify GLB structure
            with open(glb_path, 'rb') as f:
                data = f.read()
            magic, ver, length = struct.unpack_from('<4sII', data, 0)
            jlen, = struct.unpack_from('<I', data, 12)
            doc = json.loads(data[20:20+jlen])
            
            summary[prod] = {
                "file": f"gem_{prod}.glb",
                "bytes": file_bytes,
                "bytes_kb": round(file_bytes / 1024, 1),
                "sha256": file_sha,
                "total_polygons": total_polys,
                "part_polygons": part_poly_counts,
                "nodes_count": len(doc.get('nodes', [])),
                "materials_count": len(doc.get('materials', [])),
                "extensions_used": doc.get('extensionsUsed', []),
                "pass_budget_tris": total_polys < 25000,
                "pass_budget_size": file_bytes < 1500000
            }
            
        finally:
            # Clean up modifiers
            for obj, mod in added_modifiers:
                try:
                    obj.modifiers.remove(mod)
                except Exception:
                    pass
            # Restore materials
            for part, mats in orig_materials.items():
                obj = bpy.data.objects.get(f"GEM_{prod}_{part}")
                if obj:
                    obj.data.materials.clear()
                    for m in mats:
                        if m:
                            obj.data.materials.append(m)
            # Restore root location
            if root and orig_root_loc:
                root.location = orig_root_loc
            bpy.context.view_layer.update()
            
    summary_path = os.path.join(M35_DIR, "glb_export_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nAll 5 products exported. Summary written: {summary_path}")

if __name__ == "__main__":
    export_all()
