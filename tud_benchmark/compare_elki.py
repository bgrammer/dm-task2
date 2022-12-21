def compare_elki(xi, tau, X):
    
    ELKI_JAR = "elki-bundle-0.7.5.jar"
    
    np.savetxt("data.tsv", X, delimiter=",", fmt="%.5f")
    
    process = Popen(["java", "-cp", ELKI_JAR, "de.lmu.ifi.dbs.elki.application.KDDCLIApplication",
                     "-algorithm", "clustering.subspace.CLIQUE",
                     "-dbc.in", "data.tsv",
                     "-parser.colsep", ",",
                     "-clique.xsi", str(xi),
                     "-clique.tau", str(tau),
                     "-clique.prune", 'false'],
                    stdout=PIPE)
    
    (output, err) = process.communicate()
    
    os.remove("data.tsv")
    
    elki_output = output.decode("utf-8")    
    
    # create a dictionary to store lists of point ids of clusters in different subspaces
    diction = defaultdict(lambda : list())
    
    # for each cluster, split by regex from output
    for cluster in elki_output.split("Dimensions:")[1:]:
        # find dimension where cluster is in
        dim = frozenset([int(s)-1 for x in [r[1:-1].split(',') for r in re.findall(r"\[\d.*\]",cluster)] for s in x])
        # find point coordinates in output
        IDs_list = re.findall(r"ID=(\d+)", cluster)
        # create a numpy array
        IDs = np.array(IDs_list, dtype="i")    
        # use subspace dimension as key and list of point ids (each list represents a cluster) as values
        diction[dim].append(np.sort(IDs, axis=0))

    # dictionary to transform results in order to compare them better to our results
    res = dict()

    for key in diction.keys():
        # create for each subspace a np.array filled with -1 (-1 = noise)
        label = np.full(X.shape[0], -1)
        # iterate over list of point ids and assign cluster id to all points in a cluster
        for i, cluster in enumerate(diction[key]):
            for point in cluster:
                label[point-1] = i
        res[frozenset(key)] = label
    
    # run our algorithm with input data
    clique_instance = Clique(xi, tau, X)
    clique_instance.process()
    res_implem = clique_instance.get_labels()
    
    nmis = list()
    
    # compare clustering in each subspace using nmi
    if res.keys() == res_implem.keys():
        for key in res.keys():
            nmis.append(nmi(res[key], res_implem[key]))
    else:
        del clique_instance
        return "subspaces different"
    
    del clique_instance
    # return the elki output, all nmi results and the results of both algorithms
    return  elki_output, nmis, res, res_implem

