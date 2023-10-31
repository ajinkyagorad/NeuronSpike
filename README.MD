# Neuron Ion Simulation in Blender

## Overview

This Blender script simulates the movement of ions (Sodium and Potassium) along a neural axon during a neuronal spike. It's a visual representation aiming to facilitate the understanding of ion movements and their role in action potentials in neurons. The script is written in Python and uses Blender's API for object creation, manipulation, and animation.

### Key Features

- Generates a cylinder to represent a neural axon.
- Populates the axon with Sodium and Potassium ions represented as spheres.
- Animate the ions to move along the z-axis based on a Gaussian spike function.
- Ions that move out of the axon are wrapped back to the other end, maintaining the total number of ions.

![EM Animation](EM.gif)

### How it Works

1. **Clear Existing Mesh Objects**: The script first deletes any existing mesh objects in the scene.
2. **Axon Creation**: A cylinder is added to act as the neural axon.
3. **Ion Creation**: Sodium and Potassium ions are randomly placed along the axon. These ions are represented as small spheres.
4. **Material Assignment**: Different materials are applied to Sodium and Potassium ions for better visualization.
5. **Animation**: Each ion is animated to move along the z-axis. The movement is based on a Gaussian function, simulating the ion behavior during a neuronal spike. The ions are wrapped back to the opposite end if they move out of the specified bounds.

### Dependencies

- Blender
- Python

For more detailed explanation, feel free to explore the source code. Enjoy visualizing the fascinating world of neurons!

Note: Generated with the help of ChatGPT4.
