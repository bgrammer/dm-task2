import os
import re
from subprocess import Popen, PIPE
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.metrics import normalized_mutual_info_score

DATA_FILE_NAME = "data.tsv"
# Install Java and download the elki bundle https://elki-project.github.io/releases/release0.7.5/elki-bundle-0.7.5.jar
ELKI_JAR = "elki-bundle-0.7.5.jar"


def elki_clique(X, tau= 0.2, xsi = 10, prune = "true"):
    """Perform COPAC clustering implemented by ELKI package.
       The function calls jar package, which must be accessible through the
       path stated in ELKI_JAR constant.

        Parameters
        ----------
        X : array of shape (n_samples, n_features)
            A feature array.
        tau : float, optional, default=0.2
            Clustering threshold for determining dense units. A unit in the CLIQUE grid is considered dense if it contains more than this fraction of the total points. 
        xsi : int, optional, default=10
            Number of subdivision in the CLIQUE grid cluster. Each dimension is split into xsi number of equal intervals.
        prune: string, optional, default=true
            Use pruning during the implementation of the algorithm to speed up computation. Use "false" to return all clusters.
       
        Returns
        -------
        clusters : dict 
            Dictionary of clusters with their dimensions, extent(dense unit intervals) and point labels.
        predictions : dict
            Dictionary of prediction with dimensions as key and Y predictions as value. Outliers are labelled with -1.
    """
    # write data into tsv file
    np.savetxt(DATA_FILE_NAME, X, delimiter=",", fmt="%.6f")
    print("Run elki")
    # run elki with java
    # You can find the read of the names of the parameters for the COPAC algorithm from the elki GUI
    process = Popen(["java", "-cp", ELKI_JAR, "de.lmu.ifi.dbs.elki.application.KDDCLIApplication",
                     "-algorithm", "clustering.subspace.CLIQUE",
                     "-dbc.in", "data.tsv",
                     "-parser.colsep", ",",
                     "-clique.xsi", str(xsi),
                     "-clique.tau", str(tau),
                     "-clique.prune", str(prune)],
                    stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if exit_code != 0:
        raise IOError("Elki implementation failed to execute: \n {}".format(output.decode("utf-8")))

    # remove data file
    os.remove(DATA_FILE_NAME)

    # parse output
    elki_output = output.decode("utf-8")
    #print(elki_output)
    # initialize array of ids and labels
    # for each cluster, split by regex from output
    clusters = []
    
    for i, cluster in enumerate(elki_output.split("Cluster: Cluster")[1:]):
        cluster_info = {}
        cluster_info["id"] = i
        # find point coordinates in output
        IDs_list = re.findall(r"ID=(\d+)", cluster)
        extent = re.findall(r"d(\d):\[(\-*\d+\.\d+)\;\s(\-*\d+\.\d+)\)",cluster)
        
        dimensions = re.findall(r"Dimensions: \[(.*)\]",cluster)
        #print(dimensions)
        split_string = r",\s"
        dimensions = tuple(re.split(split_string,dimensions[0]))
        #print(dimensions)
        
        cluster_info["dimension"] = dimensions
        cluster_info["extent"] = extent
        #print("cluster: {}".format(i))
        # create a numpy array
        IDs = np.array(IDs_list, dtype="i").reshape(-1, 1)
        # append label
        IDs_and_labels = np.hstack((IDs, np.repeat(i, len(IDs_list)).reshape(-1, 1)))
        # append to matrix
        cluster_info["id_and_label"] = IDs_and_labels
        clusters.append(cluster_info)
        #print(IDs_and_labels)
        #Y_pred = np.array([]).reshape(0, 2)
        #Y_pred = np.vstack((Y_pred, IDs_and_labels))
        #print(Y_pred)
    prediction = {}
    
    for cluster in clusters:
        #print("Dimension:")
        #print(cluster["dimension"])
        #print("Id and label size:")
        #print(cluster["id_and_label"].size)
        #print(cluster["id_and_label"])
        dimension = cluster["dimension"]
        if dimension not in prediction.keys():
            prediction[dimension] = cluster["id_and_label"]
        else:
            prediction[dimension] = np.vstack((prediction[dimension],cluster["id_and_label"]))
    
    point_counts = {}
    for dimension,labels in prediction.items():
        #print(labels[:,0].size)
        if dimension not in point_counts.keys():
            point_counts[dimension] = labels[:,0].size
        else:
            point_counts[dimension] += labels[:,0].size
        Y_preds = np.full((X.shape[0],1),-1)
        #Y_preds[:,0] = np.arange(X.shape[0])
        Y_preds[labels[:,0]-1,0] = labels[:,1]
        prediction[dimension] = Y_preds

    print("Found {} clusters in {} subspaces".format(len(clusters),len(prediction)))
    #print(point_counts)
    return clusters, prediction

