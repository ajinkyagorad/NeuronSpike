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

# Create magnetic spheres
magnetic_spheres = []
total_spheres = 500  # or any number you prefer

for i in range(total_spheres):
    min_radius = 2  # minimum distance from the axis of the cylinder
    max_radius = 5  # maximum distance from the axis of the cylinder
    height_low = -5
    height_high = 5
    
    angle = random.uniform(0, 2 * math.pi)
    radius = random.uniform(min_radius, max_radius)
    height = random.uniform(height_low, height_high)

    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    z = height
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.07, location=(x, y, z))
    sphere = bpy.context.active_object
    
    # Assign green material to the magnetic spheres
    if "Green_Material" not in bpy.data.materials:
        green_mat = bpy.data.materials.new(name="Green_Material")
        green_mat.diffuse_color = (0.0, 1.0, 0.0, 1)
    else:
        green_mat = bpy.data.materials["Green_Material"]
        
    sphere.data.materials.append(green_mat)
    
    magnetic_spheres.append(sphere)



# Animate the ions and the magnetic spheres
start_frame = 1
end_frame = 500   
peak_frame = 125
second_peak_frame = 125+250
sigma = 25

for frame in range(start_frame, end_frame + 1):
    
    if frame <= 250:
        # Positive spike for the first part
        spike_intensity = math.exp(-((frame - peak_frame)**2) / (2 * sigma**2))
    else:
        # Negative spike for the second part
        second_peak_frame = 375
        spike_intensity = -math.exp(-((frame - second_peak_frame)**2) / (2 * sigma**2))


    for ion in ions:
        ion.location.z += random.random() * spike_intensity
        if ion.location.z > 5:
            ion.location.z = -5
        if ion.location.z < -5:
            ion.location.z = 5
        ion.keyframe_insert(data_path="location", frame=frame)

    # Rotate magnetic spheres around the z-axis
    for sphere in magnetic_spheres:
        x, y, z = sphere.location
        radial_distance = math.sqrt(x**2 + y**2)
        
        # Set rotation speed based on spike_intensity and radial_distance
        if radial_distance != 0:
            angle = math.atan2(y, x)
            rotation_speed = .3* spike_intensity / radial_distance
            angle += rotation_speed  # anti-clockwise rotation
            sphere.location.x = math.cos(angle) * radial_distance
            sphere.location.y = math.sin(angle) * radial_distance
            sphere.keyframe_insert(data_path="location", frame=frame)

    # Update electric field on the axon
    axon.scale.z = 1 + spike_intensity * 0.1  # Adjust scaling factor as needed
    axon.keyframe_insert(data_path="scale", frame=frame)


bpy.context.scene.frame_end = end_frame
