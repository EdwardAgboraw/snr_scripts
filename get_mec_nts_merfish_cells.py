# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 09:19:09 2025

@author: edwar

Get corrected CCF coordinates from the mec-nts labels layer created
by Gulsen in Napari.
Search through the MERFISH data for cells found within those bounds.
Visualize cells in brainrender.

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

from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache
import pandas as pd
from pathlib import Path
import numpy as np
import anndata
import time

#load mec-nts labels layer tif file----------------------------------------
data = imread("mec-nts.tif")
#convert to Mesh object
mesh = vedo.Volume(data).isosurface()
#scale coordinates from pixel space to atlas space
mesh = mesh.scale(25)
#reorder axes from z,y,x (napari) to x,y,z (brainrender)
mesh.vertices = mesh.vertices[:, [2, 1, 0]]

#translate into right hemisphere
mesh.vertices[:, 0] = 11400 - mesh.vertices[:, 0]

#extract corrected CCF coordinates of MESH for later use
coords = pd.DataFrame(mesh.vertices)
coords.columns = ["z", "y", "x"]

#Define bounds of mec-nts mesh

x_max = coords["x"].max()
x_min = coords["x"].min()

y_max = coords["y"].max()
y_min = coords["y"].min()

z_max = coords["z"].max()
z_min = coords["z"].min()

#Get MERFISH Data----------------------------------------------------------
#set up access to the AWS data
download_base = Path("C:/Users/edwar/Documents/PHD/single_neuron_reconstruction/atlas_data")

#get manifest for current release
abc_cache = AbcProjectCache.from_cache_dir(download_base)
abc_cache.current_manifest

#get datasets
datasets = ['Zhuang-ABCA-1', 'Zhuang-ABCA-2', 
            'Zhuang-ABCA-3', 'Zhuang-ABCA-4']

#get cell metadata
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

#get cluster annotations

cluster_details = abc_cache.get_metadata_dataframe(
    directory='WMB-taxonomy',
    file_name='cluster_to_cluster_annotation_membership_pivoted',
    keep_default_na=False
)
cluster_details.set_index('cluster_alias', inplace=True)

cluster_colors = abc_cache.get_metadata_dataframe(
    directory='WMB-taxonomy',
    file_name='cluster_to_cluster_annotation_membership_color',
)
cluster_colors.set_index('cluster_alias', inplace=True)

cell_extended = {}

for d in datasets :
    cell_extended[d] = cell[d].join(cluster_details, on='cluster_alias')
    cell_extended[d] = cell_extended[d].join(cluster_colors, on='cluster_alias')
    
#get CCF coordiantes
ccf_coordinates = {}

for d in datasets :

    ccf_coordinates[d] = abc_cache.get_metadata_dataframe(directory=f"{d}-CCF", file_name='ccf_coordinates')
    ccf_coordinates[d].set_index('cell_label', inplace=True)
    ccf_coordinates[d].rename(columns={'x': 'x_ccf',
                                       'y': 'y_ccf',
                                       'z': 'z_ccf'},
                              inplace=True)
    
    cell_extended[d] = cell_extended[d].join(ccf_coordinates[d], how='inner')
    
#get parcellation information
    
parcellation_annotation = abc_cache.get_metadata_dataframe(directory="Allen-CCF-2020",
                                                           file_name='parcellation_to_parcellation_term_membership_acronym')
parcellation_annotation.set_index('parcellation_index', inplace=True)
parcellation_annotation.columns = ['parcellation_%s'% x for x in  parcellation_annotation.columns]

parcellation_color = abc_cache.get_metadata_dataframe(directory="Allen-CCF-2020",
                                                      file_name='parcellation_to_parcellation_term_membership_color')
parcellation_color.set_index('parcellation_index', inplace=True)
parcellation_color.columns = ['parcellation_%s'% x for x in  parcellation_color.columns]

for d in datasets :
    cell_extended[d] = cell_extended[d].join(parcellation_annotation, on='parcellation_index')
    cell_extended[d] = cell_extended[d].join(parcellation_color, on='parcellation_index')   

# Scale CCF Coordinates
for abca in ['Zhuang-ABCA-1', 'Zhuang-ABCA-2','Zhuang-ABCA-3', 'Zhuang-ABCA-4']:
    cell_extended[abca][['x_ccf', 'y_ccf', 'z_ccf']] *= 1000
    

mesh_pop = {}
#Filter for Cells within MEC-NTS Mesh
for abca in ['Zhuang-ABCA-1', 'Zhuang-ABCA-2','Zhuang-ABCA-3', 'Zhuang-ABCA-4']:
    df = cell_extended[abca]
    df = df.loc[(df['x_ccf'] >= x_min) & (df['x_ccf'] <= x_max)]
    df = df.loc[(df['y_ccf'] >= y_min) & (df['y_ccf'] <= y_max)]
    df = df.loc[(df['z_ccf'] >= z_min) & (df['z_ccf'] <= z_max)]
    mesh_pop[abca] = df
 
zh1 = mesh_pop["Zhuang-ABCA-1"]
zh2 = mesh_pop["Zhuang-ABCA-2"]
zh3 = mesh_pop["Zhuang-ABCA-3"]
zh4 = mesh_pop["Zhuang-ABCA-4"]

mesh_cells = pd.concat([zh1,zh2,zh3,zh4])

#only keep excitatory and inhibitory cell types
mesh_cells = mesh_cells[mesh_cells["neurotransmitter"].isin(
    ["Glut", "GABA"])]

mesh_cells_coords = mesh_cells[['x_ccf', 'y_ccf', 'z_ccf']].to_numpy()

#Generate brainrender Visualization
scene = Scene(atlas_name="allen_mouse_25um", title="25um")

#add cells
scene.add(Points(mesh_cells_coords))

# Add mesh to scene
scene.add(mesh)
# Display LEC Layer 5
mec = scene.add_brain_region("ENTm5", alpha=0.2)
# Add label to the brain region
scene.add_label(mec, "MEC Layer 5")
# Render the scene
scene.render()




