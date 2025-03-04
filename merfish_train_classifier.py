# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 14:05:30 2025

@author: edwar

get spatial coordinates and class/subclass/supertype/cluster information
for LEC Layer 5 cells across all Merfish datasets.

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

#multiclassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn import datasets

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

#Get cell cluster annotations

cell_annots = {}

for d in datasets :

    cell_annots[d] = abc_cache.get_metadata_dataframe(directory=d, 
                                    file_name='cell_metadata_with_cluster_annotation',
                                    dtype={"cell_label": str})
    cell_annots[d].set_index('cell_label', inplace=True)
    
meta_zh1 = cell_annots['Zhuang-ABCA-1']
meta_zh1 = meta_zh1[meta_zh1.index.isin(ccf_zh1.index)]

meta_zh2 = cell_annots['Zhuang-ABCA-2']
meta_zh2 = meta_zh2[meta_zh2.index.isin(ccf_zh2.index)]

meta_zh3 = cell_annots['Zhuang-ABCA-3']
meta_zh3 = meta_zh3[meta_zh3.index.isin(ccf_zh3.index)]

meta_zh4 = cell_annots['Zhuang-ABCA-4']
meta_zh4 = meta_zh4[meta_zh4.index.isin(ccf_zh4.index)]

#subset - only keep cell type information
meta_zh1 = meta_zh1[["class", "subclass", "supertype", "cluster"]]
meta_zh2 = meta_zh2[["class", "subclass", "supertype", "cluster"]]
meta_zh3 = meta_zh3[["class", "subclass", "supertype", "cluster"]]
meta_zh4 = meta_zh4[["class", "subclass", "supertype", "cluster"]]

#combine information
zh1_full = ccf_zh1.join(meta_zh1)
zh2_full = ccf_zh2.join(meta_zh2)
zh3_full = ccf_zh3.join(meta_zh3)
zh4_full = ccf_zh4.join(meta_zh4)

#combine into big dataset

data = [zh1_full, zh2_full, zh3_full, zh4_full]

all_data = pd.concat(data)

#remove parcellation indices

all_data = all_data.drop("parcellation_index", axis = 1)

#how many labels do we have at each level in LEC Layer 5?

classes = all_data["class"]
len(classes.unique()) # 13 unique classes

subclasses = all_data["subclass"]
len(subclasses.unique()) # 49 unique classes

supertypes = all_data["supertype"]
len(supertypes.unique()) # 140 unique classes

clusters = all_data["cluster"]
len(clusters.unique()) # 276 unique classes

#start at the Class level, and work down from there

#Split data

all_data = all_data.reset_index()

all_data_training = all_data.iloc[:9531,:]
all_data_testing = all_data.iloc[9531:,:]

#extract training data
training_labels = all_data_training["class"]
training_labels = np.array(training_labels)

training_data = []

for index, row in all_data_training.iterrows():
    x = row["x_ccf"]
    y = row["y_ccf"]
    z = row["z_ccf"]
    
    tr = [x,y,z]
    training_data.append(tr)
    
training_data = np.array(training_data)


#extract testing data

testing_labels = all_data_testing["class"]
testing_labels = np.array(testing_labels)

testing_data = []

for index, row in all_data_testing.iterrows():
    x = row["x_ccf"]
    y = row["y_ccf"]
    z = row["z_ccf"]
    
    tr = [x,y,z]
    testing_data.append(tr)
    
testing_data = np.array(testing_data)


#Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier
dtree_model = DecisionTreeClassifier(max_depth = 15).fit(training_data,
                                                        training_labels)

dtree_accuracy = dtree_model.score(testing_data, testing_labels) 
#x,y = 0.207
#x,y,z = 0.210 
# 70/30 training-test split = 0.191

#support vector machine classifier
from sklearn.svm import SVC
svm_model_linear = SVC(kernel = 'linear', C = 1).fit(training_data,
                                                     training_labels)
# model accuracy for X_test  
svm_accuracy = svm_model_linear.score(testing_data, testing_labels) 
#x,y = 0.276
#x,y,z = 0.280
# 70/30 training-test split = 0.266

# K-Nearest Neighbor (Lazy) classifier
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 7).fit(training_data, 
                                                training_labels)

knn_accuracy = knn.score(testing_data, testing_labels) 
#x,y = 0.21
#x,y,z = 0.235
# 70/30 training-test split = 0.224

#Naive Bayes classifier
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB().fit(training_data, training_labels)

gnb_accuracy = gnb.score(testing_data, testing_labels) 
# x,y = 0.271
# x,y,z = 0.257
# 70/30 training-test split = 0.258





