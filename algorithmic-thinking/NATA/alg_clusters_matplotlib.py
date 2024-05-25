"""
Some provided code for plotting the clusters using matplotlib
"""

import math
import urllib.request as url
import matplotlib.pyplot as plt


# URLS for various important datasets
URL = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
MAP_URL = URL + "data_clustering/USA_Counties.png"
DIRECTORY = "/Users/fpj/Development/python/fundamentals-computing/algorithmic-thinking/data/"
#MAP_URL = DIRECTORY + "data_clustering/USA_Counties.png"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"

# Define colors for clusters.  Display a max of 16 clusters.
COLORS = ['Aqua', 'Yellow', 'Blue', 'Fuchsia', 'Black', 'Green', 'Lime', 'Maroon', 'Navy', 'Olive', 'Orange', 'Purple', 'Red', 'Brown', 'Teal']

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
    data = data_file.read()
    data_lines = data.split('\n')
    print("Loaded", len(data_lines), "data points")
    #
    for line in data_lines:
        if len(line) > 0:
            tokens = line.split(',')
            cancer_cluster_list.append(Cluster(set([tokens[0]]), float(tokens[1]), float(tokens[2]),
                                               int(tokens[3]), float(tokens[4])))
    #
    return cancer_cluster_list
 

# Helper functions

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
    #for line_idx in range(len(data_table)):
    #    fips_to_line[data_table[line_idx][0]] = line_idx
    
    for line_idx in range(len(data_table)):
        fips_code = iter(data_table[line_idx].fips_codes())
        #print("debug plot ", line_idx, fips_code, type(fips_code))
        
        fips_to_line[fips_code] = line_idx
    # Load map image
    map_file = url.urlopen(MAP_URL)
    map_img = plt.imread(map_file)

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

#
# Load all the data
#
cancer_data = load_cancer_data(DATA_3108_URL)
# create a set of test points
#
slow_short_list = []
for idx in range(15):
    slow_short_list.append(cancer_data[idx])
#
plot_clusters(cancer_data, slow_short_list)