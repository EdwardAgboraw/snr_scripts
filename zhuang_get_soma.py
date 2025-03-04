# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 21:28:44 2025

@author: edwar

Source of code/tutorial:
https://alleninstitute.github.io/abc_atlas_access/notebooks/zhuang_merfish_tutorial.html


Goal = extract soma locations for all Zhuang Brain cells

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
ccf_zh2 = ccf_coordinates['Zhuang-ABCA-2']
ccf_zh3 = ccf_coordinates['Zhuang-ABCA-3']
ccf_zh4 = ccf_coordinates['Zhuang-ABCA-4']

#Get Parcellation Term Information
parcel_annot = abc_cache.get_metadata_dataframe(directory="Allen-CCF-2020",
                                                           file_name='parcellation_to_parcellation_term_membership_acronym')

#get all parcellation ids for Lateral Entorhinal Cortex (ENTl)
parcel_lec = parcel_annot[parcel_annot["structure"] == "ENTl"]
#parcel id for LEC Layer 5 = 134

#subset neurons to only include LEC Layer 5 cells
ccf_zh1 = ccf_zh1[ccf_zh1["parcellation_index"] == 134] #6073
ccf_zh2 = ccf_zh2[ccf_zh2["parcellation_index"] == 134] #2531
ccf_zh3 = ccf_zh3[ccf_zh3["parcellation_index"] == 134] #4253
ccf_zh4 = ccf_zh4[ccf_zh4["parcellation_index"] == 134] #760
# 13617 cells in total - enough for a good single-cell analysis.

#brain render requires soma coordinates as arrays of float32 objects

zh1_soma = snr.get_coords_from_aws(ccf_zh1)
zh2_soma = snr.get_coords_from_aws(ccf_zh2)
zh3_soma = snr.get_coords_from_aws(ccf_zh3)
zh4_soma = snr.get_coords_from_aws(ccf_zh4)

#create Points objects for Merfish Neurons
n1 = Points(zh1_soma, radius=20, colors="blue")
n2 = Points(zh2_soma, radius=20, colors="red")
n3 = Points(zh3_soma, radius=20, colors="green")
n4 = Points(zh4_soma, radius=20, colors="orange")


#load brainRender scene (lateral entorhinal cortex, layer 5
scene = Scene(atlas_name="allen_mouse_25um", title="LEC")
#scene = Scene(atlas_name="allen_mouse_10um", title="LEC")

# Display LEC Layer 5
lec = scene.add_brain_region("ENTl5", alpha=0.2)

#add soma to scene
scene.add(n1)
scene.add(n2)
scene.add(n3)
scene.add(n4)

# Add label to the brain region
scene.add_label(lec, "LEC Layer 5")

# Display the figure.
scene.render()

#all zhuang neurons appear to have been gathered from the same hemisphere
#provides comprehensive coverage of LEC Layer 5.






