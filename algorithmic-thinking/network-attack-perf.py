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
        # debug check to see which nodes have the max_degree_node in them
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        #
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order

def fast_targeted_order(ugraph):
    """
    Compute a targeted attack order consisting of maximal degree
    
    Optimized implementation

    Args:
        ugraph (dict): undirected graph representing a network

    Returns:
        attack_order (list): list of nodes to attack in order of maximum impact to least impact
    """
    new_graph = copy_graph(ugraph)
    num_nodes = len(new_graph)
    degree_sets = {}
    for degree in range(num_nodes):
        degree_sets[degree] = set([])
    #
    for node in range(num_nodes):
        degree = len(new_graph[node])
        degree_sets[degree].add(node)
    #
    attack_order = []
    #
    for degree in range(num_nodes - 1, -1, -1):
        while len(degree_sets[degree]) > 0:
            node = degree_sets[degree].pop()
            # now update all the neighbors of node to lower their degree
            for neighbor in new_graph[node]:
                deg = len(new_graph[neighbor])
                #
                degree_sets[deg].remove(neighbor)
                degree_sets[deg - 1].add(neighbor)
            attack_order.append(node)
            delete_node(new_graph, node)   
    #
    return attack_order

############################################
# Helper functions

def find_less_than_dict(prob_list, prob_value):
    """
    Helper function that returns the node number has a probability just above
    the given prob_value

    Args:
        prob_list (list): Sorted list of (probability, node_idx)
        prob_value (float): Probability that it should be just above
    """
    if len(prob_list) <= 1:
        prob_match = prob_list[0][1]
    else:
        half_way = len(prob_list) // 2
        if prob_list[half_way][0] >= prob_value:
            if prob_list[half_way - 1][0] < prob_value:
                prob_match = prob_list[half_way]
            else:
                if half_way == 1:
                    prob_match = prob_list[half_way - 1]
                else:
                    prob_match = find_less_than_dict(prob_list[:half_way], prob_value)
        else:
            if half_way == 1:
                prob_match = prob_list[half_way + 1]
            else:
                prob_match = find_less_than_dict(prob_list[half_way:], prob_value)
    return prob_match

def random_order(in_graph):
    """
    Take all the keys in the dict in_graph and shuffle them

    Args:
        in_graph (dict): dictionary of nodes with their edges

    Returns:
        random_list: randomized list of nodes in graph
    """
    random_list = list()
    #
    for node in in_graph.keys():
        random_list.append(node)
    #
    random.shuffle(random_list)
    #
    return random_list

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

    """
    Take all the keys in the dict in_graph and shuffle them

    Args:
        in_graph (dict): dictionary of nodes with their edges

    Returns:
        random_list: randomized list of nodes in graph
    """
    random_list = list()
    #
    for node in in_graph.keys():
        random_list.append(node)
    #
    random.shuffle(random_list)
    #
    return random_list
#
# Main functions
#
def plot_target_comparison(node_count, tgt_times, fast_tgt_times):
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
    fig.suptitle('Comparison of target_order and fast_target_order performance')
    ax.plot(node_count, tgt_times, '-r', label='target_order function')
    ax.plot(node_count, fast_tgt_times, '-g', label='fast_target_order function')
    #
    ax.set_xlabel('Number of nodes')
    ax.set_ylabel('Execution time')
    ax.legend()
    plt.show()

def make_complete_ugraph(num_nodes):
    """
    Function to return a complete undirected graph with num_nodes nodes
    
    Restrictions:
    - Self-loops are not allowed
    """
    # start with and empty dictionary
    ugraph = {}
    # if num_nodes is not positive, then return empty
    if num_nodes <= 0:
        return ugraph
    # create a set of all nodes
    
    # loop through all the nodes (0 -> num_nodes -1)
    for node_idx in range(num_nodes):
        # create dict entry for this node and remove self-loop
        all_nodes_list = list(range(num_nodes))
        all_nodes_list.remove(node_idx)
        ugraph[node_idx] = set(all_nodes_list)
    #
    return ugraph

def make_upa_graph(num_nodes, start_nodes):
    """
    Function to implement the UPA algorithm, creating a synthetic directed graph
    
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
    upa_graph = make_complete_ugraph(start_nodes)
    #print("make_upa_graph : complete graph edges : ", total_in_degrees(upa_graph))
    # make the additional nodes
    for node_idx in range(start_nodes, num_nodes):
        ttlindegs = total_in_degrees(upa_graph)
        #print('node: ', node_idx, 'Total edges : ', ttlindegs)
        #
        upa_length = len(upa_graph)
        #print(node_idx, dpa_length, ttlindegs, ttlindegs // dpa_length)
        #
        probability_dict = {}
        cumulative_probability = 0.0
        # calculate the probability of selection for all nodes in dpa_graph
        for node in upa_graph.keys():
            node_indeg = len(upa_graph[node])
            selection_prob = (node_indeg + 1)/((2.0 * ttlindegs) + upa_length)
            cumulative_probability += selection_prob
            #print("node #", node, " selection_prob : ", cumulative_probability)
            probability_dict[cumulative_probability] = node
        #
        probability_list = sorted(probability_dict.items())
        #print("probability_list : ", probability_list)
        #
        upa_graph[node_idx] = set([])
        for _ in range(start_nodes):
            #
            prob_value = random.random()
            prob_rslt = find_less_than_dict(probability_list, prob_value)
            # add node to set of connected nodes (note: undirected needs both)
            upa_graph[(prob_rslt[1])].add(node_idx)
            #print("Node ", node_idx, " prob_rslt[1] ", prob_rslt[1])
            upa_graph[node_idx].add(prob_rslt[1])
        # added all the edges to the set, so add it to the digraph
        
        # print("edges : ", new_edges)
    #
    return upa_graph

tgt_times = []
fast_tgt_times = []
x_axis = []
start_nodes = 5
for num_nodes in range(10, 1000, 10):
    x_axis.append(num_nodes)
    test_graph = make_upa_graph(num_nodes, start_nodes)
    #
    start_time = time.time()
    tgt_nodes = targeted_order(test_graph)
    tgt_time = time.time() - start_time
    tgt_times.append(tgt_time)
    #
    start_time = time.time()
    fast_tgt_nodes = fast_targeted_order(test_graph)
    fast_tgt_time = time.time() - start_time
    fast_tgt_times.append(fast_tgt_time)
    
#for idx in range(len(x_axis)):
#    print("num : ", x_axis[idx], "\t", tgt_times[idx], "\t", fast_tgt_times[idx])

plot_target_comparison(x_axis, tgt_times, fast_tgt_times)   