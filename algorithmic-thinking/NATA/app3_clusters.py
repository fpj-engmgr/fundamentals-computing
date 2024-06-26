"""
    cancer-clustering
    
    This program takes cancer rate statistical data and clusters this data to
    plot incidence by area
"""
import alg_cluster
import math
import random
import time
import matplotlib.pyplot as plt

#import urllib2

###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table
"""
DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    
    Import a table of county-based cancer risk data
    from a csv format file
    
    cancer_cluster_list = []
    #
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print("Loaded", len(data_lines), "data points")
    #
    for line in data_lines:
        if len(line) > 0:
            tokens = line.split(',')
            cancer_cluster_list.append(alg_cluster.Cluster(set([tokens[0]]),
                                                           float(tokens[1]),
                                                           float(tokens[2]),
                                                           int(tokens[3]),
                                                           float(tokens[4])))
    return cancer_cluster_list

"""
DIRECTORY = "/Users/fpj/Development/python/fundamentals-computing/algorithmic-thinking/data/"
MAP_URL = DIRECTORY + "data_clustering/USA_Counties.png"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"

def load_data_table(file_name):
    """
    Load data from unifiedCancerData spreadsheet and return list of clusters
    """
    cancer_cluster_list = []
    #
    data_file = open(file_name)
    data = data_file.read()
    data_lines = data.split('\n')
    #
    for line in data_lines:
        if len(line) > 0:
            tokens = line.split(',')
            cancer_cluster_list.append(alg_cluster.Cluster(set([tokens[0]]),
                                                           float(tokens[1]),
                                                           float(tokens[2]),
                                                           int(tokens[3]),
                                                           float(tokens[4])))
    #
    print("Loaded", len(cancer_cluster_list), "data points")
    #
    return cancer_cluster_list

############################
#    Helper functions
############################
def deepcopy(obj):
    """
    Helper function to create a deep copy of a list

    Args:
        obj (list): any list of items
    Returns:
        new_list (list) : a deep copy of orig_list
    """
    if isinstance(obj, dict):
        return {deepcopy(key): deepcopy(value) for key, value in obj.items()}
    if hasattr(obj, '__iter__'):
        return type(obj)(deepcopy(item) for item in obj)
    return obj

def random_point(range, mid_point = 0.0):
    """
    Helper function to generate a random floating point number in a range around a mid_point

    Args:
        range (float): range across which numbers are to be generated
        mid_point (float): mid-point of above range (default is 0.0)
    Return:
        tuple that is a 2-dimensional point
    """
    lower = mid_point - (range / 2.0)
    #
    return ((random.random() * range) + lower,
            (random.random() * range) + lower)
#
def gen_random_clusters(num_clusters):
    """
    Function to create a list of clusters distributed across a random point within
    the square with corners (+/- 1, +/- 1)

    Args:
        num_clusters (int): number of clusters to be generated
    Return:
        cluster_list (Cluster): list of clusters
    """
    cluster_list = []
    #
    for _idx_ in range(num_clusters):
        cluster_point = random_point(2.0)
        cluster_list.append(alg_cluster.Cluster(set([]),
                                                cluster_point[0],
                                                cluster_point[1],
                                                0,
                                                0.0))
    #
    return cluster_list
########################
# Plotting functions

def plot_slow_fast_comparison(cluster_count, slow_tgt_times, fast_tgt_times):
    """
    Plot two line graphs depicting the performance of target_order and
    fast_target_order

    Args:
        node_count (list):      number of nodes for timing
        tgt_times (list):       execution time of target_order
        fast_tgt_times (list):  execution time of fast target_order
    """
    #
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.suptitle('Comparison of slow and fast closest pair performance')
    ax.plot(cluster_count, slow_tgt_times, '-b', label='slow_closest_pair function')
    ax.plot(cluster_count, fast_tgt_times, '-g', label='fast_closest_pair function')
    #
    ax.set_xlabel('Number of clusters')
    ax.set_ylabel('Execution time')
    ax.legend()
    plt.show()

#################################
#   Execution run for fast_slow
def fast_slow_run(max_clusters):
    """
    Run timing on slow and fast closest pair functions up to max_clusters

    Args:
        max_clusters (int): All the clusters we want!

    """
    x_axis = []
    slow_times = []
    fast_times = []
    print("Starting random cluster timing run")
    for idx in range(2, max_clusters):
        x_axis.append(idx)
        #
        cluster_list = gen_random_clusters(idx)
        #
        # slow_closest_pair timing
        #
        start_time = time.time()
        #
        closest_pair = slow_closest_pair(cluster_list)
        #
        slow_time = time.time() - start_time
        slow_times.append(slow_time)
        #
        # fast_closest_pair timing
        #
        start_time = time.time()
        #
        closest_pair = fast_closest_pair(cluster_list)
        #
        fast_time = time.time() - start_time
        fast_times.append(fast_time)
    #
    # plot the slow/fast cloest pair comparison
    #
    plot_slow_fast_comparison(x_axis, slow_times, fast_times)
    #
    # That't it!
    #
    
