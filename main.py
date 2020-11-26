import numpy as np
import time
from matplotlib import pyplot as plt
from verify import check_match
from indexer_algo import indexer
from sequencer_algo import sequencer
from generator import *

"""
Generate a set of graphs to experiment with
"""

# setup_basic()
# exit(0)

"""
Plot performance with graphs in steps of 1000, till 10000
"""

# sizes = list(range(0, 10001, 1000))
# times = [0 for i in range(11)]

# for i in range(1000, 10001, 1000):
#     g1, g2 = generate_pair(i, 0.5)
#     start = time.time()

#     ind1 = indexer(g1)
#     l1 = ind1.get_label()
#     ind2 = indexer(g2)
#     l2 = ind2.get_label()

#     # seq1 = sequencer(g1)
#     # l1 = seq1.get_label()
#     # seq2 = sequencer(g2)
#     # l2 = seq2.get_label()

#     end = time.time()

#     check_match(g1, g2, l1, l2)
#     times[i//1000] = end - start
# plt.plot(sizes, times)
# plt.xlabel("Number of nodes")
# plt.ylabel("Time in seconds")
# plt.show()
# exit(0)

"""
Experiment with individual graphs
"""

# g1 = np.load("graph_rvtqwhqjdl_10000_0.3_v1.npy")
# g2 = np.load("graph_rvtqwhqjdl_10000_0.3_v2.npy")

g1 = np.load("graph_soeuxrtioh_10000_0.5_v1.npy")
g2 = np.load("graph_soeuxrtioh_10000_0.5_v2.npy")

start = time.time()

ind1 = indexer(g1)
l1 = ind1.get_label()
ind2 = indexer(g2)
l2 = ind2.get_label()

# seq1 = sequencer(g1)
# l1 = seq1.get_label()
# seq2 = sequencer(g2)
# l2 = seq2.get_label()

end = time.time()
print("\nTime taken: %.3f seconds" %(end - start))
# print(l1)
# print(l2)

check_match(g1, g2, l1, l2)         ## Apply labellings to check if isomorphic