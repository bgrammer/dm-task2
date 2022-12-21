import nrkmeans
import sklearn
from sklearn.metrics import normalized_mutual_info_score


def nrkmeans_batch(data, labels, clusters = 20):
    '''
    Get dict of arrays, return dict of nmis
    '''
    nmis = {}
    y_preds = {}
    for name,gram in data.items():
        new_name = name+"_nrkmeans"
        nrkm = nrkmeans.NrKmeans(n_clusters=[clusters,1], allow_larger_noise_space=True)
        nrkm.fit(gram, best_of_n_rounds=10)
        nmis[new_name] = normalized_mutual_info_score(nrkm.labels[0],labels) 
        y_pred[new_name] = nrkm.labels[0] 
    return nmis,y_preds

def agglomerative_batch(data,labels,clusters = 20,linkage="complete"):
    #‘ward’, ‘complete’, ‘average’, ‘single’
    nmis = {}
    y_preds = {}
    
    for name,gram in data.items():
        new_name = name+"_aggl_"+linkage
        agglm = sklearn.cluster.AgglomerativeClustering(n_clusters=clusters, linkage=linkage)
        agglm.fit(gram)
        nmis[new_name] = normalized_mutual_info_score(agglm.labels_,labels)
        y_preds[new_name] = agglm.labels_
    return nmis,y_preds

def spectral_clustering_batch(data,labels,assign_labels = "cluster_qr", affinity = 'precomputed', clusters = 20):
    nmis = {}
    y_preds = {}

    for name,gram in data.items():
        new_name = name+"_spectral"
        sc = sklearn.cluster.SpectralClustering(affinity = affinity, assign_labels = assign_labels, n_clusters=clusters)
        sc.fit(gram)
        nmis[new_name] = normalized_mutual_info_score(sc.labels_,labels)
        y_preds[new_name] = sc.labels_
    return nmis,y_preds

def dbscan_batch(data,labels,eps,min_samples):
    nmis = {}
    y_preds = {}
    for name,gram in data.items():
        new_name = name + "_dbscan"
        dbscan = sklearn.cluster.DBSCAN(eps=eps,min_samples=min_samples)
        dbscan.fit(gram)
        nmis[new_name] = normalized_mutual_info_score(dbscan.labels_,labels)
        y_preds[new_name] = dbscan.labels_
    return nmis,y_preds

def birch_batch(data,labels,threshold = 0.5, branching_factor = 50, clusters = 20):
    nmis = {}
    y_preds = {}
    for name,gram in data.items():
        new_name = name + "_birch"
        birch = sklearn.cluster.Birch(threshold = threshold,
                                      branching_factor = branching_factor, n_clusters=clusters)
        y_pred = birch.fit_predict(gram)
        nmis[new_name] = normalized_mutual_info_score(labels,y_pred)
        y_preds[new_name] = y_pred
    return nmis,y_preds

def affinity_batch(data,labels, preference = None):
    nmis = {}
    y_preds = {}
    for name,gram in data.items():
        new_name = name + "_birch"
        birch = sklearn.cluster.AffinityPropagation(preference = preference)
        y_pred = birch.fit_predict(gram)
        nmis[new_name] = normalized_mutual_info_score(labels,y_pred)
        y_preds[new_name] = y_pred
    return nmis,y_preds

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
