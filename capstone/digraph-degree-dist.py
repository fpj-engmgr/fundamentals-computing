"""
Degree Distribution for Graphs project

"""

# 3 example graphs to use for analysis and testing
#
EX_GRAPH0 = {0: set([1, 2]),
             1: set([]),
             2: set([])}
#
EX_GRAPH1 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3]),
             3: set([0]),
             4: set([1]),
             5: set([2]),
             6: set([])}
#
EX_GRAPH2 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3, 7]),
             3: set([7]),
             4: set([1]),
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1, 2]),
             9: set([0, 3, 4, 5, 6, 7])}
#
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
        all_nodes_set = set(range(num_nodes))
        all_nodes_set.remove(node_idx)
        digraph[node_idx] = all_nodes_set
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

def transitive_closure(digraph):
    """
    Function to compute the transitive closure of a digraph

    Returns a new digraph that is the transitive closure of the input digraph
    """
    # create a copy of the input digraph
    tc_digraph = dict(digraph)
    # go through each node in the digraph
    node_list = list(tc_digraph.keys())
    #
    for idx_i in range(len(node_list)):
        for idx_j in range(len(node_list)):
            # check if i->k and k->j implies i->j
            node_i = node_list[idx_i]
            node_j = node_list[idx_j]
            if node_i in digraph[node_j] and node_j in digraph[node_i]:
                tc_digraph[node_i].add(node_j)
    # return the transitive closure
    return tc_digraph
#    
#"""
#Graphs for Module 1
#"""
#
GRAPH0 = {0: set([1]),
          1: set([2]),
          2: set([3]),
          3: set([0])}

GRAPH1 = {0: set([]),
          1: set([0]),
          2: set([0]),
          3: set([0]),
          4: set([0])}

GRAPH2 = {0: set([1, 2, 3, 4]),
          1: set([]),
          2: set([]),
          3: set([]),
          4: set([])}

GRAPH3 = {0: set([1, 2, 3, 4]),
          1: set([0, 2, 3, 4]),
          2: set([0, 1, 3, 4]),
          3: set([0, 1, 2, 4]),
          4: set([0, 1, 2, 3])}

GRAPH4 = {"dog": set(["cat"]),
          "cat": set(["dog"]),
          "monkey": set(["banana"]),
          "banana": set([])}

GRAPH5 = {1: set([2, 4, 6, 8]),
          2: set([1, 3, 5, 7]),
          3: set([4, 6, 8]),
          4: set([3, 5, 7]),
          5: set([6, 8]),
          6: set([5, 7]),
          7: set([8]),
          8: set([7])}

GRAPH6 = {1: set([2, 5]),
          2: set([1, 7]),
          3: set([4, 6, 9]),
          4: set([6]),
          5: set([2, 7]),
          6: set([4, 9]),
          7: set([1, 5]),
          9: set([3, 4])}

GRAPH7 = {0: set([1, 2, 3, 4]), 
          1: set([0, 2, 3, 4]), 
          2: set([0, 1, 3, 4]), 
          3: set([0, 1, 2, 4]), 
          4: set([0, 1, 2, 3]), 
          5: set([2, 3, 4]), 
          6: set([0, 1, 4]), 
          7: set([0, 1, 2, 3]), 
          8: set([0, 1, 4, 7]), 
          9: set([2, 4]), 
          10: set([1, 2, 4]), 
          11: set([1, 3, 4, 7]), 
          12: set([0, 2, 3]), 
          13: set([0, 2, 4, 10]), 
          14: set([0, 2, 3, 4, 13])}

GRAPH8 = {0: set([1, 2]), 
          1: set([0, 2]), 
          2: set([0, 1]), 
          3: set([0]), 
          4: set([1, 2]), 
          5: set([0, 2]), 
          6: set([1, 2, 4]), 
          7: set([0, 3]), 
          8: set([0, 1]), 
          9: set([0, 7]), 
          10: set([0]), 
          11: set([0, 1, 3]), 
          12: set([0, 4, 7]), 
          13: set([0, 5]), 
          14: set([0, 1, 8]), 
          15: set([0, 1, 3]), 
          16: set([1, 14, 6]), 
          17: set([0, 8]), 
          18: set([0, 1]), 
          19: set([0, 1, 17])}

