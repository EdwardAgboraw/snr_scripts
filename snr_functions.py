# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 10:15:24 2025

@author: edwar

Library of custom functions created for the analysis and visualization
of single-neuron reconstruction data
"""

import pandas as pd
import numpy as np

def extract_soma(data_path, num_files):
    
    #open data directory
    #extra soma information from all _trans.csv files
    #save soma coordiantes to list of lists
    #convert into numpy float32 array
    
    upper_lim = num_files + 1
    
    all_soma = []
    
    #get all soma coordinates
    for x in range(1,upper_lim):
        
        file_name = str(x) + "_trans.csv"
        
        file_path = data_path + file_name
        
        n = pd.read_csv(file_path, nrows = 1)
        
        #convert to 25x25x25 resolution
        soma_coords = [n["x"][0]* 25,
                       n["y"][0]* 25,
                       n["z"][0]* 25]
    
        all_soma.append(soma_coords)
        
    #convert to numpy float 32 array
    all_soma = np.asarray(all_soma, dtype=np.float32)
    
    return(all_soma)

def get_coords_from_aws(dataset):
    
    all_coords = []
    
    for index, row in dataset.iterrows():
        x = row["x_ccf"] * 1000
        y = row["y_ccf"] * 1000
        z = row["z_ccf"] * 1000
        
        coords = [x,y,z]
        
        all_coords.append(coords)

    all_coords = np.asarray(all_coords, dtype=np.float32)
    
    return(all_coords)