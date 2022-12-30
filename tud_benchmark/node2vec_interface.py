import networkx as nx
import gensim
from node2vec import Node2Vec

def generate_node2vec(G, embedding_dims = 64, walk_length = 30, num_walks = 200, p = 1, q = 1):
    G_node2vec = []
    embedding_dims = 64
    walk_length = 30
    num_walks = 200

    for i,graph in enumerate(G):

        wv_filename = os.path.join("word_vectors","vectors{}_wl{}_dims{}.kv".format(i,walk_length,embedding_dims))
        if not os.path.exists(wv_filename):
            node2vec = Node2Vec(graph, dimensions=embedding_dims, walk_length=walk_length, num_walks=num_walks, workers=4)

        # Embed nodes
            model = node2vec.fit(window=10, min_count=1, batch_words=4)  
            model.wv.save(wv_filename)
            G_node2vec.append(model.wv.get_normed_vectors())
        else:
            loaded_wv = KeyedVectors.load(wv_filename,mmap='r')
            G_node2vec.append(loaded_wv.get_normed_vectors())
    return G_node2vec

def generate_node2vec_embeddings(G,G_node2vec,embedding_dims):
    node2vec_embeddings = {}

    node2vec_sums = np.zeros((len(G),embedding_dims))
    for i,embedding in enumerate(G_node2vec):
        node2vec_sums[i] = embedding.sum(axis=0)
    node2vec_embeddings["sum"] = node2vec_sums 

    node2vec_means = np.zeros((len(G),embedding_dims))
    for i,embedding in enumerate(G_node2vec):
        node2vec_means[i] = embedding.mean(axis=0)
    node2vec_embeddings["mean"] = node2vec_means

    node2vec_sd = np.zeros((len(G),embedding_dims))
    for i,embedding in enumerate(G_node2vec):
        node2vec_sd[i] = embedding.std(axis=0)
    node2vec_embeddings["sd"] = node2vec_sd
    node2vec_embeddings["sum_mean_sd"] = np.hstack([node2vec_sums, node2vec_means,node2vec_sd])

    return node2vec_embeddings
