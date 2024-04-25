import matplotlib.pyplot as plt
import numpy as np
import math
import random

def make_complete_graph(num_nodes):
    """
    Function to return a complete directed graph with num_nodes nodes
    
    Restrictions:
    - Self-loops are not allowed
    """
    # start with and empty dictionary
    digraph = {}
    # if num_nodes is not positive, then return empty
    if num_nodes <= 0:
        return digraph
    # create a set of all nodes
    
    # loop through all the nodes (0 -> num_nodes -1)
    for node_idx in range(num_nodes):
        # create dict entry for this node and remove self-loop
        all_nodes_list = list(range(num_nodes))
        all_nodes_list.remove(node_idx)
        digraph[node_idx] = set(all_nodes_list)
    #
    return digraph
#
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
        totindeg += len(digraph[node_key])
    #
    return totindeg
        
def in_degree_distribution(digraph):
    """
    Function to calculate the number of nodes with a specific in-degree
    
    Returns dict with in-degree key and node count value
    """
    # first compute the in-degrees for each node in the digraph
    in_degree_dict = compute_in_degrees(digraph)
    # create an empty degree distribution dict
    deg_dist_dict = {}
    # go through each node and look at its in-degrees
    for node in in_degree_dict.keys():
        in_degrees = in_degree_dict[node]
        # if this in-degree count exists increment, else set to 1
        if in_degrees in deg_dist_dict:
            deg_dist_dict[in_degrees] += 1
        else:
            deg_dist_dict[in_degrees] = 1
    # return the distribution
    return deg_dist_dict

def make_dpa_graph(num_nodes, start_nodes):
    """
    Function to implement the DPA algorithm, creating a synthetic directed graph
    
    The process creates a graph of start_nodes nodes, which is complete (i.e. all
    edges that are possible <no self-loops> are in place). 
    
    Then num_nodes - start_nodes
    nodes are added with each new node with the following probability:
    (indeg(node) + 1)/(total in-degree + )

    Args:
        num_nodes (_type_): _description_
        start_nodes (_type_): _description_
    """
    # create the start graph that is complete
    dpa_graph = make_complete_graph(start_nodes)
    # make the additional nodes
    for node_idx in range(start_nodes, num_nodes):
        totindegs = total_in_degrees(dpa_graph)
        print('Total in-degrees : ', totindegs)
         #
        dpa_length = len(dpa_graph)
         #
        new_edges = set([])
         #
        for dummy_idx in range(start_nodes):
            # randomly select a node in dpa_graph
            node_key = random.randrange(0, dpa_length)
            node_indeg = len(dpa_graph[node_key])
            select_probability = (node_indeg + 1)/(totindegs + dpa_length)
            print('Node : ', node_key, 'Probability of selection :', select_probability)
            if select_probability > random.random():
                new_edges.add(node_key)
        # added all the edges to the set, so add it to the digraph
        dpa_graph[node_idx] = new_edges
    #
    return dpa_graph

test_graph = make_dpa_graph(27770, 13)
print(in_degree_distribution(test_graph))

