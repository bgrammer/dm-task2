import numpy as np
from sklearn.decomposition import KernelPCA, TruncatedSVD
import os
import pandas as pd
import re
import auxiliarymethods.auxiliary_methods as aux
from scipy.sparse import load_npz


def load_csv(path):
    return np.loadtxt(path, delimiter=";")

def load_sparse(path):
    return load_npz(path)

def select_from_list(l, indices):
    return [l[i] for i in indices]

def load_grams(base_path, ds_name):
    '''
    Returns a dict of gram representations of MSRC_21 image set.
    '''
    
    data = {}

    for i in range(1,6):
        gram = load_csv(os.path.join(base_path,f"{ds_name}_gram_matrix_wl{i}.csv"))
        gram = aux.normalize_gram_matrix(gram)
        data["wl"+str(i)] = gram
    
    gram = load_csv(os.path.join(base_path, "MSRC_21_gram_matrix_graphlet.csv"))
    gram = aux.normalize_gram_matrix(gram)
    data["graphlet"] = gram
        
    gram = load_csv(os.path.join(base_path, "MSRC_21_gram_matrix_shortestpath.csv"))
    gram = aux.normalize_gram_matrix(gram)
    data["shortest_path"] = gram
    return data

def load_vectors(base_path,ds_name):
    '''
    Returns a dict of vector representations of MSRC_21 image set.
    '''
    
    data = {}
    for i in range(1,6):
        data["wl"+str(i)] = load_sparse(os.path.join(base_path,f"{ds_name}_vectors_wl{i}.npz"))

    data["shortest_path"] = load_sparse(os.path.join(base_path,"MSRC_21_vectors_shortestpath.npz"))
    data["graphlet"] = load_sparse(os.path.join(base_path,"MSRC_21_vectors_graphlet.npz"))
    return data
    
def kernel_pcas(gram_dict, kernel = "precomputed", dims = 100):
    '''
    Apply KernelPCA to a dictionary of gram matrices.
    '''
    kpca = KernelPCA(n_components=dims, kernel= kernel)
    
    kpca_grams = {}
    
    for name,gram in gram_dict.items():
        reduced_kpca = kpca.fit_transform(gram)
        kpca_grams[name+"_kpca_"+str(dims)] = reduced_kpca
    
    return kpca_grams

def trunc_svds(vector_dict, dims=100):
    '''
    Apply Truncated SVD to a dictionary of sparse vectors.
    '''
    trunc_svds = {}
    explained_variance = {}
    
    for name,vector in vector_dict.items():
        tsvd = TruncatedSVD(n_components=dims)
        reduced_tsvd = tsvd.fit_transform(vector)
        trunc_svds[name+"_svd_"+str(dims)] = reduced_tsvd
        explained_variance[name+"_svd_"+str(dims)] = tsvd.explained_variance_ratio_
    return trunc_svds,explained_variance

def create_img_index_by_class(classes):
    id2img = pd.read_csv(os.path.join(os.getcwd(),"datasets","MSRC_21","MSRC_21","raw","MSRC_21_map_id2im.csv"), sep='\t',header=None)
    file_names = np.array(id2img[1])
    converted_filenames = np.full_like(file_names,"")
    #print(converted_filenames.shape)
    for i in range(0,len(file_names)):
        #image = Image.open(os.path.join(os.getcwd(),"Images",file_names[i]))
        pattern = r'(.*)\.bmp'
        result = re.match(pattern, file_names[i]).group(1)
        new_filename = result+".png"
        #image.save("Images/"+ new_filename)
        converted_filenames[i] = new_filename
    file_classes = np.vstack([converted_filenames,classes]).T
    return file_classes