############################
#    Closest pair functions
############################   
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
    index_list = []
    #
    for idx in range(len(cluster_list)):
        #print("CPS : cluster_list[idx].horiz_center ", math.fabs(cluster_list[idx].horiz_center() - horiz_center), half_width)
        if math.fabs(cluster_list[idx].horiz_center() - horiz_center) < half_width:
            index_list.append([idx, cluster_list[idx]])
    # sort list of indices in nondecreasing order of vertical coordinates
    index_list.sort(key = lambda index_list: index_list[1].vert_center())
    #
    index_list_len = len(index_list)
    #print("CPS : |S| ", index_list_len)
    #for idx in range(index_list_len):
    #    print("CPS : idx/index_list[idx]", idx, "/", index_list[idx])
    #
    closest_pair = (float('inf'), -1, -1)
    #
    for idx_u in range(0, index_list_len - 1):
        for idx_v in range(idx_u + 1, min(idx_u + 4, index_list_len)):
            distance_u_v = index_list[idx_u][1].distance(index_list[idx_v][1])
            #print("CPS : distance_u_v ", distance_u_v, idx_u, idx_v)
            if distance_u_v < closest_pair[0]:
                closest_pair = (distance_u_v,
                                index_list[idx_u][0],
                                index_list[idx_v][0])
    #
    #print("CPS : closest_pair ", closest_pair)
    if closest_pair[1] > closest_pair[2]:
        closest_pair = (closest_pair[0], closest_pair[2], closest_pair[1])
    #
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
        #print("SLO dist/clu1/clu2: ", closest_pair[0], 
        #      sorted_cluster_list[closest_pair[1]],
        #      sorted_cluster_list[closest_pair[2]])
        #print("  debug(fast) num_clusters <= 3 :", sorted_cluster_list)
    else:
        # find the mid-point in the list
        #print("debugsy : ", num_clusters)
        half_num_clusters = num_clusters // 2
        #print("debug : half/full", half_num_clusters, "/", num_clusters)
        # split into upper and lower lists
        left_sorted_cluster_list = sorted_cluster_list[:half_num_clusters]
        right_sorted_cluster_list = sorted_cluster_list[half_num_clusters:]
        #print("debug (upper/lower) ", len(upper_sorted_cluster_list), len(lower_sorted_cluster_list))
        # recurse over both the lower and upper halves of the list
        left_closest_pair  = fast_closest_pair(left_sorted_cluster_list)
        right_closest_pair = fast_closest_pair(right_sorted_cluster_list)
        # see which half came up with the closest cluster
        if left_closest_pair[0] < right_closest_pair[0]:
            closest_pair = left_closest_pair
            #print("left is closer : ", closest_pair)
            #print("details ", sorted_cluster_list[closest_pair[1]])
            #print("details ", sorted_cluster_list[closest_pair[2]])
        else:
            closest_pair = (right_closest_pair[0],
                            right_closest_pair[1] + half_num_clusters,
                            right_closest_pair[2] + half_num_clusters)
            #print("right is closer : ", closest_pair)
            #print("details ", sorted_cluster_list[closest_pair[1]])
            #print("details ", sorted_cluster_list[closest_pair[2]])
        # find the center between our original list mid-point pair
        mid_point = (sorted_cluster_list[half_num_clusters -1].horiz_center() + 
                     sorted_cluster_list[half_num_clusters].horiz_center()) / 2.0
        # get the distance between this pair
        vert_slice_pair = closest_pair_strip(sorted_cluster_list, mid_point, closest_pair[0])
        # if the mid-point pair produced the lower distance, then that's the winner
        if closest_pair[0] > vert_slice_pair[0]:
            closest_pair = vert_slice_pair
    #
    #print("|sorted_cluster_list| : ",len(sorted_cluster_list))
    #for clust_idx in range(len(sorted_cluster_list)):
        #print("SCL :[", clust_idx, "] ", sorted_cluster_list[clust_idx])
    
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
    #
    #cluster_len = len(cluster_list)
    #
    hier_cluster_set = deepcopy(cluster_list)
    #
    while len(hier_cluster_set) > num_clusters:
        closest_pair = fast_closest_pair(hier_cluster_set)
        #
        cluster_i = hier_cluster_set[closest_pair[1]]
        cluster_j = hier_cluster_set[closest_pair[2]]
        #
        hier_cluster_set.remove(cluster_i)
        hier_cluster_set.remove(cluster_j)
        #
        hier_cluster_set.append(cluster_i.merge_clusters(cluster_j))
    #
    return hier_cluster_set

#
# Work area
#
#fast_slow_run(200)
#
# plotting of hierarchical clustering
#
cancer_clusters = load_data_table(DATA_3108_URL)
#
    