# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 11:28:22 2025

@author: edwar

Compare spatial locations of Zhuang Merfish Cells to that of the 
SNR cells

zhuang tutorial: https://alleninstitute.github.io/abc_atlas_access/notebooks/zhuang_merfish_tutorial.html

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

#get soma coordinates for all neurons in brain 1057 (SNR)
data_path = "data/ent_data_20241022/ENT_NO1057/"
num_files = 19
all_soma_1 = snr.extract_soma(data_path, num_files)

#get soma coordinates for all neurons in brain 1056 (SNR)
data_path_2 = "data/ent_data_20241112/ENT_NO1056/"
num_files_2 = 41
all_soma_2 = snr.extract_soma(data_path_2, num_files_2)

#create Points actors
neurons_1 = Points(all_soma_1, radius=40, colors = "salmon")
neurons_2 = Points(all_soma_2, radius=40, colors="blue")

#get soma locations from Zhuang-ABCA-1
#set up access to the AWS data
download_base = Path("C:/Users/edwar/Documents/PHD/single_neuron_reconstruction/atlas_data")

#get manifest for current release
abc_cache = AbcProjectCache.from_cache_dir(download_base)
abc_cache.current_manifest

#get datasets
datasets = ['Zhuang-ABCA-1', 'Zhuang-ABCA-2', 
            'Zhuang-ABCA-3', 'Zhuang-ABCA-4']

#get CCF coordinates for each dataset
ccf_coordinates = {}

for d in datasets :

    ccf_coordinates[d] = abc_cache.get_metadata_dataframe(directory=f"{d}-CCF", file_name='ccf_coordinates')
    ccf_coordinates[d].set_index('cell_label', inplace=True)
    ccf_coordinates[d].rename(columns={'x': 'x_ccf',
                                       'y': 'y_ccf',
                                       'z': 'z_ccf'},
                              inplace=True)
    
#now have the CCF coordinates and parcellation index for the 
#5.4 million MERFISH cells which passed all filters

ccf_zh1 = ccf_coordinates['Zhuang-ABCA-1']

ccf_zh1 = ccf_zh1[ccf_zh1["parcellation_index"] == 134]
#parcel id for LEC Layer 5 is 134

#brain render requires soma coordinates as arrays of float32 objects
zh1_soma = snr.get_coords_from_aws(ccf_zh1)

#create points actor
z1 = Points(zh1_soma, radius=20, colors="green")

#load brainRender scene (lateral entorhinal cortex, layer 5
scene = Scene(atlas_name="allen_mouse_25um", title="LEC")

# Display LEC Layer 5
lec = scene.add_brain_region("ENTl5", alpha=0.2)

#add soma to scene
scene.add(z1)
scene.add(neurons_1)
scene.add(neurons_2)

# Add label to the brain region
scene.add_label(lec, "LEC Layer 5")

# Display the figure.
scene.render()