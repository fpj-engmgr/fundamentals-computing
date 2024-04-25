"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""
import matplotlib.pyplot as plt
import numpy as np

"""
# Omit this section for right now

# general imports
import urllib2

# Set timeout for CodeSkulptor if necessary
import codeskulptor
codeskulptor.set_timeout(20)

# end of codeskulptor items
"""
###################################
# Code for loading citation graph

# CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"
CITATION_URL = "/Users/fpj/Development/python/fundamentals-computing/Algorithmic Thinking/data/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
#    graph_file = urllib2.urlopen(graph_url)
    graph_file = open(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print("Loaded graph with", len(graph_lines), "nodes")
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

def compute_in_degrees(digraph):
    """
    Function to calculate the in-degrees for each node in a digraph
    
    Returns a dict of nodes and their in-degrees
    """
    # start with an empty in-degree dictionary
    in_degree_dict = {}
    # go through the nodes in digraph and set in-degree to 0
    for node in digraph.keys():
        in_degree_dict[node] = 0
    # now got through the edges in digraph and count them
    for edges in digraph.values():
        for node in edges:
            in_degree_dict[node] += 1
    #
    return in_degree_dict
    
def in_degree_distribution(digraph):
    """
    Function to calculate the number of nodes with a specific in-degree
    
    Returns dict with in-degree key and node count value
    """
    # first compute the in-degrees for each node in the digraph
    in_degree_dict = compute_in_degrees(digraph)
    # create an empty degree distribution dict
    in_degree_dist_dict = {}
    # go through each node and look at its in-degrees
    for node in in_degree_dict.keys():
        in_degrees = in_degree_dict[node]
        # if this in-degree count exists increment, else set to 1
        if in_degrees in in_degree_dist_dict:
            in_degree_dist_dict[in_degrees] += 1
        else:
            in_degree_dist_dict[in_degrees] = 1
    # return the distribution
    return in_degree_dist_dict

def total_in_degrees(digraph):
    """
    Helper function to calculate the total number of in-degrees

    Args:
        digraph (dict): directed graph to be traversed
    """
    #
    totindeg = 0
    #
    for node_key in digraph.keys():
        totindeg += node_key * digraph[node_key]
    #
    return totindeg
   
def normal_in_degree_distribution(digraph):
    """
    Function to return a normalized in-degree distribution for a given
    directed graph
    
    Returns a dict with normalized in-degree values
    """
    # get the number of nodes in the digraph
    num_nodes = float(len(digraph))
    # get the in-degree distribution (not normalized)
    in_degree_distro = in_degree_distribution(digraph)
    #
    normal_in_degree_dist_dict = {}
    # step through the in-degree distribution and normalize
    for node_key in in_degree_distro.keys():
        # get the value, normalize and store
        normal_in_degree_dist_dict[node_key] = float(in_degree_distro[node_key]) / num_nodes
    #
    return normal_in_degree_dist_dict

def plot_digraph_loglog(digraph):
    """
    Function to plot a normalized digraph in loglog mode
    """
    # Let's organize the digraph into x and y data
    points_list = sorted(digraph.items())
    # remove 0 in_degrees from the points_list to avoid log(0)
    del points_list[0]
    #
    x, y = zip(*points_list)
    #
    # Now let's set up the plotting area
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.suptitle('Log/Log plot of in_degree distribution for the citation graph')
    ax.scatter(x, y)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Number of Citations')
    ax.set_ylabel('Fraction of Papers')
    plt.show()
    
    
    
citation_graph = load_graph(CITATION_URL)
#print(len(citation_graph))
in_degree_dist = in_degree_distribution(citation_graph)
print(in_degree_dist)

totlindegs = total_in_degrees(in_degree_dist)
print('Length of citation graph', len(citation_graph))
print('Total in-degrees : ', totlindegs)
print('Average in-degrees : ', totlindegs / len(citation_graph))

#print(in_degree_dist)
normal_in_degree = normal_in_degree_distribution(citation_graph)
sorted_digraph = sorted(normal_in_degree.items())
#del sorted_digraph[0]
#print(sorted_digraph)
print(len(normal_in_degree), len(in_degree_dist))

#plot_digraph_loglog(normal_in_degree)


