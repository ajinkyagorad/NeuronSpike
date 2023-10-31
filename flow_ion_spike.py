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
    z = random.uniform(-5, 5)  # Initially place ions within the -5 to 5 range
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=ion_radius, location=(x, y, z))
    ion = bpy.context.active_object
    ions.append(ion)
    
    # Assign materials to ions (for visualization)
    if i < num_ions // 2:
        if "Sodium_Material" not in bpy.data.materials:
            sodium_mat = bpy.data.materials.new(name="Sodium_Material")
            sodium_mat.diffuse_color = (0.7, 0.7, 1, 1)
        else:
            sodium_mat = bpy.data.materials["Sodium_Material"]
        ion.data.materials.append(sodium_mat)
    else:
        if "Potassium_Material" not in bpy.data.materials:
            potassium_mat = bpy.data.materials.new(name="Potassium_Material")
            potassium_mat.diffuse_color = (1, 0.7, 0.7, 1)
        else: 
            potassium_mat = bpy.data.materials["Potassium_ Material"]
        ion.data.materials.append(potassium_mat)

# Animate the ions based on a simulated neuron spike
start_frame = 1
end_frame = 250
peak_frame = 125  # The frame at which the spike peaks
sigma = 25  # Controls the width of the spike

for frame in range(start_frame, end_frame + 1):
    for ion in ions:
        # Gaussian function to simulate the spike  
        spike_intensity = math.exp(-((frame - peak_frame)**2) / (2 * sigma**2))
        
        # Move ions based on the spike intensity
        ion.location.z += random.random() * spike_intensity
        # Wrap ions around if they move above z=5
        if ion.location.z > 5:
            ion.location.z = -5
        
        ion.keyframe_insert(data_path="location", frame=frame)

bpy.context.scene.frame_end = end_frame
