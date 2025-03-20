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
data = imread("mec-nts.tif")

#load corresponding atlas
scene = Scene(atlas_name="allen_mouse_25um", title="25um")

# Display LEC Layer 5
mec = scene.add_brain_region("ENTm5", alpha=0.2)
#lec = scene.add_brain_region("ENTl5", alpha = 0.2)
# Add label to the brain region
scene.add_label(mec, "MEC Layer 5")
#scene.add_label(lec, "LEC Layer 5")

#convert Labels Layer to Mesh object
mesh = vedo.Volume(data).isosurface()
#scale coordiantes
mesh = mesh.scale(25)
#reorder axes from z,y,x (napari) to x,y,z (brainrender)
mesh.vertices = mesh.vertices[:, [2, 1, 0]]

#create flipped (opposite hemisphere) copy
mesh2 = mesh.copy()
mesh2.vertices[:, 0] = 11400 - mesh2.vertices[:, 0]

#add mesh to scene
scene.add(mesh)
scene.add(mesh2)

# Render the scene
scene.render()
