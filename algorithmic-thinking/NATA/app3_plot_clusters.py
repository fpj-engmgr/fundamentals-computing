"""
Some provided code for plotting the clusters using matplotlib
"""

import math
import alg_cluster
from urllib.request import urlopen
import matplotlib.pyplot as plt


# URLS for various important datasets
#DIR_IMAGE = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
#MAP_URL = DIR_IMAGE + "data_clustering/USA_Counties.png"

DIR_FILES = "/Users/fpj/Development/python/fundamentals-computing/algorithmic-thinking/data/"
MAP_URL = DIR_FILES + "data_clustering/USA_Counties.png"
DATA_3108_URL = DIR_FILES + "data_clustering/unifiedCancerData_3108.csv"

# Define colors for clusters.  Display a max of 16 clusters.
COLORS = ['Aqua', 'Yellow', 'Blue', 'Fuchsia', 'Black', 'Green', 'Lime', 'Maroon', 'Navy', 'Olive', 'Orange', 'Purple', 'Red', 'Brown', 'Teal']

###############################
#   Helper functions
def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = open(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print("Loaded", len(data_lines), "data points")
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]
    
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

def circle_area(pop):
    """
    Compute area of circle proportional to population
    """
    return math.pi * pop / (200.0 ** 2)


def plot_clusters(data_table, cluster_list, draw_centers = False):
    """
    Create a plot of clusters of counties
    """

    fips_to_line = {}
    for line_idx in range(len(data_table)):
        fips_to_line[data_table[line_idx][0]] = line_idx
     
    # Load map image
    #map_file = urlopen(MAP_URL)
    map_img = plt.imread(MAP_URL)

    # Scale plot to get size similar to CodeSkulptor version
    ypixels, xpixels, bands = map_img.shape
    DPI = 60.0                  # adjust this constant to resize your plot
    xinch = xpixels / DPI
    yinch = ypixels / DPI
    plt.figure(figsize=(xinch,yinch))
    implot = plt.imshow(map_img)
   
    # draw the counties colored by cluster on the map
    if not draw_centers:
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            for fips_code in cluster.fips_codes():
                line = data_table[fips_to_line[fips_code]]
                plt.scatter(x = [line[1]], y = [line[2]], s =  circle_area(line[3]), lw = 1,
                            facecolors = cluster_color, edgecolors = cluster_color)

    # add cluster centers and lines from center to counties            
    else:
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            for fips_code in cluster.fips_codes():
                line = data_table[fips_to_line[fips_code]]
                plt.scatter(x = [line[1]], y = [line[2]], s =  circle_area(line[3]), lw = 1,
                            facecolors = cluster_color, edgecolors = cluster_color, zorder = 1)
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            cluster_center = (cluster.horiz_center(), cluster.vert_center())
            for fips_code in cluster.fips_codes():
                line = data_table[fips_to_line[fips_code]]
                plt.plot( [cluster_center[0], line[1]],[cluster_center[1], line[2]], cluster_color, lw=1, zorder = 2)
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            cluster_center = (cluster.horiz_center(), cluster.vert_center())
            cluster_pop = cluster.total_population()
            plt.scatter(x = [cluster_center[0]], y = [cluster_center[1]], s =  circle_area(cluster_pop), lw = 2,
                        facecolors = "none", edgecolors = "black", zorder = 3)


    plt.show()

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

#############################
#   Work area
#
#   Load the data
#
cancer_data_table = load_data_table(DATA_3108_URL)
cancer_cluster_list = []
#
for idx in range(len(cancer_data_table)):
    cancer_cluster_list.append(alg_cluster.Cluster(set([cancer_data_table[idx][0]]),
                                                   cancer_data_table[idx][1],
                                                   cancer_data_table[idx][2],
                                                   cancer_data_table[idx][3],
                                                   cancer_data_table[idx][4]))
#
hier_cluster_list = hierarchical_clustering(cancer_cluster_list, 15)
#
plot_clusters(cancer_data_table, hier_cluster_list)
