"""
    cancer-clustering
    
    This program takes cancer rate statistical data and clusters this data to
    plot incidence by area
"""
import math
import matplotlib.pyplot as plt
import numpy as np

# constants
DIRECTORY = "/Users/fpj/Development/python/fundamentals-computing/algorithmic-thinking/data/"
MAP_URL = DIRECTORY + "data_clustering/USA_Counties.png"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"

"""
    Cluster class for Module 3
"""
class Cluster:
    """
    Class for creating and merging clusters of counties
    """
    
    def __init__(self, fips_codes, horiz_pos, vert_pos, population, risk):
        """
        Create a cluster based the models a set of counties' data
        """
        self._fips_codes = fips_codes
        self._horiz_center = horiz_pos
        self._vert_center = vert_pos
        self._total_population = population
        self._averaged_risk = risk
        
        
    def __repr__(self):
        """
        String representation assuming the module is "alg_cluster".
        """
        rep = "alg_cluster.Cluster("
        rep += str(self._fips_codes) + ", "
        rep += str(self._horiz_center) + ", "
        rep += str(self._vert_center) + ", "
        rep += str(self._total_population) + ", "
        rep += str(self._averaged_risk) + ")"
        return rep


    def fips_codes(self):
        """
        Get the cluster's set of FIPS codes
        """
        return self._fips_codes
    
    def horiz_center(self):
        """
        Get the averged horizontal center of cluster
        """
        return self._horiz_center
    
    def vert_center(self):
        """
        Get the averaged vertical center of the cluster
        """
        return self._vert_center
    
    def total_population(self):
        """
        Get the total population for the cluster
        """
        return self._total_population
    
    def averaged_risk(self):
        """
        Get the averaged risk for the cluster
        """
        return self._averaged_risk
   
        
    def copy(self):
        """
        Return a copy of a cluster
        """
        copy_cluster = Cluster(set(self._fips_codes), self._horiz_center, self._vert_center,
                               self._total_population, self._averaged_risk)
        return copy_cluster


    def distance(self, other_cluster):
        """
        Compute the Euclidean distance between two clusters
        """
        vert_dist = self._vert_center - other_cluster.vert_center()
        horiz_dist = self._horiz_center - other_cluster.horiz_center()
        return math.sqrt(vert_dist ** 2 + horiz_dist ** 2)
        
    def merge_clusters(self, other_cluster):
        """
        Merge one cluster into another
        The merge uses the relative populations of each
        cluster in computing a new center and risk
        
        Note that this method mutates self
        """
        if len(other_cluster.fips_codes()) == 0:
            return self
        else:
            self._fips_codes.update(set(other_cluster.fips_codes()))
 
            # compute weights for averaging
            self_weight = float(self._total_population)                        
            other_weight = float(other_cluster.total_population())
            self._total_population = self._total_population + other_cluster.total_population()
            self_weight /= self._total_population
            other_weight /= self._total_population
                    
            # update center and risk using weights
            self._vert_center = self_weight * self._vert_center + other_weight * other_cluster.vert_center()
            self._horiz_center = self_weight * self._horiz_center + other_weight * other_cluster.horiz_center()
            self._averaged_risk = self_weight * self._averaged_risk + other_weight * other_cluster.averaged_risk()
            return self

    def cluster_error(self, data_table):
        """
        Input: data_table is the original table of cancer data used in creating the cluster.
        
        Output: The error as the sum of the square of the distance from each county
        in the cluster to the cluster center (weighted by its population)
        """
        # Build hash table to accelerate error computation
        fips_to_line = {}
        for line_idx in range(len(data_table)):
            line = data_table[line_idx]
            fips_to_line[line[0]] = line_idx
        
        # compute error as weighted squared distance from counties to cluster center
        total_error = 0
        counties = self.fips_codes()
        for county in counties:
            line = data_table[fips_to_line[county]]
            singleton_cluster = Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
            singleton_distance = self.distance(singleton_cluster)
            total_error += (singleton_distance ** 2) * singleton_cluster.total_population()
        return total_error
"""
    Helper functions
"""
def load_cancer_data(file_name):
    """
    Load data from unifiedCancerData spreadsheet and return list of clusters
    """
    cancer_cluster_list = []
    #
    data_file = open(file_name)
    data_text = data_file.read()
    data_lines = data_text.split('\n')
    data_lines = data_lines[ : -1]
    #
    print("load_cancer_data read in ", len(data_lines), " records")
    #
    for line in data_lines:
        fields = line.split(',')
        fips_code = int(fields[0])
        hori_cntr = float(fields[1])
        vert_cntr = float(fields[2])
        tot_popul = int(fields[3])
        aver_risk = float(fields[4])
        #
        cancer_cluster_list.append(Cluster(fips_code, hori_cntr, vert_cntr, tot_popul, aver_risk))
    #
    return cancer_cluster_list


"""
    Closest pair functions
"""    
def slow_closest_pair(cluster_list):
    """
    Find the closest pair of clusters among a list of clusters using the
    SlowClosestPair algorithm

    Args:
        cluster_list (list): A list of Cluster objects
    Returns:
        closestpair (tuple): a tuple consisting of (dist, idx1, idx2), where idx1 and idx2 are
            the indices of the two closest clusters
    """
    # set our starting distance and indices
    closest_pair = (float('inf'), -1, -1)
    #
    num_clusters = len(cluster_list)
    #
    #print("debug : slow ", num_clusters)
    for idx_u in range(num_clusters):
        for idx_v in range(num_clusters):
            if idx_u == idx_v:
                continue
            distance = cluster_list[idx_u].distance(cluster_list[idx_v])
            # print("debug - distance ", distance, "indices ", idx_u, idx_v)
            #
            if distance < closest_pair[0]:
                closest_pair = (distance, idx_u, idx_v)
    #
    #print("debug: slow ", closest_pair)
    return closest_pair
    
