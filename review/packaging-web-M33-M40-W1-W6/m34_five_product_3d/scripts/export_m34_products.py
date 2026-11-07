"""Export individual OBJ and GLB files for each of the 5 products in GEM_M34_five_products_PROVISIONAL.blend.
Centers model at origin (0,0,0) during export and restores placement.
"""
import bpy
import os
import json
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
M34_DIR = os.path.dirname(HERE)
SCENE_FILE = os.path.join(M34_DIR, "scenes", "GEM_M34_five_products_PROVISIONAL.blend")
EXPORTS_DIR = os.path.join(M34_DIR, "exports")

PRODUCTS = ('shampoo', 'conditioner', 'body_wash', 'body_lotion', 'hand_wash')
PARTS = ('glass', 'liquid', 'label', 'collar', 'stem', 'actuator', 'spout', 'dip_tube')

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def export_all():
    manifest = {}
    lookdev_scene = bpy.data.scenes.get('M8_Lookdev')
    if lookdev_scene:
        bpy.context.window.scene = lookdev_scene
    
    for prod in PRODUCTS:
        prod_dir = os.path.join(EXPORTS_DIR, prod)
        os.makedirs(prod_dir, exist_ok=True)
        glb_path = os.path.join(prod_dir, f"gem_{prod}_provisional.glb")
        obj_path = os.path.join(prod_dir, f"gem_{prod}_provisional.obj")
        
        # Deselect all across all scenes
        for s in bpy.data.scenes:
            for o in s.objects:
                o.select_set(False)
        
        root = bpy.data.objects.get(f"GEM_{prod}_root")
        orig_loc = root.location.copy() if root else None
        
        try:
            # Temporarily center root
            if root:
                root.location = (0.0, 0.0, 0.0)
            bpy.context.view_layer.update()
            
            # Select parts
            mesh_objs = []
            for part in PARTS:
                obj = bpy.data.objects.get(f"GEM_{prod}_{part}")
                if obj:
                    obj.select_set(True)
                    mesh_objs.append(obj)
            
            if not mesh_objs:
                raise RuntimeError(f"No objects found for {prod}!")
                
            bpy.context.view_layer.objects.active = mesh_objs[0]
            
            # Export GLB
            print(f"Exporting GLB: {glb_path}...")
            bpy.ops.export_scene.gltf(
                filepath=glb_path,
                use_selection=True,
                use_active_scene=True,
                export_format='GLB',
                export_apply=False,
                export_materials='EXPORT',
                export_image_format='AUTO'
            )
            
            # Export OBJ
            print(f"Exporting OBJ: {obj_path}...")
            bpy.ops.wm.obj_export(
                filepath=obj_path,
                export_selected_objects=True,
                export_materials=True,
                forward_axis='NEGATIVE_Z',
                up_axis='Y'
            )
            
            manifest[prod] = {
                "glb": {
                    "path": os.path.relpath(glb_path, M34_DIR),
                    "bytes": os.path.getsize(glb_path),
                    "sha256": sha256_file(glb_path)
                },
                "obj": {
                    "path": os.path.relpath(obj_path, M34_DIR),
                    "bytes": os.path.getsize(obj_path),
                    "sha256": sha256_file(obj_path)
                }
            }
            print(f"Done {prod}: GLB {manifest[prod]['glb']['bytes']} bytes, OBJ {manifest[prod]['obj']['bytes']} bytes")
            
        finally:
            if root and orig_loc:
                root.location = orig_loc
            bpy.context.view_layer.update()
            
    manifest_path = os.path.join(EXPORTS_DIR, "exports_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Exports manifest written: {manifest_path}")

if __name__ == "__main__":
    export_all()
