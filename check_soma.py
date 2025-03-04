# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:35:30 2025

@author: edwar

Checking the location of the soma (cell bodies) of the traced neurons
in brains 1056 and 1057 
(ent_data_20241126)
+
Visualising the soma in the mouse brain using brainRender

The soma measurement for a neuron is always given by the first row of
the CSV file.
"""

import pandas as pd
import numpy as np

from brainrender import Scene
from brainrender.actors import Points

import sys
sys.path.append("./snr_scripts")
import snr_functions as snr

#get soma coordinates for all neurons in brain 1057

data_path = "data/ent_data_20241022/ENT_NO1057/"
num_files = 19
all_soma_1 = snr.extract_soma(data_path, num_files)

#get soma coordinates for all neurons in brain 1056
data_path_2 = "data/ent_data_20241112/ENT_NO1056/"
num_files_2 = 41
all_soma_2 = snr.extract_soma(data_path_2, num_files_2)

#create a Points actor
neurons_1 = Points(all_soma_1, radius=40)
neurons_2 = Points(all_soma_2, radius=40, colors="blue")

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


