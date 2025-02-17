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


#extract soma coordinates for brain 1057
#folder = "data/ent_data_"


#load data for neuron 1 and 2 in brain 1056
n1 = pd.read_csv("data/ent_data_20241022/ENT_NO1057/1_trans.csv", nrows = 1)

n2 = pd.read_csv("data/ent_data_20241022/ENT_NO1057/2_trans.csv", nrows = 1)

#save soma location information
somaloc = n1["Abbreviation"][0]

somaloc_2 = n2["Abbreviation"][0]

#extract soma coordinates as list
soma_coords = [n1["x"][0],
               n1["y"][0],
               n1["z"][0]]

soma_coords_2 = [n2["x"][0],
                 n2["y"][0],
                 n2["z"][0]]

#collect data
all_soma = [soma_coords, soma_coords_2]

#convert to np float 32 array
all_soma = np.asarray(all_soma, dtype=np.float32)

#create a Points actor
neurons = Points(all_soma, radius=40)

#load brainRender scene (lateral entorhinal cortex, layer 5
scene = Scene(atlas_name="allen_mouse_25um", title="LEC")

# Display LEC Layer 5
lec = scene.add_brain_region("ENTl5", alpha=0.2)

#add soma to scene
scene.add(neurons)

# Add label to the brain region
scene.add_label(lec, "LEC Layer 5")

# Display the figure.
scene.render()


