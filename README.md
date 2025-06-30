# BlenderDNAScript
DNA Structure Generator in Blender (Python + bpy)

This script generates an editable 3D DNA double-helix model inside Blender, using the `bpy` Python API. It's designed to help animators, scientific illustrators, educators, and developers rapidly prototype DNA models with structural accuracy and customizable visuals.

--------------------------------------------------
FEATURES
--------------------------------------------------

✅ Supports multiple DNA types:
- B-DNA (default, 3.4 Å rise, 20 Å diameter)
- A-DNA (2.3 Å rise, 26 Å diameter, right-handed)
- Z-DNA (3.7 Å rise, 18 Å diameter, left-handed)

✅ Clean base-pair geometry:
- Each base (A, T, G, C) represented by a color-coded cube
- Proper orientation toward the helix center
- Correct rotation, scale, and spacing based on DNA type

✅ Structured backbone:
- Cylindrical phosphate-sugar chain with smooth twist
- Connector spheres between segments to fill gaps

✅ Scene organization:
- All geometry is added to named Blender collections:
    - BasePairs
    - Backbone
        - Cylinders
        - JoinSpheres

✅ Material system:
- One shared `Backbone` material for cylinders and spheres
- Four unique materials: `A`, `T`, `G`, `C`
- A `Floor` plane is generated with all materials pre-assigned for easy editing

✅ Customizable inputs:
- DNA sequence (`ATGCGT...`)
- DNA type (`A`, `B`, `Z`)
- Materials editable by selecting the floor object

--------------------------------------------------
USAGE
--------------------------------------------------

1. Open Blender
2. Paste the script into the Scripting editor
3. Set your desired DNA sequence and DNA_FORM at the top
4. Run the script
5. Select the “Floor” plane to access and tweak all materials

--------------------------------------------------
NOTES
--------------------------------------------------

- The script is clean and modular for future extension
- Future versions may support:
    - Base pair bonds
    - 3D nucleotide meshes
    - Curve-guided strands
    - Unwinding/replication animations
