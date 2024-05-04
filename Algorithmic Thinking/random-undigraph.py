import matplotlib.pyplot as plt
import numpy as np
import math
import random


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

def random_undirected_graphs(num_nodes, probability):
    """
    Founction to generate a set of random undirected graphs

    Args:
        num_nodes (int): number of nodes to create
        probability (float): likelihood of 2 nodes being connected
    """
    # start with an enpty dictionary
    random_graphs = {}
    # populate the dictionary with the nodes and no edges yet
    for node_idx in range(num_nodes):
        random_graphs[node_idx] = set([])
    # step through each node
    for node_outer in random_graphs.keys():
       # loop through all nodes other than self
        for node_inner in random_graphs.keys():
            if node_outer == node_inner:
                continue
            else:
                if random.random() < probability:
                    random_graphs[node_outer].add(node_inner)
    # all done
    return random_graphs

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

def plot_undigraph(undigraph, num_nodes):
    """
    Function to plot a normalized digraph in loglog mode
    """
    # Let's organize the digraph into x and y data
    points_list = sorted(undigraph.items())
    #
    x, y = zip(*points_list)
    #
    # Now let's set up the plotting area
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.suptitle('Log/Log plot of in_degree distribution for the citation graph')
    ax.scatter(x, y)
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    ax.set_xlabel('Degree')
    ax.set_ylabel('Probability')
    plt.xlim(0, num_nodes)
    plt.show()
    
num_nodes = 100
undie = random_undirected_graphs(num_nodes, 0.5)
#print(undie[0])
degs = compute_in_degrees(undie)
print("Compute_in_degrees : ", degs)

#undie_degree = normal_in_degree_distribution(undie)

# print(undie)
#print(sorted(undie_degree.items()))

#plot_undigraph(undie_degree, num_nodes)
