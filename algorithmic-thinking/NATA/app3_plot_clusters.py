"""
Some provided code for plotting the clusters using matplotlib
"""

import math
import alg_cluster
import alg_project3_solution as soln
from urllib.request import urlopen
import matplotlib.pyplot as plt
import time

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
start_time = time.time()
hier_cluster_list = soln.hierarchical_clustering(cancer_cluster_list, 15)
hier_time = time.time() - start_time
#
#plot_clusters(cancer_data_table, hier_cluster_list)
#
start_time = time.time()
kmeans_cluster_list = soln.kmeans_clustering(cancer_cluster_list, 15, 5)
kmeans_time = time.time() - start_time
#
#plot_clusters(cancer_data_table, kmeans_cluster_list)
#
print("hierarchical clustering time ", hier_time)
print("kmeans clustering time       ", kmeans_time)