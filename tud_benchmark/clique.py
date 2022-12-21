import numpy as np
from typing import Dict, List, FrozenSet
from scipy.sparse.csgraph import connected_components
from collections import defaultdict

Subspace = FrozenSet[int]
Unit = Dict[int,int]
Cluster = List[int]
ClustersOfSupspaces = Dict[Subspace,List[Cluster]]
DenseUnitsOfSubspaces = Dict[Subspace, List[Unit]]
LabelsOfSubspaces = Dict[Subspace,List[int]]

class Clique:

  subspace_clusters: ClustersOfSupspaces = dict()

  def __init__(self, xi: int, tau: float, data: np.ndarray) -> None:
    if tau < 1:
      self.tau = tau * data.shape[0]
    else:
      self.tau = tau
    self.xi = xi
    normalized_data = self.__normalize_data(data.copy())
    self.data_units = self.__transform_data_to_units(normalized_data).astype(int)
    self.numbers_of_datapoints = data.shape[0]
    self.numbers_of_features = data.shape[1]

  def __del__(self):
    self.subspace_clusters.clear()

  def __normalize_data(self,data: np.ndarray) -> np.ndarray:
    """
    normalized data between [0, 1). Not including 1 as our algorithm does not check 1
    to ensure this we add a small number to our maximum of the features 
    """
    minimum = np.amin(data,axis=0)
    data = data - minimum
    maximum = np.amax(data, axis=0) +1e-7
    return data / maximum

  def __transform_data_to_units(self, data: np.ndarray) -> np.ndarray:
    """
    transforms normalized data to its assigned unit over all features
    No need to get value. Only interested in which unit a datapoint is.
    """
    return data // (1/self.xi)

  def process(self) -> None:
    """
    Performs Clique Algorithm
    1.Find one dimensional Dense Units
      1.1.Count Number of Points in Unit
      1.2.Select Units that exceed threshold
    2.Find Clusters
      2.1 Construct Adjacency Matrix
      2.2. Find Connected Dense Units (Clusters)
      2.3. Assign Points to Clusters
    3.Find higher dimensional Dense Units
      3.1.Join lower dimensional Units
      3.2.Prune Candidates
      3.3.Count Number of Points in Unit
      3.4.Select Units that exceed threshold
    4.Find Clusters  (same as 2)
    """
    dense_units = self.__find_one_dimensional_dense_units()
    self.subspace_clusters.update(self.__find_clusters(dense_units))
    for dimension  in range(2, self.numbers_of_features+1):
      if len(dense_units) == 0:
        break
      dense_units = self.__find_n_dimensional_dense_units(dimension, dense_units)
      self.subspace_clusters.update(self.__find_clusters(dense_units))

  def __join_dense_units(self, previous_dense_units: List[Unit],dim) -> List[Unit]:
    """
    joins units if they have dim-2 dimensions in common
    """
    candidates =  np.array([])
    for i in range(len(previous_dense_units)):
      for j in range(i + 1, len(previous_dense_units)):
        joined_dense_unit = {**previous_dense_units[i], **previous_dense_units[j]}
        if len(joined_dense_unit.keys()) != dim:
          continue

        add_to_candidates = True
        for feature,unit in previous_dense_units[i].items():
          if feature in previous_dense_units[j].keys():
            if unit != previous_dense_units[j][feature]:
              add_to_candidates = False
              break

        if add_to_candidates:
          if joined_dense_unit not in candidates:
            candidates = np.append(candidates, joined_dense_unit)

    return candidates

  def __prune(self,previous_dense_units: List[Unit], candidates: List[Unit]) -> List[Unit]:
    """
    reduces candidates of dense unit by downward closure principle.
    """
    removing_candidates = np.array([], dtype = np.int64)
    for i in range(len(candidates)):
      projected_units = self.__get_all_unit_projections_one_dim_lower(candidates[i])
      for projected_unit in projected_units:
        if projected_unit not in previous_dense_units:
          np.append(removing_candidates, i)
          break

    pruned_candidates = np.delete(candidates, removing_candidates)
    return pruned_candidates

  def __is_in_unit(self, datapoint: np.ndarray, unit: Unit):
    """
    checks if datapoint is in unit
    """
    for feature, unit_id in unit.items():
      if datapoint[feature] != unit_id:
        return False
    return True


  def __get_points_of_cluster(self, dense_units: List[Unit]):
    """
    gets point indexes that are in a dense unit
    """
    point_ids = []
    for i, datapoint in enumerate(self.data_units):
      for unit in dense_units:
        if self.__is_in_unit(datapoint, unit):
          point_ids.append(i)
          break
    
    return point_ids


  def __get_all_unit_projections_one_dim_lower(self,unit: Unit) -> List[Unit]:
    """
    generates all unit projections that are one dimension lower than the unit
    """
    projected_units: List[Unit] = np.array([])
    for feature in unit.keys():
      projected_unit = unit.copy()
      projected_unit.pop(feature)
      projected_units = np.append(projected_units, projected_unit)
    return projected_units

  def __find_one_dimensional_dense_units(self) -> DenseUnitsOfSubspaces:
    """
    Finds dense Units by counting Number of points in each unit and finding units that exceed threshold
    """
    units_counts = np.zeros((self.numbers_of_features, self.xi))
    one_dim_dense_units = np.array([])
    for feature in range(self.numbers_of_features):
      units, counts = np.unique(self.data_units[:,feature], return_counts = True)
      units_counts[feature, units] = counts

    features, units = np.where(units_counts >= self.tau)

    for i, feature in enumerate(features):
      dense_unit = dict({feature : units[i]})
      one_dim_dense_units = np.append(one_dim_dense_units, dense_unit)
    
    return one_dim_dense_units 

  def __find_n_dimensional_dense_units(self,dim, previous_dense_units: List[Unit]) -> DenseUnitsOfSubspaces:
    """
    Finds higher dimensional dense units by first joining lower dimensional dense units and pruning them.
    Afterward the number of point in each unit are counted. Candidates exceeding the threshold are dense units.
    """
    candidates = self.__join_dense_units(previous_dense_units,dim)

    if dim > 2:
      pruned_candidates = self.__prune(previous_dense_units,candidates)
    else: 
      pruned_candidates = candidates

    units_counts = np.zeros(pruned_candidates.shape[0])
    for datapoint in self.data_units:
      for i in range(candidates.shape[0]):
          if self.__is_in_unit(datapoint, candidates[i]):
                units_counts[i] += 1

    dense_units = pruned_candidates[np.where(units_counts >= self.tau)]
    return dense_units

  def __find_clusters(self,dense_units: List[Unit]) -> ClustersOfSupspaces:
    """
    Finds Clusters of dense units. First it builds a adjecency matrix. Afterwards it findes connected dense units and groups them
    to a Cluster. For each cluster the datapoints of the cluster are assigned.
    """
    clusters = defaultdict(list)
    matrix = self.__generate_adjacency_matrix(dense_units)
    n_components, labels = connected_components(matrix, directed=False)

    for cluster_idx in range(n_components):
      dense_unit_cluster = dense_units[np.where(labels == cluster_idx)]

      subspace =  frozenset(dense_unit_cluster[0].keys())

      point_cluster = self.__get_points_of_cluster(dense_unit_cluster)
      clusters[subspace].append(point_cluster)
      
    return clusters

  def __generate_adjacency_matrix(self, dense_units: List[Unit]) -> np.ndarray:
    """
    generates adjacency matrix of dense units to find connected dense units
    """
    matrix = np.zeros((len(dense_units), len(dense_units)))
    for i , dense_unit_1 in enumerate(dense_units):
      for j in range(i+1, len(dense_units)):
        edge = self.__get_edge(dense_unit_1, dense_units[j])
        matrix[i, j] = edge
        matrix[j, i] = edge
    return matrix

  def __get_edge(self, unit1: Unit,unit2: Unit) -> int:
    """
    calculates the edges of the adjacency Matrix. There only exists an edge if the dense units are in the same subspace
    and if they are adjacent to each other.
    """
    if unit1.keys() != unit2.keys():
      return 0;

    distance = 0
    for feature in unit1.keys():
      distance += abs(unit1[feature] - unit2[feature])
      if distance > 1:
        return 0
    return 1

  def get_labels(self):
    """
    returns all labels for all subspaces. Noise points are labeled with -1
    """
    labels = dict()
    for subspace in self.subspace_clusters.keys():
      labels.update({subspace: self.get_labels_for_subspace(subspace)})
    return labels

  def get_labels_for_subspace(self, subspace):
    """
    returns label of subspace
    """
    subspace_key = frozenset(subspace)
    labels = np.full(self.numbers_of_datapoints, -1)
    cluster_list = self.subspace_clusters[subspace_key]

    for cluster_index, cluster_points in enumerate(cluster_list):
      labels[cluster_points] = cluster_index
    return labels
