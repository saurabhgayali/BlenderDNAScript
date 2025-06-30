import bpy
import math
import mathutils

# === USER OPTIONS ===
DNA_FORM = "B"  # Options: "A", "B", "Z"
dna_sequence = "ATGCGTACGCTAAGCT"

# === BASE COLORS (editable) ===
BASE_COLORS = {
    'A': (1.0, 0.0, 0.0),     # Red
    'T': (0.0, 0.4, 1.0),     # Blue
    'G': (0.0, 1.0, 0.0),     # Green
    'C': (1.0, 1.0, 0.0),     # Yellow
}
BACKBONE_COLOR = (0.7, 0.7, 0.7)

# === DNA FORM CONFIGURATION ===
DNA_CONFIGS = {
    'B': {'twist_angle': 36.0, 'rise': 0.34, 'diameter': 2.0, 'handedness': 'right'},
    'A': {'twist_angle': 33.0, 'rise': 0.23, 'diameter': 2.6, 'handedness': 'right'},
    'Z': {'twist_angle': 60.0, 'rise': 0.37, 'diameter': 1.8, 'handedness': 'left'},
}

# Load config
config = DNA_CONFIGS[DNA_FORM.upper()]
twist_angle = config['twist_angle']
base_pair_distance = config['rise']
diameter = config['diameter']
radius = diameter / 2.0
is_left_handed = config['handedness'] == 'left'

# Geometry
backbone_radius = 0.05
base_width = 0.2
base_length = radius * 0.95  # half of diameter, slightly short to avoid overlap
base_height = 0.02

# === MATERIAL SETUP ===
def create_material(name, color):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = False
    return mat

base_materials = {
    base: create_material(base, BASE_COLORS[base]) for base in BASE_COLORS
}
backbone_material = create_material("Backbone", BACKBONE_COLOR)

complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}

# === OBJECT CREATION ===
def create_base(location, base, name, direction_vec):
    direction = mathutils.Vector(direction_vec).normalized()
    offset = direction * (base_length / 2)
    adjusted_location = mathutils.Vector(location) + offset

    bpy.ops.mesh.primitive_cube_add(size=1, location=adjusted_location)
    obj = bpy.context.object
    obj.scale = (base_length, base_width, base_height)
    obj.name = name

    # Constrain rotation: only rotate around Z to face inward in XY plane
    x, y = direction.xy
    angle_z = math.atan2(y, x)
    obj.rotation_euler = (0, 0, angle_z)

    if base in base_materials:
        obj.data.materials.append(base_materials[base])

def create_backbone(start, end, name):
    mid = [(s + e) / 2 for s, e in zip(start, end)]
    direction = [e - s for s, e in zip(start, end)]
    length = math.sqrt(sum([d ** 2 for d in direction]))

    bpy.ops.mesh.primitive_cylinder_add(
        radius=backbone_radius,
        depth=length,
        location=(0, 0, 0)
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(backbone_material)

    vec = mathutils.Vector(direction).normalized()
    up = mathutils.Vector((0, 0, 1))
    rot_quat = up.rotation_difference(vec)
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = rot_quat
    obj.location = mid

def create_backbone_joint_sphere(location, name):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=backbone_radius,
        location=location,
        segments=16,
        ring_count=8
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(backbone_material)

# === DNA GENERATOR ===
def generate_dna(sequence):
    angle = 0
    prev_a = prev_b = None

    for i, base in enumerate(sequence.upper()):
        if base not in complement:
            print(f"Skipping invalid base: {base}")
            continue

        comp_base = complement[base]
        theta = math.radians(angle)
        direction = -1 if is_left_handed else 1

        # Compute helical strand positions
        x_a = radius * math.cos(theta)
        y_a = radius * math.sin(theta)
        x_b = -x_a
        y_b = -y_a
        z = i * base_pair_distance

        pos_a = (direction * x_a, direction * y_a, z)
        pos_b = (direction * x_b, direction * y_b, z)

        # Vector from backbone toward center
        dir_a = [-x_a, -y_a, 0]
        dir_b = [-x_b, -y_b, 0]

        create_base(pos_a, base, f"Base_{i}_{base}", dir_a)
        create_base(pos_b, comp_base, f"Base_{i}_{comp_base}", dir_b)

        if prev_a and prev_b:
            create_backbone(prev_a, pos_a, f"Backbone_A_{i}")
            create_backbone(prev_b, pos_b, f"Backbone_B_{i}")
            create_backbone_joint_sphere(pos_a, f"Joint_A_{i}")
            create_backbone_joint_sphere(pos_b, f"Joint_B_{i}")
        else:
            create_backbone_joint_sphere(pos_a, f"Joint_A_{i}")
            create_backbone_joint_sphere(pos_b, f"Joint_B_{i}")

        prev_a = pos_a
        prev_b = pos_b
        angle += twist_angle

# === SCENE CLEANUP ===
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

# === RUN ===
clear_scene()
generate_dna(dna_sequence)
