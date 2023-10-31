import bpy
import random
import math

# Clear existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Create a cylinder to represent the axon
bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=10, location=(0, 0, 0))
axon = bpy.context.active_object

# Create sodium and potassium ions as spheres along the axon
num_ions = 500
ion_radius = 0.05
ions = []

for i in range(num_ions):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    z = random.uniform(-5, 5)
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=ion_radius, location=(x, y, z))
    ion = bpy.context.active_object
    ions.append(ion)
    
    # Assign materials to ions
    if i < num_ions // 2:
        # Sodium ions
        if "Sodium_Material" not in bpy.data.materials:
            sodium_mat = bpy.data.materials.new(name="Sodium_Material")
            sodium_mat.diffuse_color = (0.7, 0.7, 1, 1)
        else:
            sodium_mat = bpy.data.materials["Sodium_Material"]
        ion.data.materials.append(sodium_mat)
    else:
        # Potassium ions
        if "Potassium_Material" not in bpy.data.materials:
            potassium_mat = bpy.data.materials.new(name="Potassium_Material")
            potassium_mat.diffuse_color = (1, 0.7, 0.7, 1)
        else:
            potassium_mat = bpy.data.materials["Potassium_Material"]
        ion.data.materials.append(potassium_mat)

# Create an arrow object for instancing
bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.02, depth=0.5, location=(0, 0, -1000))  # Offscreen location
arrow_prototype = bpy.context.active_object
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')

# Create a grid of arrows to represent the magnetic field
magnetic_arrows = []
for height in range(-5, 6, 2):
    for radius in [2,3,4]:
        for angle in range(0, 360, 20):
            x = radius * math.cos(math.radians(angle))
            y = radius * math.sin(math.radians(angle))
            
            # Instance the arrow
            arrow = arrow_prototype.copy()
            arrow.location = (x, y, height)
            arrow.rotation_euler = (-math.pi/2, 0, math.radians(angle))
            bpy.context.collection.objects.link(arrow)
            
            magnetic_arrows.append(arrow)

# Hide the arrow prototype
arrow_prototype.hide_render = True
arrow_prototype.hide_viewport = True

# Animate the ions and the fields
start_frame = 1
end_frame = 250
peak_frame = 125
sigma = 25
 
for frame in range(start_frame, end_frame + 1):
    spike_intensity = math.exp(-((frame - peak_frame)**2) / (2 * sigma**2))

    for ion in ions:
        ion.location.z += random.random() * spike_intensity
        if ion.location.z > 5:
            ion.location.z = -5
        ion.keyframe_insert(data_path="location", frame=frame)

    # Update magnetic field arrows based on spike intensity
    for arrow in magnetic_arrows:
        arrow.scale.z = 10*spike_intensity 
        arrow.keyframe_insert(data_path="scale", frame=frame)

    # Update electric field on the axon
    axon.scale.z = 1 + spike_intensity * 0.1  # Adjust scaling factor as needed
    axon.keyframe_insert(data_path="scale", frame=frame)

bpy.context.scene.frame_end = end_frame
