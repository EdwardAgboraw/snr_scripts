# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 08:40:36 2025

@author: edwar
"""

from brainrender import Scene
from tifffile import imread
import vedo


# Load the TIFF files
lec = imread("napari_layers/lec.tif")
intEC = imread("napari_layers/int-EC.tif")
mec = imread("napari_layers/mec.tif")

#Labels to Mesh Conversion
def labels_to_mesh(data):
    mesh = vedo.Volume(data).isosurface()
    #scale coordiantes
    mesh = mesh.scale(25)
    #reorder axes from z,y,x (napari) to x,y,z (brainrender)
    mesh.vertices = mesh.vertices[:, [2, 1, 0]]
    return(mesh)

lec_mesh = labels_to_mesh(lec)
intEC_mesh = labels_to_mesh(intEC)
mec_mesh = labels_to_mesh(mec)

#add colours
lec_mesh.c("teal")
mec_mesh.c("orange")
intEC_mesh.c("green")

#load corresponding atlas
scene = Scene(atlas_name="allen_mouse_25um", title="25um")

# Display EC Layer 5
mec = scene.add_brain_region("ENTm5", alpha=0.2)
lec = scene.add_brain_region("ENTl5", alpha = 0.2)
# Add label to the brain region
scene.add_label(mec, "MEC Layer 5")
scene.add_label(lec, "LEC Layer 5")

#add meshes
scene.add(mec_mesh)
scene.add(intEC_mesh)
scene.add(lec_mesh)

#visualize
scene.render()
