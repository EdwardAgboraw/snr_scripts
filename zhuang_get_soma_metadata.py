# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 12:28:34 2025

@author: edwar
"""

from pathlib import Path
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache

import pandas as pd
import numpy as np

from brainrender import Scene
from brainrender.actors import Points

import sys
sys.path.append("./snr_scripts")
import snr_functions as snr

#set up access to the AWS data
download_base = Path("C:/Users/edwar/Documents/PHD/single_neuron_reconstruction/atlas_data")

#get manifest for current release
abc_cache = AbcProjectCache.from_cache_dir(download_base)
abc_cache.current_manifest

#get datasets
datasets = ['Zhuang-ABCA-1', 'Zhuang-ABCA-2', 
            'Zhuang-ABCA-3', 'Zhuang-ABCA-4']

#get ccf coordinates

ccf_coordinates = {}

for d in datasets :

    ccf_coordinates[d] = abc_cache.get_metadata_dataframe(directory=f"{d}-CCF", file_name='ccf_coordinates')
    ccf_coordinates[d].set_index('cell_label', inplace=True)
    ccf_coordinates[d].rename(columns={'x': 'x_ccf',
                                       'y': 'y_ccf',
                                       'z': 'z_ccf'},
                              inplace=True)
    
ccf_zh4 = ccf_coordinates['Zhuang-ABCA-4']
ccf_zh4 = ccf_zh4[ccf_zh4["parcellation_index"] == 134] #760

#get corrected (mm -> um) coordinates for zh4
zh4_soma = snr.get_coords_from_aws(ccf_zh4)

#get metadata 
cell = {}

for d in datasets :

    cell[d] = abc_cache.get_metadata_dataframe(
        directory=d,
        file_name='cell_metadata',
        dtype={"cell_label": str}
    )
    cell[d].set_index('cell_label', inplace=True)
    
    sdf = cell[d].groupby('brain_section_label')
    
    print(d,":","Number of cells = ", len(cell[d]), ", ", "Number of sections =", len(sdf))
    
#meta_zh1 = cell['Zhuang-ABCA-1']
#meta_zh2 = cell['Zhuang-ABCA-2']
#meta_zh3 = cell['Zhuang-ABCA-3']
meta_zh4 = cell['Zhuang-ABCA-4']

#subset meta_zh4 to only include LEC layer 5 cells
meta_zh4 = meta_zh4[meta_zh4.index.isin(ccf_zh4.index)]

#test on meta_zh4

meta_coords = []
    
for index, row in meta_zh4.iterrows():
    x = row["x"] * 1000
    y = row["y"] * 1000
    z = row["z"] * 1000
        
    coords = [x,y,z]
        
    meta_coords.append(coords)

meta_coords = np.asarray(meta_coords, dtype=np.float32)

#visualize via brain render

#create Points objects for Merfish Neurons
n1 = Points(zh4_soma, radius=20, colors="blue")
n2 = Points(meta_coords, radius=20, colors="red")

#load brainRender scene (lateral entorhinal cortex, layer 5
scene = Scene(atlas_name="allen_mouse_25um", title="LEC")
#scene = Scene(atlas_name="allen_mouse_10um", title="LEC")

# Display LEC Layer 5
lec = scene.add_brain_region("ENTl5", alpha=0.2)

#add soma to scene
scene.add(n1)
scene.add(n2)

# Add label to the brain region
scene.add_label(lec, "LEC Layer 5")

# Display the figure.
scene.render()



