# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 10:31:51 2025

@author: edwar

The SWC file is essentially just the first seven columns
of the CSV file.

The goal here is to edit the dataframe in the CSV file so that
it only contains the information for the soma and the axon,
and then use that dataframe to generate a new, streamlined
SWC file.

test file 
ent_data_20241022
1_trans.csv

"""

import pandas as pd

#load neuron data

neuron = pd.read_csv("scripts/1_trans.csv")

#apply Ntype filter
#1 = Soma
#2 = axon
#5 = axon fork point
#6 = axon end point

soma_axon = [1,2,5,6]

small_neuron = neuron[neuron["Ntype"].isin(soma_axon)]

#trim - only keep first seven columns

small_neuron_final = small_neuron.iloc[:,1:8]

#save data

small_neuron_final.to_csv("data/1_trans_axon_soma.csv",
                          index = False,
                          header = False)
