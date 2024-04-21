"""
Degree Distribution for Graphs project

"""

# 3 example graphs to use for analysis and testing
#
EX_GRAPH0 = {0: set([1, 2])}
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

def test_suite():
    """
    Test suite for functions
    """
    print "Basic test of make_complete_graph with 5 nodes"
    graph5 = make_complete_graph(5)
    print graph5
    print type(graph5)

test_suite()