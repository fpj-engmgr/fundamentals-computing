"""
Provided code for Application portion of Module 2
"""

# general imports
# import urllib2
import random
import time
import math
from collections import deque

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
import matplotlib.pyplot as plt

############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    
def random_undirected_graphs(num_nodes, probability):
    """
    Founction to generate a set of random undirected graphs (note:
    undirected graphs always have symmetric adjacency matrix, i.e. if
    there is an edge between (i,j) then there's an edge between (j,i))

    Args:
        num_nodes (int): number of nodes to create
        probability (float): likelihood of 2 nodes being connected
    Returns:
        random_graphs (ugraph): undirected graph 
    """
    # start with an enpty dictionary
    random_graphs = {}
    # populate the dictionary with the nodes and no edges yet
    for node_idx in range(num_nodes):
        random_graphs[node_idx] = set([])
    # step through each node
    for node_outer in range(num_nodes):
       # loop through all nodes other than self
        for node_inner in range(node_outer + 1, num_nodes):
            if random.random() < probability:
                # ensure symmetry for adjacency
                random_graphs[node_outer].add(node_inner)
                random_graphs[node_inner].add(node_outer)
    # all done
    return random_graphs

##########################################################
# Code for loading computer network graph

# NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
NETWORK_URL = "/Users/fpj/Development/python/fundamentals-computing/Algorithmic Thinking/data/alg_rf7.txt"

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

def bfs_visited(ugraph, start_node):
    """
    Function to compute the set of connected nodes in an undirected graph that 
    are visited when starting a breadth-first search at start_node.

    Args:
        ugraph (dict): Undirected graph
        start_node (int): Starting node for the search
    Returns:
        visited (set): Set of nodes that were visited during the search
    """
    queue = deque()
    #
    visited = {start_node}
    #
    queue.append(start_node)
    #
    while len(queue) > 0:
        current_node = queue.popleft()
        for neighbor in ugraph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return visited

def cc_visited(ugraph):
    """
    Function to get a list of all connected nodes within an undirected graph.

    Args:
        ugraph (dict): Undirected graph
    Returns:
        c_components (list): List of all sets that are connected to a node
    """
    remain_nodes = list(ugraph.keys())
    #
    c_components = list()
    #
    while len(remain_nodes) > 0:
        node = remain_nodes[0]
        visited = bfs_visited(ugraph, node)
        c_components.append(visited)
        for visit in visited:
            if visit in remain_nodes:
                remain_nodes.remove(visit)
    #
    return c_components

def largest_cc_size(ugraph):
    """
    Function to return the largest number of connected nodes in an undirected graph

    Args:
        ugraph (graph): Undirected graph
    Returns:
        max_cc_size (int): Count of nodes in largest set of connected components
    """
    max_cc_size = 0
    #
    conn_components = cc_visited(ugraph)
    #
    for cc_nodes in conn_components:
        if len(cc_nodes) > max_cc_size:
            max_cc_size = len(cc_nodes)
    #
    return max_cc_size

def compute_in_degrees(ugraph):
    """
    Function to calculate the in-degrees for each node in a graph
    
    Returns a dict of nodes and their in-degrees
    """
    # start with an empty in-degree dictionary
    in_degree_dict = {}
    # go through the nodes in digraph and set in-degree to 0
    for node in ugraph.keys():
        in_degree_dict[node] = len(ugraph[node])
    # now got through the edges in digraph and count them
    #for edges in digraph.values():
    #    for node in edges:
    #        in_degree_dict[node] += 1
    #
    # 
    return in_degree_dict
    
def in_degree_distribution(ugraph):
    """
    Function to calculate the number of nodes with a specific in-degree
    
    Returns dict with in-degree key and node count value
    """
    # first compute the in-degrees for each node in the digraph
    in_degree_dict = compute_in_degrees(ugraph)
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

def total_in_degrees(ugraph):
    """
    Helper function to calculate the total number of in-degrees

    Args:
        digraph (dict): directed graph to be traversed
    """
    #
    totindeg = 0
    #
    for node_key in ugraph.keys():
        totindeg += len(ugraph[node_key])
    # as edges are symmetric, divide by 2!
    return totindeg // 2

def compute_resilience(ugraph, attack_order):
    """
    Function to comupute the resilience of a network to removal of nodes in attack_order

    Args:
        ugraph (dict): Undirected graph
        attack_order (list): List of nodes that are attacked in each iteration
    Returns:
        network_max_cc (list): List of sizes of the largest number of connected
            after each attack 
    """
    # make a copy of ugraph (so we don't mess with it)
    un_graph = ugraph.copy()
    # First entry is the current state of connectivity
    network_max_cc = []
    #
    network_max_cc.append(largest_cc_size(un_graph))
    #
    for attack_node in attack_order:
        # remove the node
        un_graph.pop(attack_node)
        # step through the remaining ugraph nodes to remove edges to attack_node
        for node in un_graph.keys():
            edges = un_graph[node]
            if attack_node in edges:
                edges.remove(attack_node)
        #
        network_max_cc.append(largest_cc_size(un_graph))
        # print("c_r: ", un_graph)
    #
    return network_max_cc
 
ngraf = load_graph(NETWORK_URL)
print("Max CC : ", largest_cc_size(ngraf))
#print("Edges in ngraf : ", compute_in_degrees(ngraf))
print("Edges in ngraf : ", total_in_degrees(ngraf))
#
# Testing area
ugraf = random_undirected_graphs(1239, 0.004)
#print("Undirected graph : ", ugraf)

visits = bfs_visited(ugraf, 5)
#print("bfs_visited for node ", 5, " : ", visits)
ccomps = cc_visited(ugraf)
print("Edges in ugraf : ", total_in_degrees(ugraf))

#print("Connected components : ", ccomps)
print("Max CC : ", largest_cc_size(ugraf))






