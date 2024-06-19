"""
Input: Undirected graph g = (V, E)
Output: Subset V' _ V that satisfies some property.
1 n< V|;
2 for i < 0 ton do
3
foreach subset V' C V of size i do
4
flag - True;
5
foreach e € E do
6
ifen V' = @ then
7
flag + False;
if flag = True then
9
return V';
"""
import itertools
import time
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

#
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

def mystery_algorithm(undi_graph):
    """
    Take an undirected graph and perform a mystery algorithm on it.

    Args:
        undi_graph (dict): undirected graph
    """
    # V is the set of nodes
    node_set = set(undi_graph.keys())
    #
    edge_set = set([])
    # E is the set of edges
    for node in node_set:
        for edge in undi_graph[node]:
            if edge < node:
                edge = (edge, node)
            else:
                edge = (node, edge)
            edge_set.add(edge)
    #
    num_nodes = len(node_set)
    # for i = 0 to n do
    for idx_i in range(num_nodes + 1):
        # for each subset V' C V of size i do
        for node_subs in itertools.combinations(node_set, idx_i):
            node_subset = set(node_subs)
            # print("debug: NODE_SUBSET= ", node_subset)
            # set flat to True initially
            flag = True
            # foreach e € E do
            for edge in edge_set:
                #print("debug: edge_set = ", edge_set, set(node_subset))
                # if e n V' = @ then
                if set(edge).intersection(node_subset) == set([]):
                    # print("debug: edge_set = ", edge_set, node_subset)
                    # flag <- False
                    flag = False
            # if flag = True then return node_subset
            if flag:
                return node_subset
    # all done
        

###############################
# Test the mystery_algorithm
print("\n\nTesting mystery_algorithm")

# Example graphs

GRAPH0 = {1 : set([]),
          2 : set([3,1]),
          3 : set([2]),
          4 : set([2])}

GRAPH1 = {1 : set([]), 2 : set([3, 7]), 3 : set([2, 4]), 4 : set([3, 5]), 5 : set([4, 6]), 6 : set([5, 7]), 7 : set([2, 6])}
GRAPH2 = {1 : set([2, 3, 4, 5, 6, 7]), 2 : set([1]), 3 : set([1]), 4 : set([1]), 5 : set([1]), 6 : set([1]), 7 : set([1])}
GRAPH3 = {0: set([4, 7, 10]), 1: set([5, 6]), 2: set([7, 11]), 3: set([10]), 4: set([0, 7, 11]), 5: set([1, 7]), 6: set([1]), 7: set([0, 2, 4, 5, 9, 11]), 8: set([9]), 9: set([7, 8]), 10: set([0, 3]), 11: set([2, 4, 7])}
GRAPH4 = {0: set([4, 7, 10, 12, 13]), 1: set([5, 6, 12]), 2: set([7, 11, 12, 14]), 3: set([10, 14, 15]), 4: set([0, 7, 11, 12, 13, 14]), 5: set([1, 7, 15]), 6: set([1, 13]), 7: set([0, 2, 4, 5, 9, 11, 14]), 8: set([9, 14, 15]), 9: set([7, 8]), 10: set([0, 3]), 11: set([2, 4, 7]), 12: set([0, 1, 2, 4]), 13: set([0, 4, 6, 15]), 14: set([2, 3, 4, 7, 8]), 15: set([3, 5, 8, 13])}
GRAPH5 = {0: set([4, 7, 10, 12, 13, 16]), 1: set([5, 6, 12]), 2: set([7, 11, 12, 14]), 3: set([10, 14, 15]), 4: set([0, 7, 11, 12, 13, 14, 17]), 5: set([1, 7, 15]), 6: set([1, 13]), 7: set([0, 2, 4, 5, 9, 11, 14, 18]), 8: set([9, 14, 15]), 9: set([7, 8, 19]), 10: set([0, 3]), 11: set([2, 4, 7]), 12: set([0, 1, 2, 4]), 13: set([0, 4, 6, 15, 16]), 14: set([2, 3, 4, 7, 8]), 15: set([3, 5, 8, 13]), 16: set([0, 13, 19]), 17: set([4]), 18: set([7]), 19: set([9, 16])}
GRAPH6 = {0: set([4, 7, 10, 12, 13, 16]), 1: set([5, 6, 12]), 2: set([7, 11, 12, 14]), 3: set([10, 14, 15]), 4: set([0, 7, 11, 12, 13, 14, 17]), 5: set([1, 7, 15]), 6: set([1, 13]), 7: set([0, 2, 4, 5, 9, 11, 14, 18]), 8: set([9, 14, 15]), 9: set([7, 8, 19]), 10: set([0, 3]), 11: set([2, 4, 7]), 12: set([0, 1, 2, 4]), 13: set([0, 4, 6, 15, 16]), 14: set([2, 3, 4, 7, 8]), 15: set([3, 5, 8, 13]), 16: set([0, 13, 17, 19]), 17: set([4, 16]), 18: set([7]), 19: set([9, 16])}

