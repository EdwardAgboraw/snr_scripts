# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 17:08:03 2025

@author: edwar
"""

#adding structural information to neurons in
#ent_data_20241022

import pandas as pd

#load neuron data

neuron = pd.read_csv("scripts/1_trans.csv")

#get ntype information

ntype = neuron["Ntype"]

#format Structure column
structure = []

for x in ntype:
    if x == 0:
        structure.append("undefined")
    if x == 1:
        structure.append("soma")
    if x == 2:
        structure.append("axon")
    if x == 3:
        structure.append("(basal) dendrite")
    if x == 4:
        structure.append("apical dendrite")
    if x == 5:
        structure.append("axon fork point")
    if x == 6:
        structure.append("axon end point")
    if x == 7:
        structure.append("(basal) dendrite end point")
    if x == 8:
        structure.append("apical dendrite end point")
    if x == 11:
        structure.append("(basal) dendrite fork point")
    if x == 12:
        structure.append("apical dendrite fork point")
 
#add structure information
neuron["Structure"] = structure

#save information
neuron.to_csv("scripts/1_trans.csv")