def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    near_cluster_list = []
    #
    #print("debug: strip : ", horiz_center, half_width)
    #
    for cluster in cluster_list:
        if math.fabs(cluster.horiz_center() - horiz_center) < half_width:
            near_cluster_list.append(cluster)
    # sort the indices in S in non-decreasing vertical coordinate order
    near_cluster_list.sort(key = lambda cluster: cluster.vert_center())
    #
    num_near_clusters = len(near_cluster_list)
    #
    #print("debug : strip : num_near_clusters ", num_near_clusters)
   #for idx in range(num_near_clusters):
        #print("debug : strip : near_cluster_list[idx] ", idx, near_cluster_list[idx])
    #
    closest_pair = (float('inf'), -1, -1)
    #
    for idx_u in range(0, num_near_clusters - 2):
        for idx_v in range(idx_u + 1, min(idx_u + 3, num_near_clusters - 1)):
            distance_uv = near_cluster_list[idx_u].distance(near_cluster_list[idx_v])
            #print("debug : strip : idx_u/idx_v/distance ", idx_u, idx_v, distance_uv)
            if distance_uv < closest_pair[0]:
                closest_pair = (distance_uv, idx_u, idx_v)
            #print("debug : strip : closes_pair ", closest_pair)
    #
    #print("debug : strip : result ", closest_pair)
    return closest_pair
    
def fast_closest_pair(sorted_cluster_list):
    """
    Find the closest pair of clusters among a list of clusters using the
    FastClosestPair algorithm

    Args:
        sorted_cluster_list (list): A sorted list of Cluster objects
    Returns:
        closestpair (tuple): a tuple consisting of (dist, idx1, idx2), where idx1 and idx2 are
            the indices of the two closest clusters
    """
    num_clusters = len(sorted_cluster_list)
    #
    if num_clusters <= 3:
        closest_pair = slow_closest_pair(sorted_cluster_list)
        #print("debug(fast) num_clusters :", num_clusters, closest_pair)
        #print("debug(fast) num_clusters <= 3 :", sorted_cluster_list)
    else:
        # find the mid-point in the list
        #print("debugsy : ", num_clusters)
        half_num_clusters = num_clusters // 2
        #print("debug : half/full", half_num_clusters, "/", num_clusters)
        # split into upper and lower lists
        lower_sorted_cluster_list = sorted_cluster_list[:half_num_clusters]
        upper_sorted_cluster_list = sorted_cluster_list[half_num_clusters:]
        #print("debug (upper/lower) ", len(upper_sorted_cluster_list), len(lower_sorted_cluster_list))
        # recurse over both the lower and upper halves of the list
        lower_closest_pair = fast_closest_pair(lower_sorted_cluster_list)
        upper_closest_pair = fast_closest_pair(upper_sorted_cluster_list)
        # see which half came up with the closest cluster
        if lower_closest_pair[0] < upper_closest_pair[0]:
            closest_pair = lower_closest_pair
            #print("lower is closer : ", closest_pair)
        else:
            closest_pair = upper_closest_pair
            #print("upper is closer : ", closest_pair)
        # find the center between our original list mid-point pair
        mid_point = (sorted_cluster_list[half_num_clusters -1].horiz_center() + 
                     sorted_cluster_list[half_num_clusters].horiz_center()) / 2.0
        # get the distance between this pair
        vert_slice_pair = closest_pair_strip(sorted_cluster_list, mid_point, closest_pair[0])
        # if the mid-point pair produced the lower distance, then that's the winner
        if closest_pair[0] > vert_slice_pair[0]:
            closest_pair = vert_slice_pair
    #
    return closest_pair
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    return []


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
            
    return []

#
# Test area
#
# Load all the data
#
cancer_data = load_cancer_data(DATA_3108_URL)
# create a set of test points
#
slow_short_list = []
for idx in range(10):
    slow_short_list.append(cancer_data[idx])
#
#for idx in range(10):
#    print(slow_short_list[idx])
#
slow_neighbor_pair = slow_closest_pair(slow_short_list)
#
print("slow_closest_pair : ", slow_neighbor_pair)
#print("slow_short_list-pair : ", slow_short_list[slow_neighbor_pair[1]])
#print("slow_short_list-pair : ", slow_short_list[slow_neighbor_pair[2]])
#
# prep for fast_closest_pair
#
# get the test points again
#
fast_short_list = []
for idx in range(10):
    fast_short_list.append(cancer_data[idx])
# sort the list by horizontal center
fast_short_list.sort(key = lambda cluster: cluster.horiz_center())
#
#for idx in range(10):
#    print(fast_short_list[idx])
#
fast_neighbor_pair = fast_closest_pair(fast_short_list)
#
print("fast_closest_pair : ", fast_neighbor_pair)
#
# slow_long_list...
data_3108_len = len(cancer_data)
slow_long_list = []
#
for idx in range(data_3108_len):
    slow_long_list.append(cancer_data[idx])
#
#for idx in range(10):
#    print(slow_short_list[idx])
#
slow_long_pair = slow_closest_pair(slow_long_list)
#
print("slow_long_pair : ", slow_long_pair)
#
# fast
#
data_3108_len = len(cancer_data)
fast_long_list = []
#
for idx in range(data_3108_len):
    fast_long_list.append(cancer_data[idx])
#
#for idx in range(10):
#    print(slow_short_list[idx])
#
fast_long_list.sort(key = lambda cluster: cluster.horiz_center())
fast_long_pair = fast_closest_pair(fast_long_list)
#
print("fast_long_pair : ", fast_long_pair)
