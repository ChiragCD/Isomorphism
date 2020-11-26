import time, random, string
import numpy as np

np.random.seed(int(time.time()))

def generate_name():
    return "graph_" + ''.join(random.choice(string.ascii_lowercase) for i in range(10))

def erdos_renyi(n, r):
    graph = np.random.rand(n, n)
    graph[graph < r] = 1
    graph[graph < 1] = 0
    graph = np.array(graph, dtype=np.bool_)
    indices = np.tril_indices(n)
    graph[indices] = graph.T[indices]
    np.fill_diagonal(graph, False)
    return graph

def generate_pair(n, r):
    g1 = erdos_renyi(n, r)
    print("g1 ready")
    
    matching = np.array(list(range(n)))
    np.random.shuffle(matching)
    print("matching ready", matching)

    g2 = np.copy(g1)
    g2 = g2[matching]
    g2 = g2[:, matching]
    print("g2 ready")

    return g1, g2

def save_graph(graph, n, r):
    np.save(generate_name() + '_' + str(n) + '_' + str(r), graph)

def save_pair(g1, g2, n, r):
    name = generate_name()
    np.save(name + '_' + str(n) + '_' + str(r) + "_v1", g1)
    np.save(name + '_' + str(n) + '_' + str(r) + "_v2", g2)

def setup_basic():
    g1, g2 = generate_pair(10000, 0.5)
    save_pair(g1, g2, 10000, 0.5)
    g1, g2 = generate_pair(10000, 0.3)
    save_pair(g1, g2, 10000, 0.3)
    g1, g2 = generate_pair(5, 0.5)
    save_pair(g1, g2, 5, 0.5)

# setup_basic()