# Testing 
start_time = time.time()
print(len(mystery_algorithm(GRAPH0)))   # answer should be 1
end_time = time.time()
print("Time taken to run mystery_algorithm on GRAPH0 : ", end_time - start_time)
start_time = time.time()
print(len(mystery_algorithm(GRAPH1)))     # answer should be 3
end_time = time.time()
print("Time taken to run mystery_algorithm on GRAPH1 : ", end_time - start_time)
start_time = time.time()
print(len(mystery_algorithm(GRAPH2)))     # answer should be 1
end_time = time.time()
print("Time taken to run mystery_algorithm on GRAPH2 : ", end_time - start_time)
start_time = time.time()
print(len(mystery_algorithm(GRAPH3)))     # answer should be 6
end_time = time.time()
print("Time taken to run mystery_algorithm on GRAPH3 : ", end_time - start_time)
start_time = time.time()
print(len(mystery_algorithm(GRAPH4)))     # answer should be 9
end_time = time.time()
print("Time taken to run mystery_algorithm on GRAPH4 : ", end_time - start_time)
start_time = time.time()
print(len(mystery_algorithm(GRAPH5)))
end_time = time.time()
print("Time taken to run mystery_algorithm on GRAPH5 : ", end_time - start_time)
start_time = time.time()
print(len(mystery_algorithm(GRAPH6)))
end_time = time.time()
print("Time taken to run mystery_algorithm on GRAPH6 : ", end_time - start_time)
start_time = time.time()

GRAPH7 = {1: set([]),
          2: set([3, 7]),
          3: set([2, 4]),
          4: set([3, 5]),
          5: set([4, 6]),
          6: set([5, 7]),
          7: set([2, 6])}
#
v_prime = mystery_algorithm(GRAPH7)
#
print("V' = ", v_prime)
#
v_prime = mystery_algorithm(GRAPH2)
#
print("V' = ", v_prime)
#
degs = compute_in_degrees(GRAPH4)
sum_degrees = 0
for key in degs.keys():
    #print("Node : ", key, " has in-degree : ", degs[key])
    sum_degrees += degs[key]
print("Compute_in_degrees : ", degs)
print("Sum of all degrees : ", sum_degrees)
print("m * n = ", len(GRAPH4) * sum_degrees)
#
degs = compute_in_degrees(GRAPH5)
sum_degrees = 0
for key in degs.keys():
    #print("Node : ", key, " has in-degree : ", degs[key])
    sum_degrees += degs[key]
print("Compute_in_degrees : ", degs)
print("Sum of all degrees : ", sum_degrees)
print("m * n = ", len(GRAPH5) * sum_degrees)
#
degs = compute_in_degrees(GRAPH6)
sum_degrees = 0
for key in degs.keys():
    #print("Node : ", key, " has in-degree : ", degs[key])
    sum_degrees += degs[key]
print("Compute_in_degrees : ", degs)
print("Sum of all degrees : ", sum_degrees)
print("m * n = ", len(GRAPH6) * sum_degrees)