import numpy as np
import networkx as nx

def enhance_embeddings(G,node2vec_embeddings,spectralmix_aggr,spectralmix_aggr_attr,pagerank_label_hist_all,clustering_label_hist_all):
    
    node_label_hist = np.zeros((len(G),25))
    degree_hist = np.zeros((len(G),24))
    tree_widths = np.zeros((len(G),1))
    connectivities = np.zeros((len(G),1))
    clique_hist = np.zeros((len(G),25))
    no_nodes = np.zeros((len(G),1))
    no_edges = np.zeros((len(G),1))
    pagerank_hist = np.zeros((len(G),20))

    for i,graph in enumerate(G):
        node_label_hist[i,:] = graph.graph["node_label_hist"]
        degree_hist[i,:] = graph.graph["degree_hist"]
        tree_widths[i,:] = graph.graph["tree_width"][0]
        connectivities[i,:] = graph.graph["connectivity"]
        clique_hist[i,:] = graph.graph["clique_label_hist"]
        no_nodes[i,:] = graph.graph["nodes"]
        no_edges[i,:] = graph.graph["edges"]
        pagerank_hist[i,:] = np.histogram(list(nx.get_node_attributes(graph,"pagerank").values()),20)[0]

    node2vec_enhanced = {}

    # don't judge

    #All graph properties without node label information
    node2vec_enhanced["sum_all_without_node_labels"] = np.hstack([node2vec_embeddings["sum"],pagerank_hist,no_nodes,no_edges,tree_widths,connectivities,degree_hist])

    #Combination of properties
    node2vec_enhanced["sum_label_hist"] = np.hstack([node2vec_embeddings["sum"],node_label_hist])
    node2vec_enhanced["sum_label_degree_hist"] = np.hstack([node2vec_embeddings["sum"],node_label_hist,degree_hist])
    node2vec_enhanced["sum_label_hist_tree_width"] = np.hstack([node2vec_embeddings["sum"],node_label_hist,tree_widths])
    node2vec_enhanced["sum_all"] = np.hstack([node2vec_embeddings["sum"],no_nodes,no_edges,clique_hist,node_label_hist,tree_widths,connectivities,degree_hist,pagerank_hist])

    # Node label information only
    node2vec_enhanced["sum_clique_label_only"] = np.hstack([node2vec_embeddings["sum"],clique_hist])
    node2vec_enhanced["sum_pagerank_label_only"] = np.hstack([node2vec_embeddings["sum"],pagerank_label_hist_all])
    node2vec_enhanced["mean_clique_node_label"] = np.hstack([node2vec_embeddings["mean"],clique_hist,node_label_hist])
    node2vec_enhanced["sum_clique_node_label"] = np.hstack([node2vec_embeddings["sum"],clique_hist,node_label_hist])
    node2vec_enhanced["sum_mean_sd_labels"] = np.hstack([node2vec_embeddings["sum_mean_sd"],clique_hist,node_label_hist])
    node2vec_enhanced["mean_all_label_hist"] = np.hstack([node2vec_embeddings["mean"],clustering_label_hist_all,node_label_hist,clique_hist])
    node2vec_enhanced["mean_all_label_pagerank_hist"] = np.hstack([node2vec_embeddings["mean"],clustering_label_hist_all,node_label_hist,clique_hist,pagerank_label_hist_all])
    node2vec_enhanced["sd_all_label_pagerank_hist"] = np.hstack([node2vec_embeddings["sd"],clustering_label_hist_all,node_label_hist,clique_hist,pagerank_label_hist_all])
    node2vec_enhanced["mean_all_hist_all_properties"] = np.hstack([node2vec_embeddings["mean"],no_nodes,no_edges,clique_hist,node_label_hist,tree_widths,connectivities,degree_hist,pagerank_hist,
                                                             clustering_label_hist_all,pagerank_label_hist_all])
    sm_enhanced = {}

    #All graph properties without node label information
    sm_enhanced["sum_all_without_node_labels"] = np.hstack([spectralmix_aggr["sum"],pagerank_hist,no_nodes,no_edges,tree_widths,connectivities,degree_hist])

    #Combination of properties
    sm_enhanced["sum_label_hist"] = np.hstack([spectralmix_aggr["sum"],node_label_hist])
    sm_enhanced["sum_label_degree_hist"] = np.hstack([spectralmix_aggr["sum"],node_label_hist,degree_hist])
    sm_enhanced["sum_label_hist_tree_width"] = np.hstack([spectralmix_aggr["sum"],node_label_hist,tree_widths])
    sm_enhanced["sum_all_properties_node_label"] = np.hstack([spectralmix_aggr["sum"],no_nodes,no_edges,clique_hist,node_label_hist,tree_widths,connectivities,degree_hist,pagerank_hist])

    # Node label information only
    sm_enhanced["sum_clique_label_only"] = np.hstack([spectralmix_aggr["sum"],clique_hist])
    sm_enhanced["sum_pagerank_label_only"] = np.hstack([spectralmix_aggr["sum"],pagerank_label_hist_all])
    sm_enhanced["mean_clique_node_label"] = np.hstack([spectralmix_aggr["mean"],clique_hist,node_label_hist])
    sm_enhanced["sum_clique_node_label"] = np.hstack([spectralmix_aggr["sum"],clique_hist,node_label_hist])
    sm_enhanced["sum_mean_sd_labels"] = np.hstack([spectralmix_aggr["sum_mean_sd"],clique_hist,node_label_hist])
    sm_enhanced["mean_all_label_hist"] = np.hstack([spectralmix_aggr["mean"],clustering_label_hist_all,node_label_hist,clique_hist,pagerank_label_hist_all])
    sm_enhanced["sd_all_label_hist"] = np.hstack([spectralmix_aggr["sd"],clustering_label_hist_all,node_label_hist,clique_hist,pagerank_label_hist_all])

    sm_enhanced["mean_all_hist_all_properties"] = np.hstack([spectralmix_aggr["mean"],no_nodes,no_edges,clique_hist,node_label_hist,tree_widths,connectivities,degree_hist,pagerank_hist,
                                                             clustering_label_hist_all,pagerank_label_hist_all])

    sm_enhanced_attr = {}

    #All graph properties without node label information
    sm_enhanced_attr["sum_all_without_node_labels"] = np.hstack([spectralmix_aggr_attr["sum"],pagerank_hist,no_nodes,no_edges,tree_widths,connectivities,degree_hist])

    #Combination of properties
    sm_enhanced_attr["sum_label_hist"] = np.hstack([spectralmix_aggr_attr["sum"],node_label_hist])
    sm_enhanced_attr["sum_label_degree_hist"] = np.hstack([spectralmix_aggr_attr["sum"],node_label_hist,degree_hist])
    sm_enhanced_attr["sum_label_hist_tree_width"] = np.hstack([spectralmix_aggr_attr["sum"],node_label_hist,tree_widths])
    sm_enhanced_attr["sum_all_properties_node_label"] = np.hstack([spectralmix_aggr_attr["sum"],no_nodes,no_edges,clique_hist,node_label_hist,tree_widths,connectivities,degree_hist,pagerank_hist])

    # Node label information only
    sm_enhanced_attr["sum_clique_label_only"] = np.hstack([spectralmix_aggr_attr["sum"],clique_hist])
    sm_enhanced_attr["sum_pagerank_label_only"] = np.hstack([spectralmix_aggr_attr["sum"],pagerank_label_hist_all])
    sm_enhanced_attr["mean_clique_node_label"] = np.hstack([spectralmix_aggr_attr["mean"],clique_hist,node_label_hist])
    sm_enhanced_attr["sum_clique_node_label"] = np.hstack([spectralmix_aggr_attr["sum"],clique_hist,node_label_hist])
    sm_enhanced_attr["sum_mean_sd_labels"] = np.hstack([spectralmix_aggr_attr["sum_mean_sd"],clique_hist,node_label_hist])
    sm_enhanced_attr["mean_all_label_hist"] = np.hstack([spectralmix_aggr_attr["mean"],clustering_label_hist_all,node_label_hist,clique_hist,pagerank_label_hist_all])
    sm_enhanced_attr["sd_all_label_hist"] = np.hstack([spectralmix_aggr_attr["sd"],clustering_label_hist_all,node_label_hist,clique_hist,pagerank_label_hist_all])

    sm_enhanced_attr["mean_all_hist_all_properties"] = np.hstack([spectralmix_aggr_attr["mean"],no_nodes,no_edges,clique_hist,node_label_hist,tree_widths,connectivities,degree_hist,pagerank_hist,
                                                             clustering_label_hist_all,pagerank_label_hist_all])

    node_labels_only = {"no_embedding_labels_only" : node_label_hist}


    return node2vec_enhanced,sm_enhanced, sm_enhanced_attr, node_labels_only