GRAPH9 = {0: set([1, 2, 3, 4, 5, 6]),
          1: set([0, 2, 3, 4, 5, 6]),
          2: set([0, 1, 3, 4, 5, 6]),
          3: set([0, 1, 2, 4, 5, 6]),
          4: set([0, 1, 2, 3, 5, 6]),
          5: set([0, 1, 2, 3, 4, 6]),
          6: set([0, 1, 2, 3, 4, 5]),
          7: set([1, 3, 4, 6]),
          8: set([0, 3, 4, 5, 6]),
          9: set([0, 5, 6, 7]),
          10: set([1, 2, 4, 9]),
          11: set([1, 2, 4, 6]),
          12: set([0, 2, 4, 6]),
          13: set([1, 2, 4, 5]),
          14: set([0, 1, 4, 6]),
          15: set([1, 4, 5, 6]),
          16: set([0, 1, 2, 4, 6]),
          17: set([0, 1, 2, 4, 5, 6]),
          18: set([2, 4, 5, 6, 13]),
          19: set([1, 2, 3, 5, 6]),
          20: set([0, 1, 2, 4, 5]),
          21: set([1, 2, 4, 5, 15]),
          22: set([0, 9, 4, 5, 13]),
          23: set([0, 1, 2, 3, 5, 20]),
          24: set([0, 1, 2, 3, 4, 5, 6]),
          25: set([0, 1, 2, 4, 5]),
          26: set([1, 2, 4, 5, 10, 22]),
          27: set([1, 2, 3, 5, 6]),
          28: set([0, 1, 3, 5]),
          29: set([2, 26, 4, 5, 6]),
          30: set([0, 2, 4, 6, 7]),
          31: set([20, 4, 21, 6]),
          32: set([1, 2, 4, 20, 28]),
          33: set([0, 4, 5, 6, 8, 22]),
          34: set([0, 2, 4, 5, 15]),
          35: set([1, 2, 5, 6, 9, 28]),
          36: set([24, 2, 3, 4, 6]),
          37: set([0, 1, 2, 4, 6, 10, 29]),
          38: set([0, 24, 11, 5, 6]),
          39: set([0, 1, 22, 6, 17]),
          40: set([0, 1, 2, 3, 5, 15]),
          41: set([11, 2, 3, 5, 6]),
          42: set([16, 1, 2, 5]),
          43: set([0, 1, 2, 4, 22]),
          44: set([32, 3, 6, 24, 27, 29]),
          45: set([1, 2, 4, 5, 16, 18, 37]),
          46: set([1, 5, 6, 7, 8, 12, 14]),
          47: set([8, 20, 2, 4]),
          48: set([0, 16, 2, 5, 14]),
          49: set([2, 21, 18, 6, 15])}
def test_suite():
    """
    Test suite for functions
    """
    print("Basic test of make_complete_graph with 5 nodes")
    graph5 = make_complete_graph(5)
    print(graph5)
    print(type(graph5))

    print("Basic test of compute_in_degrees with GRAPH0")
    degrees = compute_in_degrees(GRAPH0)
    print(degrees)
    in_degrees = in_degree_distribution(GRAPH0)
    print(in_degrees)
    
    print("Basic test of compute_in_degrees with GRAPH1")
    degrees = compute_in_degrees(GRAPH1)
    print(degrees)
    in_degrees = in_degree_distribution(GRAPH1)
    print(in_degrees)
    
    print("Basic test of compute_in_degrees with GRAPH2")
    degrees = compute_in_degrees(GRAPH2)
    print(degrees)
    in_degrees = in_degree_distribution(GRAPH2)
    print(in_degrees)
    
    print("Basic test of compute_in_degrees with GRAPH3")
    degrees = compute_in_degrees(GRAPH3)
    print(degrees)
    in_degrees = in_degree_distribution(GRAPH3)
    print(in_degrees)
    
    print("Basic test of compute_in_degrees with GRAPH4")
    degrees = compute_in_degrees(GRAPH4)
    print(degrees)
    in_degrees = in_degree_distribution(GRAPH4)
    print(in_degrees)
    
    print("Basic test of compute_in_degrees with GRAPH5")
    degrees = compute_in_degrees(GRAPH5)
    print(degrees)
    in_degrees = in_degree_distribution(GRAPH5)
    print(in_degrees)
    
    print("Basic test of compute_in_degrees with GRAPH6")
    degrees = compute_in_degrees(GRAPH6)
    print(degrees)
    in_degrees = in_degree_distribution(GRAPH6)
    print(in_degrees)
    
    print("Basic test of compute_in_degrees with GRAPH7")
    degrees = compute_in_degrees(GRAPH7)
    print(degrees)
    in_degrees = in_degree_distribution(GRAPH7)
    print(in_degrees)
    
    print("Basic test of compute_in_degrees with GRAPH8")
    degrees = compute_in_degrees(GRAPH8)
    print(degrees)
    in_degrees = in_degree_distribution(GRAPH8)
    print(in_degrees)
    
    print("Basic test of compute_in_degrees with GRAPH9")
    degrees = compute_in_degrees(GRAPH9)
    print(degrees)
    in_degrees = in_degree_distribution(GRAPH9)
    print(in_degrees)
    
# test_suite()

print("\nBasic test of compute_in_degrees with GRAPH1")
degrees = compute_in_degrees(GRAPH1)
print(degrees)
in_degrees = in_degree_distribution(GRAPH1)
print(in_degrees)
trans_clos_digraph = transitive_closure(GRAPH1)
print(trans_clos_digraph)

print("\nBasic test of compute_in_degrees with GRAPH6")
degrees = compute_in_degrees(GRAPH6)
print(degrees)
in_degrees = in_degree_distribution(GRAPH6)
print(in_degrees)
trans_clos_digraph = transitive_closure(GRAPH6)
print(trans_clos_digraph)