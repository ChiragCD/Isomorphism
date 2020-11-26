import time, random, string
import numpy as np

np.random.seed(int(time.time()))

net = False     ## Bool decides whether to use networkx
try:
    import networkx as nx
    net = True
except ImportError:
    print("Warning: Not using networkx")

net = False     ## Don't use networkx
                ## Networkx erdos-renyi graph generator not very efficient

"""
Generate a name to save a graph with
Use 10 random characters
"""
def generate_name():
    return "graph_" + ''.join(random.choice(string.ascii_lowercase) for i in range(10))

"""
Generate Erdos-Renyi graph as an adjacency matrix
Use parameters n and p
"""
def erdos_renyi(n, p):

    print("\nGenerating Erdos-Renyi with n = " + str(n) +" and p = " + str(p))

    if(net):
        graph = nx.to_numpy_matrix(nx.erdos_renyi_graph(n, p))
        return np.array(graph, dtype=np.bool_)
    
    graph = np.random.rand(n, n)                ## Fill random
    graph[graph < p] = 1                        ## Decide with threshold
    graph[graph < 1] = 0
    graph = np.array(graph, dtype=np.bool_)
    indices = np.tril_indices(n)
    graph[indices] = graph.T[indices]
    np.fill_diagonal(graph, False)
    return graph

"""
Generate and return a pair of isomorphic graphs with different labellings
"""
def generate_pair(n, r):
    g1 = erdos_renyi(n, r)
    print("g1 ready")
    
    matching = np.array(list(range(n)))
    np.random.shuffle(matching)
    print("Matching ready")

    g2 = np.copy(g1)
    g2 = g2[matching]
    g2 = g2[:, matching]
    print("g2 ready")

    return g1, g2

"""
Save a graph with its details and a random name
"""
def save_graph(graph, n, r):
    np.save(generate_name() + '_' + str(n) + '_' + str(r), graph)

"""
Save a pair of graphs with similar name, meant for isomorphs
"""
def save_pair(g1, g2, n, r):
    name = generate_name()
    np.save(name + '_' + str(n) + '_' + str(r) + "_v1", g1)
    np.save(name + '_' + str(n) + '_' + str(r) + "_v2", g2)

"""
Generate some random samples
"""
def setup_basic():
    g1, g2 = generate_pair(10000, 0.5)
    save_pair(g1, g2, 10000, 0.5)
    g1, g2 = generate_pair(10000, 0.3)
    save_pair(g1, g2, 10000, 0.3)
    g1, g2 = generate_pair(5, 0.5)
    save_pair(g1, g2, 5, 0.5)

"""
Load an adjacency matrix from a text file
Can be comma or space separated (or both), with elements being 0 1 or True False
"""
def load_graph(filename):
    f = open(filename, "r")
    l = f.readlines()
    f.close()
    if(',' in l[0]):
        lines = [[(j.strip("\n, \t") not in ['0', "False"]) for j in i.split(",")] for i in l]
    else:
        lines = [[(j.strip("\n, \t") not in ['0', "False"]) for j in i.split()] for i in l]
    return np.array(lines, dtype=np.bool_)

# setup_basic()