"""
    cancer-clustering
    
    This program takes cancer rate statistical data and clusters this data to
    plot incidence by area
"""
import alg_cluster
import math
import random
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
    
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print("Loaded", len(data_lines), "data points")
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]

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
        closest_pair = slow_closest_pair(hier_cluster_set)
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


######################################################################
# Code for k-means clustering
    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    cluster_list_len = len(cluster_list)
    # create a list of num_clusters centers...try the first 3 in cluster_list
    # alt: position initial centers at the location of clusters with largest populations
    center_list = []
    for idx in range(num_clusters):
        center_list.append((cluster_list[idx].horiz_center(),
                            cluster_list[idx].vert_center()))
    #
    for _idx_i in range(num_iterations):
        # create a set of num_clusters empty clusters
        cluster_sets = []
        for idx in range(num_clusters):
            cluster_sets.append(alg_cluster.Cluster(set([]), 0.0, 0.0, 0, 0.0))
        # find the cluster closest to the center of the desired cluster
        for idx_j in range(0, cluster_list_len):
            # check distance of each cluster to each of the center_list entries
            hor_ctr = cluster_list[idx_j].horiz_center()
            ver_ctr = cluster_list[idx_j].vert_center()
            closest_ctr_idx = -1
            closest_ctr_dis = float('inf')
            #
            for idx_f in range(num_clusters):
                #
                dist_ctr = math.sqrt(((center_list[idx_f][0] - hor_ctr) ** 2) +
                                     ((center_list[idx_f][1] - ver_ctr) ** 2))
                if dist_ctr < closest_ctr_dis:
                    closest_ctr_dis = dist_ctr
                    closest_ctr_idx = idx_f
            # we'll have the closest of the center's index, so merge in the cluster
            cluster_sets[closest_ctr_idx].merge_clusters(cluster_list[idx_j])
        # centers in the cluster_sets have been adjusted, so amend our center_list
        for idx in range(num_clusters):
            center_list[idx] = (cluster_sets[idx].horiz_center(),
                                cluster_sets[idx].vert_center())
    # after the iterations, we have our k clusters, so return them
    return cluster_sets

##
## Test area
##
## Load all the data
##
cancer_data = load_data_table(DATA_3108_URL)
# create a set of test points
#
slow_short_list = []
for idx in range(24):
    slow_short_list.append(cancer_data[idx])
#    slow_short_list.append(alg_cluster.Cluster(set(cancer_data[idx][0]),
#                                  cancer_data[idx][1],
#                                  cancer_data[idx][2],
#                                  cancer_data[idx][3],
#                                  cancer_data[idx][4]))
##
#for idx in range(15):
#    print(slow_short_list[idx])
#
slow_neighbor_pair = slow_closest_pair(slow_short_list)
#
print("slow_closest_pair : ", slow_neighbor_pair)
print("slow_short_list-pair : ", slow_short_list[slow_neighbor_pair[1]])
print("slow_short_list-pair : ", slow_short_list[slow_neighbor_pair[2]])
print("")
#
hier_slow_set = hierarchical_clustering(slow_short_list, 15)
#
for idx in range(len(hier_slow_set)):
    print("hier slow : idx/hier_slow_set[idx] ", idx, hier_slow_set[idx])
#
print("")
#
kmeans_slow_set = kmeans_clustering(slow_short_list, 15, 1)
for idx in range(len(kmeans_slow_set)):
    print("kmeans slow : idx/kmeans_slow_set[idx] ", idx, kmeans_slow_set[idx])
#
print("")
# plot attempt
#
##plot_clusters(cancer_data, hier_slow_set, True)
#
# prep for fast_closest_pair
#
# get the test points again
#
#fast_short_list = []
#for idx in range(15):
#    fast_short_list.append(alg_cluster.Cluster(set(cancer_data[idx][0]),
#                                  cancer_data[idx][1],
#                                  cancer_data[idx][2],
#                                  cancer_data[idx][3],
#                                  cancer_data[idx][4]))
## sort the list by horizontal center
#fast_short_list.sort(key = lambda cluster: cluster.horiz_center())
##
##for idx in range(15):
##    print(fast_short_list[idx])
##
#fast_neighbor_pair = fast_closest_pair(fast_short_list)
##
#print("fast_closest_pair : ", fast_neighbor_pair)
#print("fast_short_list-pair : ", fast_short_list[fast_neighbor_pair[1]])
#print("fast_short_list-pair : ", fast_short_list[fast_neighbor_pair[2]])
#print("")
##
### slow_long_list...
###data_3108_len = len(cancer_data)
###slow_long_list = []
###
###for idx in range(data_3108_len):
###    slow_long_list.append(cancer_data[idx])
###
###for idx in range(15):
###    print(slow_short_list[idx])
###
###slow_long_pair = slow_closest_pair(slow_long_list)
###
###print("slow_long_pair : ", slow_long_pair)
###print("slow long result ", slow_long_list[slow_long_pair[1]])
###print("slow long result ", slow_long_list[slow_long_pair[2]])
###
### fast
###
###data_3108_len = len(cancer_data)
###fast_long_list = []
###
###for idx in range(data_3108_len):
###    fast_long_list.append(cancer_data[idx])
###
###for idx in range(15):
###    print(slow_short_list[idx])
###
###fast_long_list.sort(key = lambda cluster: cluster.horiz_center())
###print("ante-fast-long : ",fast_long_list[1], fast_long_list[2])
###fast_long_pair = fast_closest_pair(fast_long_list)
###print("post-fast-long : ",fast_long_list[1], fast_long_list[2])
###
###print("fast_long_pair : ", fast_long_pair)
###print("fast long result ", fast_long_list[fast_long_pair[1]])
###print("fast long result ", fast_long_list[fast_long_pair[2]])
###
### Test it GOOD!
###
print("Testing closest_pair_strip")
tst1_clusters = [alg_cluster.Cluster(set([]), 0, 0, 1, 0),
                 alg_cluster.Cluster(set([]), 1, 0, 1, 0),
                 alg_cluster.Cluster(set([]), 2, 0, 1, 0),
                 alg_cluster.Cluster(set([]), 3, 0, 1, 0)]
tst1_closest_pair = closest_pair_strip(tst1_clusters, 1.5, 1.0)
print(tst1_closest_pair)
#
tst2_clusters = [alg_cluster.Cluster(set([]), -4.0, 0.0, 1, 0),
                 alg_cluster.Cluster(set([]), 0.0, -1.0, 1, 0),
                 alg_cluster.Cluster(set([]), 0.0, 1.0, 1, 0),
                 alg_cluster.Cluster(set([]), 4.0, 0.0, 1, 0)]
tst2_closest_pair = closest_pair_strip(tst2_clusters, 0.0, 4.123106)
print(tst2_closest_pair)
#
tst3_clusters = [alg_cluster.Cluster(set([]), 1.0, 0.0, 1, 0),
                 alg_cluster.Cluster(set([]), 4.0, 0.0, 1, 0),
                 alg_cluster.Cluster(set([]), 5.0, 0.0, 1, 0),
                 alg_cluster.Cluster(set([]), 7.0, 0.0, 1, 0)]
tst3_closest_pair = fast_closest_pair(tst3_clusters)
print(tst3_closest_pair)
