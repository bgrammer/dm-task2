from networkx.readwrite import json_graph
from copy import deepcopy
import json
from scipy.io import loadmat

def export_nx_to_json(G):
    for i,graph in enumerate(G):
        data = deepcopy(nx.node_link_data(graph))
        data["graph"]["clique_label_hist"] = data["graph"]["clique_label_hist"].tolist()
        data["graph"]["degree_hist"] = data["graph"]["degree_hist"].tolist()
        data["graph"]["node_label_hist"] = data["graph"]["node_label_hist"].tolist()
        data["graph"]["tree_width"] = None
        s = json.dumps(data)
        filename = "msrc21_{}.json".format(i)
        with open(filename, "w") as file:
            file.write(s)



def load_mat_obj(G):
    spectralmix_embeddings = []
    spectralmix_aggr = {}
    for i in range(0,len(G)):
        filename = "objCoord-msrc21-100D-50e5g"+str(i)+".mat"
        mat = loadmat(os.path.join("spectralmixpublic-master","SpectralMix","embeddings","noattr",filename))
        embedding = mat["objCoord"]
        spectralmix_embeddings.append(embedding)

    sm_sums = np.zeros((len(G),100))
    for i,embedding in enumerate(spectralmix_embeddings):
        sm_sums[i] = embedding.sum(axis=0)
    spectralmix_aggr["sum"] = sm_sums

    sm_means = np.zeros((len(G),100))
    for i,embedding in enumerate(spectralmix_embeddings):
        sm_means[i] = embedding.mean(axis=0)
    spectralmix_aggr["mean"] = sm_means

    sm_sd = np.zeros((len(G),100))
    for i,embedding in enumerate(spectralmix_embeddings):
        sm_sd[i] = embedding.std(axis=0)
    spectralmix_aggr["sd"] = sm_sd

    spectralmix_aggr["sum_mean_sd"] = np.hstack([sm_sums,sm_means,sm_sd])
    
    return spectralmix_aggr

def load_mat_obj_attr(G):

    spectralmix_embeddings_attr = []
    spectralmix_embeddings_cats = []
    spectralmix_aggr_attr = {}

    for i in range(0,len(G)):
        filename = "objCoord-msrc21-100D-50e5g"+str(i)+".mat"
        mat = loadmat(os.path.join("spectralmixpublic-master","SpectralMix","embeddings",filename))
        embedding = mat["objCoord"]

        filename_cat = "objCat-msrc21-100D-50e5g"+str(i)+".mat"
        cats = loadmat(os.path.join("spectralmixpublic-master","SpectralMix","embeddings",filename_cat))
        embedding_cats = cats["catCoord"]
        #stacked_embeddings = np.vstack([embedding,embedding_cats])
        spectralmix_embeddings_attr.append(embedding)
        spectralmix_embeddings_cats.append(embedding_cats)

    sm_sums = np.zeros((len(G),200))
    for i,embedding in enumerate(spectralmix_embeddings_attr):
        sm_sums[i,0:100] = embedding.sum(axis=0)
    for i,embedding in enumerate(spectralmix_embeddings_cats):
        sm_sums[i,100:] = embedding.sum(axis=0)
    spectralmix_aggr_attr["sum"] = sm_sums

    sm_means = np.zeros((len(G),200))
    for i,embedding in enumerate(spectralmix_embeddings_attr):
        sm_means[i,:100] = embedding.mean(axis=0)
    for i,embedding in enumerate(spectralmix_embeddings_cats):
        sm_means[i,100:] = embedding.mean(axis=0)
    spectralmix_aggr_attr["mean"] = sm_means

    sm_sd = np.zeros((len(G),200))
    for i,embedding in enumerate(spectralmix_embeddings_attr):
        sm_sd[i,:100] = embedding.std(axis=0)
    for i,embedding in enumerate(spectralmix_embeddings_cats):
        sm_sd[i,100:] = embedding.std(axis=0)
    spectralmix_aggr_attr["sd"] = sm_sd

    spectralmix_aggr_attr["sum_mean_sd"] = np.hstack([sm_sums,sm_means,sm_sd])
    
    return spectralmix_aggr_attr
