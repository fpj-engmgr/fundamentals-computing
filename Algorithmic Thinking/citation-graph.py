"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2

# Set timeout for CodeSkulptor if necessary
import codeskulptor
codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

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

citation_graph = load_graph(CITATION_URL)
print len(citation_graph)
in_degree_dist = in_degree_distribution(citation_graph)
print in_degree_dist
