# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 11:49:38 2025

@author: edwar
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 13:15:18 2025

@author: edwar

Load Labels Layer (tif file) created in Napari into BrainRender as a Mesh

New inspiration:
https://github.com/brainglobe/brainrender/blob/be420f11858c63a17f5006a1d9cc939556cc38e9/examples/user_volumetric_data.py


"""

from brainrender import Scene
from brainrender.actors import Points
#from brainrender.actors import Mesh
from brainrender.actors import Volume

from brainglobe_space import AnatomicalSpace

from brainglobe_atlasapi import BrainGlobeAtlas
import numpy as np

from tifffile import imread
import numpy as np

import vedo
from vedo import Volume as VedoVolume
from myterial import blue_grey, orange

import pandas as pd

# Load the TIFF file
#data = imread("hipp.tif")
#data = imread("ent_test.tif")
#data = imread("entl5_test.tif")
data = imread("mec-nts.tif")

#load corresponding atlas
scene = Scene(atlas_name="allen_mouse_25um", title="25um")

#align data to atlas
target_space = scene.atlas.space

#define Anatomical Space conventions for Allen Mouse Brain Atlases
source_space = AnatomicalSpace(
    "asl"
)  # for more info: https://docs.brainglobe.info/brainglobe-space/usage

transformed_stack = source_space.map_stack_to(target_space, data)


# 3. create a Volume vedo actor and smooth
print("Creating volume")
vol = VedoVolume(transformed_stack).isosurface()
#convert vertices
vol.vertices = vol.vertices / 0.04

# Ensure the data is binary (0 = background, 1 = region of interest)
#voxel_data = (voxel_data > 0).astype(np.uint8) 

#convert to Mesh object
mesh = vedo.Volume(data).isosurface()
#print(mesh.vertices) #coordiantes in pixel space
#print()
#mesh.vertices = mesh.vertices / 0.04
mesh = mesh.scale(25)

mesh.vertices = mesh.vertices[:, [2, 1, 0]]

#print(mesh.vertices) # coordinates in CCF space

#atlas_coords = pd.DataFrame(mesh.vertices)

#mesh2 = mesh.clone()

#mirror mesh
#mesh_right = mesh.clone().mirror(axis="x")

#mesh.vertices = vol.vertices

# Add it to the scene
#scene.add(vol)
scene.add(mesh)
#scene.add(mesh2)

# Display LEC Layer 5
mec = scene.add_brain_region("ENTm5", alpha=0.2)
#lec = scene.add_brain_region("ENTl5", alpha = 0.2)
# Add label to the brain region
scene.add_label(mec, "MEC Layer 5")
#scene.add_label(lec, "LEC Layer 5")

# Render the scene
scene.render()
