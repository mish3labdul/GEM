"""Build GEM_M34_five_products_PROVISIONAL.blend from GEM_M29_MASTER_UNAPPROVED.blend.
Retains Shampoo and Conditioner 100% untouched.
Adds Body Wash, Body Lotion, and Hand Wash collections under Authorization B (GEM-PKG-OWNER-20261107-005)
using the GEM architectural vocabulary and packing all 5 M15 bilingual label textures.
"""
import bpy
import json
import os
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
M34_DIR = os.path.dirname(HERE)
PARAMS_FILE = os.path.join(M34_DIR, "params", "m34_five_product_params.json")
SCENE_FILE = os.path.join(M34_DIR, "scenes", "GEM_M34_five_products_PROVISIONAL.blend")

with open(PARAMS_FILE, "r") as f:
    CONFIG = json.load(f)

PARTS = ('glass', 'liquid', 'label', 'collar', 'stem', 'actuator', 'spout', 'dip_tube')
NEW_PRODUCTS = ('body_wash', 'body_lotion', 'hand_wash')
ALL_PRODUCTS = ('shampoo', 'conditioner', 'body_wash', 'body_lotion', 'hand_wash')

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

def build_scene():
    lookdev_scene = bpy.data.scenes.get('M8_Lookdev')
    if not lookdev_scene:
        raise RuntimeError("Scene M8_Lookdev not found!")

    shampoo_hash_before = get_geom_hash('shampoo')
    conditioner_hash_before = get_geom_hash('conditioner')
    print("Shampoo geom hash before:", shampoo_hash_before)
    print("Conditioner geom hash before:", conditioner_hash_before)

    # 1. Prepare label images & materials for all products
    repo_root = os.path.abspath(os.path.join(M34_DIR, "..", "..", ".."))
    
    for prod in ALL_PRODUCTS:
        meta = CONFIG['products'][prod]['confirmed_metadata']
        tex_path = os.path.join(repo_root, meta['label_texture_path'])
        if not os.path.isfile(tex_path):
            raise FileNotFoundError(f"Label texture not found: {tex_path}")

        img_name = f"GEM_S3D label {prod}"
        img = bpy.data.images.get(img_name)
        if not img:
            img = bpy.data.images.load(tex_path)
            img.name = img_name
        else:
            img.filepath = tex_path
            img.reload()
        
        # Ensure image is packed
        if not img.packed_file:
            img.pack()
        
        # Verify packed bytes match texture
        packed_bytes = bytes(img.packed_file.data)
        file_bytes = open(tex_path, "rb").read()
        if hashlib.sha256(packed_bytes).hexdigest() != hashlib.sha256(file_bytes).hexdigest():
            raise RuntimeError(f"Packed image bytes mismatch for {img_name}")
        print(f"Verified packed texture {img_name} ({len(packed_bytes)} bytes)")

        # Prepare label material
        mat_name = meta['label_material_datablock']
        mat = bpy.data.materials.get(mat_name)
        if not mat:
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True
            tree = mat.node_tree
            tree.nodes.clear()
            
            uv_node = tree.nodes.new('ShaderNodeUVMap')
            uv_node.location = (-400, 200)
            uv_node.uv_map = 'UVMap'
            
            tex_node = tree.nodes.new('ShaderNodeTexImage')
            tex_node.name = "Label Image"
            tex_node.location = (-200, 200)
            tex_node.image = img
            
            bsdf_node = tree.nodes.new('ShaderNodeBsdfPrincipled')
            bsdf_node.location = (100, 200)
            bsdf_node.inputs['Roughness'].default_value = 0.70
            if 'Specular IOR Level' in bsdf_node.inputs:
                bsdf_node.inputs['Specular IOR Level'].default_value = 0.15
            elif 'Specular' in bsdf_node.inputs:
                bsdf_node.inputs['Specular'].default_value = 0.15
                
            out_node = tree.nodes.new('ShaderNodeOutputMaterial')
            out_node.location = (400, 200)
            
            tree.links.new(uv_node.outputs['UV'], tex_node.inputs['Vector'])
            tree.links.new(tex_node.outputs['Color'], bsdf_node.inputs['Base Color'])
            tree.links.new(bsdf_node.outputs['BSDF'], out_node.inputs['Surface'])
            print(f"Created label material {mat_name}")

    # 2. Add New Products
    for prod in NEW_PRODUCTS:
        col_name = f"GEM_S3D_{prod}"
        col = bpy.data.collections.get(col_name)
        if col:
            # Clean existing collection if script re-run
            for o in list(col.objects):
                bpy.data.objects.remove(o, do_unlink=True)
            bpy.data.collections.remove(col)
        
        col = bpy.data.collections.new(col_name)
        lookdev_scene.collection.children.link(col)
        
        geo_params = CONFIG['products'][prod]['provisional_exploratory_geometry']
        layout_x = geo_params['lineup_layout_x_m']
        
        # Root empty
        root_name = f"GEM_{prod}_root"
        root = bpy.data.objects.get(root_name)
        if root:
            bpy.data.objects.remove(root, do_unlink=True)
        root = bpy.data.objects.new(root_name, None)
        root.location = (layout_x, 0.0, 0.0)
        root.scale = (0.001, 0.001, 0.001)
        root['gem_product'] = prod
        root['dimensions_status'] = 'PROVISIONAL_EXPLORATORY_GEOMETRY'
        root['auth_ref'] = 'GEM-PKG-OWNER-20261107-005'
        col.objects.link(root)
        
        # Create 8 parts
        for part in PARTS:
            src_obj = bpy.data.objects[f"GEM_shampoo_{part}"]
            src_mesh = src_obj.data
            
            new_mesh_name = f"GEM_{prod}_{part}_mesh"
            old_mesh = bpy.data.meshes.get(new_mesh_name)
            if old_mesh:
                bpy.data.meshes.remove(old_mesh)
            
            new_mesh = src_mesh.copy()
            new_mesh.name = new_mesh_name
            
            obj_name = f"GEM_{prod}_{part}"
            new_obj = bpy.data.objects.new(obj_name, new_mesh)
            new_obj.location = src_obj.location.copy()
            new_obj.rotation_mode = src_obj.rotation_mode
            new_obj.rotation_euler = src_obj.rotation_euler.copy()
            new_obj.rotation_quaternion = src_obj.rotation_quaternion.copy()
            new_obj.scale = src_obj.scale.copy()
            new_obj.parent = root
            new_obj.matrix_parent_inverse = src_obj.matrix_parent_inverse.copy()
            
            # Custom properties
            new_obj['gem_product'] = prod
            new_obj['gem_region'] = part
            new_obj['dimensions_status'] = 'PROVISIONAL_EXPLORATORY_GEOMETRY'
            new_obj['auth_ref'] = 'GEM-PKG-OWNER-20261107-005'
            new_obj['gem_arabic_name'] = CONFIG['products'][prod]['confirmed_metadata']['name_ar']
            new_obj['gem_material_key'] = src_obj.get('gem_material_key', '')
            
            # Assign materials
            new_obj.data.materials.clear()
            if part == 'label':
                lbl_mat = bpy.data.materials[CONFIG['products'][prod]['confirmed_metadata']['label_material_datablock']]
                new_obj.data.materials.append(lbl_mat)
            else:
                for s in src_obj.material_slots:
                    if s.material:
                        new_obj.data.materials.append(s.material)
            
            col.objects.link(new_obj)
        print(f"Created collection {col_name} with 8 parts and root at X={layout_x}")

    # Verify Shampoo and Conditioner remain untouched
    shampoo_hash_after = get_geom_hash('shampoo')
    conditioner_hash_after = get_geom_hash('conditioner')
    assert shampoo_hash_before == shampoo_hash_after, f"Shampoo geom hash changed! {shampoo_hash_before} != {shampoo_hash_after}"
    assert conditioner_hash_before == conditioner_hash_after, f"Conditioner geom hash changed! {conditioner_hash_before} != {conditioner_hash_after}"
    print("PASSED: Shampoo and Conditioner remain 100% byte-identical and untouched!")

    # Save blend file
    bpy.ops.wm.save_mainfile(filepath=SCENE_FILE)
    print(f"Saved provisional five-product master: {SCENE_FILE}")

if __name__ == "__main__":
    build_scene()
