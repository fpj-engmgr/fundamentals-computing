import matplotlib.pyplot as plt
import numpy as np
import math
import random

"""
Provided code for application portion of module 2

Helper class for implementing efficient version
of UPA algorithm
"""

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
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

def compute_in_degrees(digraph):
    """
    Function to calculate the in-degrees for each node in a digraph
    
    Returns a dict of nodes and their in-degrees
    """
    # start with an empty in-degree dictionary
    in_degree_dict = {}
    # go through the nodes in digraph and set in-degree to 0
    for node in digraph.keys():
        in_degree_dict[node] = len(digraph[node])
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
    fig.suptitle('Log/Log plot of in_degree distribution for the DPA graph')
    ax.scatter(x, y)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('in_degree')
    ax.set_ylabel('Fraction of Nodes')
    plt.show()

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
        ttlindegs = total_in_degrees(dpa_graph)
        #print('Total edges : ', totindegs)
        #
        dpa_length = len(dpa_graph)
        #print(node_idx, dpa_length, ttlindegs, ttlindegs // dpa_length)
        #
        new_edges = set([])
        #
        probability_dict = {}
        cumulative_probability = 0.0
        # calculate the probability of selection for all nodes in dpa_graph
        for node in dpa_graph.keys():
            node_indeg = len(dpa_graph[node])
            selection_prob = (node_indeg + 1)/(ttlindegs + dpa_length)
            cumulative_probability += selection_prob
            probability_dict[cumulative_probability] = node
        #
        probability_list = sorted(probability_dict.items())
        #
        for dummy_idx in range(start_nodes):
            #
            prob_value = random.random()
            prob_rslt = find_less_than_dict(probability_list, prob_value)
            dpa_graph[(prob_rslt[1])].add(node_idx)
        # added all the edges to the set, so add it to the digraph
        dpa_graph[node_idx] = set([])
        # print("edges : ", new_edges)
    #
    return dpa_graph

num_starter = 10
num_nodes = 20
test_graph = make_dpa_graph(num_nodes, num_starter)

print('Total edges : ', total_in_degrees(test_graph))
in_deg_dict = in_degree_distribution(test_graph)
print(sorted(in_deg_dict.items()))
plot_graph = normal_in_degree_distribution(test_graph)
plot_digraph_loglog(plot_graph)
#
for node_idx in range(num_starter):
    print(" Node : ", node_idx, " edges : ",len(test_graph[node_idx]))
    


