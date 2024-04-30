from collections import deque

def bfs_visited(ugraph: dict, start_node):
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

def cc_visited(ugraph: dict):
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
        remain_nodes.pop(0)
    #
    return c_components

def largest_cc_size(ugraph: dict):
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

def compute_resilience(ugraph: dict, attack_order: list):
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
        print("c_r: ", un_graph)
    #
    return network_max_cc

# 3 example graphs to use for analysis and testing
#
EX_GRAPH0 = {0: set([1, 2]),
             1: set([]),
             2: set([])}
#
EX_GRAPH1 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3]),
             3: set([]),
             4: set([1]),
             5: set([2]),
             6: set([])}
#
EX_GRAPH2 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3, 7]),
             3: set([]),
             4: set([1]),
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1, 2]),
             9: set([0, 3, 4, 5, 6, 7])}


# bf_visited tests
st_node = 0
v0 = bfs_visited(EX_GRAPH0, st_node)
print("EX_GRAPH0 [", st_node, "] : ", v0)
st_node = 0
v1 = bfs_visited(EX_GRAPH1, st_node)
print("EX_GRAPH1 [", st_node, "] : ", v1)
st_node = 4
v1 = bfs_visited(EX_GRAPH1, st_node)
print("EX_GRAPH1 [", st_node, "] : ", v1)
st_node = 0
v2 = bfs_visited(EX_GRAPH2, st_node)
print("EX_GRAPH2 [", st_node, "] : ", v2)
st_node = 2
v2 = bfs_visited(EX_GRAPH2, st_node)
print("EX_GRAPH2 [", st_node, "] : ", v2)
st_node = 6
v2 = bfs_visited(EX_GRAPH2, st_node)
print("EX_GRAPH2 [", st_node, "] : ", v2)
st_node = 9
v2 = bfs_visited(EX_GRAPH2, st_node)
print("EX_GRAPH2 [", st_node, "] : ", v2)
#
# cc_visited tests
cc0 = cc_visited(EX_GRAPH0)
cc1 = cc_visited(EX_GRAPH1)
cc2 = cc_visited(EX_GRAPH2)
#
print("EX_GRAPH0 : ", cc0)
print("EX_GRAPH1 : ", cc1)
print("EX_GRAPH2 : ", cc2)

# largest_cc_size tests
ls0 = largest_cc_size(EX_GRAPH0)
ls1 = largest_cc_size(EX_GRAPH1)
ls2 = largest_cc_size(EX_GRAPH2)
#
print("EX_GRAPH0 largest : ", ls0)
print("EX_GRAPH1 largest : ", ls1)
print("EX_GRAPH2 largest : ", ls2)

#
att1 = [1, 6, 4]
res1 = compute_resilience(EX_GRAPH1, att1)

print("EX_GRAPH1 : ", res1, att1, EX_GRAPH1)
