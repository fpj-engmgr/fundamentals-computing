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

def random_undirected_graph(num_nodes, probability):
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
    random_graph = {}
    # populate the dictionary with the nodes and no edges yet
    for node_idx in range(num_nodes):
        random_graph[node_idx] = set([])
    # step through each node
    for node_outer in range(num_nodes):
       # loop through all nodes other than self
        for node_inner in range(node_outer + 1, num_nodes):
            if random.random() < probability:
                # ensure symmetry for adjacency
                random_graph[node_outer].add(node_inner)
                random_graph[node_inner].add(node_outer)
    # all done
    return random_graph
 
def normal_in_degree_distribution(digraph):
    """
    Function to return a normalized in-degree distribution for a given
    (un)directed graph
    
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
    fig.suptitle('Log/Log plot of in_degree distribution for the DPA graph')
    ax.scatter(x, y)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('in_degree')
    ax.set_ylabel('Fraction of Nodes')
    plt.show()

def plot_ugraph_compare_three(network_resilience, er_resilience, upa_resilience):
    """
    Plot three line graphs depicting the resilience under a random order attack on
    - computer network (pre-defined)
    - ER algorithm generated network graph
    - DPA algorithm generated network graph

    Args:
        network_resilience (list): remaining largest connected component
        er_resilience (list): remaining largest connected component
        upa_resilience (list): remaining largest connected component
    """
    x_axis = list(range(len(network_resilience)))
    print
    #
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.suptitle('Comparison of graph resilience for random order attack')
    ax.plot(x_axis, network_resilience, '-b', label='Computer Network')
    ax.plot(x_axis, er_resilience, '-g', label='ER synthetic; p = 0.004')
    ax.plot(x_axis, upa_resilience, '-r', label='UPA synthetic; m = 3')
    ax.set_xlabel('Number of nodes removed')
    ax.set_ylabel('Size of larges connected component')
    ax.legend()
    plt.show()

def plot_ugraph_compare_targeted(network_resilience, er_resilience, upa_resilience):
    """
    Plot three line graphs depicting the resilience under a random order attack on
    - computer network (pre-defined)
    - ER algorithm generated network graph
    - DPA algorithm generated network graph

    Args:
        network_resilience (list): remaining largest connected component
        er_resilience (list): remaining largest connected component
        upa_resilience (list): remaining largest connected component
    """
    x_axis = list(range(len(network_resilience)))
    print
    #
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.suptitle('Comparison of graph resilience for targeted order attack')
    ax.plot(x_axis, network_resilience, '-b', label='Computer Network')
    ax.plot(x_axis, er_resilience, '-g', label='ER synthetic; p = 0.004')
    ax.plot(x_axis, upa_resilience, '-r', label='UPA synthetic; m = 3')
    ax.set_xlabel('Number of nodes removed')
    ax.set_ylabel('Size of larges connected component')
    ax.legend()
    plt.show()

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
    un_graph = copy_graph(ugraph)
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

#
# main code
# 
net_graf = load_graph(NETWORK_URL)
print("Max CC : ", largest_cc_size(net_graf))
print("Edges in ngraf : ", total_in_degrees(net_graf))
#for node in net_graf:
#    print(node, net_graf[node])
#
num_nodes = 1239
er_probability = 0.004
num_starter = 3
#
er_graf = random_undirected_graph(num_nodes, er_probability)
print("Max CC : ", largest_cc_size(er_graf))
print("Edges in ER graph : ", total_in_degrees(er_graf))
#
upa_graf = make_upa_graph(num_nodes, num_starter)
print("Max CC : ", largest_cc_size(upa_graf))
print("Edges in UPA graph : ", total_in_degrees(upa_graf))

net_attack = random_order(net_graf)
net_resilience = compute_resilience(net_graf, net_attack)
er_attack = random_order(er_graf)
er_resilience = compute_resilience(er_graf, er_attack)
upa_attack = random_order(upa_graf)
upa_resilience = compute_resilience(upa_graf, upa_attack)
#
#print(net_resilience)
#print(er_resilience)
#print(upa_resilience)

#plot_ugraph_compare_three(net_resilience, er_resilience, upa_resilience)

net_targets = targeted_order(net_graf)
#print("net_targets :", net_targets)
er_targets = targeted_order(er_graf)
#print("er_targets :", er_targets)
upa_targets = targeted_order(upa_graf)
print("upa_targets :", upa_targets)
upa_fast_targets = fast_targeted_order(upa_graf)
print("upa_fast_targets : ", upa_fast_targets)

#net_tgt_resilience = compute_resilience(net_graf, net_targets)
#er_tgt_resilience = compute_resilience(er_graf, er_targets)
#upa_tgt_resilience = compute_resilience(upa_graf, upa_targets)

#plot_ugraph_compare_targeted(net_tgt_resilience, er_tgt_resilience, upa_tgt_resilience)

