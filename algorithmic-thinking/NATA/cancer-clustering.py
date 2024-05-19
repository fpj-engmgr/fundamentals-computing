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
        cluster_list (list): A list of points (x, y) representing the center of each cluster
    Returns:
        closestpair (tuple): a tuple consisting of (dist, idx1, idx2), where idx1 and idx2 are
            the indices of the two closest clusters
    """
    # set our starting distance and indices
    closest_pair = (float('inf'), -1, -1)
    #
    num_clusters = len(cluster_list)
    #
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
    return closest_pair
    
    
def fast_closest_pair(cluster_list):
    """
    Find the closest pair of clusters among a list of clusters using the
    FastClosestPair algorithm

    Args:
        cluster_list (list): A list of points (x, y) representing the center of each cluster
    Returns:
        closestpair (tuple): a tuple consisting of (dist, idx1, idx2), where idx1 and idx2 are
            the indices of the two closest clusters
    """
    
#
# Test area
#
# Load all the data
#
cancer_data = load_cancer_data(DATA_3108_URL)
# create a set of test points
#
short_list = []
for idx in range(10):
    short_list.append(cancer_data[idx])
#
print(short_list)
#
neighbor_pair = slow_closest_pair(short_list)
#
print("neighbor_pair : ", neighbor_pair)