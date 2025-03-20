# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 16:41:01 2025

@author: edwar
"""

import pandas as pd
import numpy as np

from brainrender import Scene
from brainrender.actors import Points

import sys
sys.path.append("./snr_scripts")
import snr_functions as snr


#load ORB vs RSP colour information
soma_colours = pd.read_excel("ORB_vs_RSP.xlsx")

#split
data_1056 = soma_colours[soma_colours["mouse_ID"] == "ENT1056"]
data_1057 = soma_colours[soma_colours["mouse_ID"] == "ENT1057"]

colours_1056 = data_1056["Colour"]
colours_1057 = data_1057["Colour"]

#get soma coordinates for all neurons in brain 1057

data_path = "data/ent_data_20241022/ENT_NO1057/"
num_files = 19
all_soma_1 = snr.extract_soma(data_path, num_files)

#all_soma_1_napari = all_soma_1 * 0.04
#np.save("soma_1_napari.npy", all_soma_1_napari)

#get soma coordinates for all neurons in brain 1056
data_path_2 = "data/ent_data_20241112/ENT_NO1056/"
num_files_2 = 41
all_soma_2 = snr.extract_soma(data_path_2, num_files_2)

#all_soma_2_napari = all_soma_2 * 0.04
#np.save("soma_2_napari.npy", all_soma_2_napari)

#create a Points actor
neurons_1 = Points(all_soma_1, radius=40, colors= colours_1057)
neurons_2 = Points(all_soma_2, radius=40, colors= colours_1056)

#load brainRender scene (lateral entorhinal cortex, layer 5
scene = Scene(atlas_name="allen_mouse_25um", title="LEC")

# Display LEC Layer 5
lec = scene.add_brain_region("ENTl5", alpha=0.2)

#add soma to scene
scene.add(neurons_1)
scene.add(neurons_2)

# Add label to the brain region
scene.add_label(lec, "LEC Layer 5")

# Display the figure.
scene.render()
