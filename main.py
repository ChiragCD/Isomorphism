import numpy as np
import time
from verify import check_match
from indexer_algo import indexer
from sequencer_algo import sequencer
from generator import setup_basic

# setup_basic()
# exit(0)

g1 = np.load("graph_rvtqwhqjdl_10000_0.3_v1.npy")
g2 = np.load("graph_rvtqwhqjdl_10000_0.3_v2.npy")

# g1 = np.load("graph_soeuxrtioh_10000_0.5_v1.npy")
# g2 = np.load("graph_soeuxrtioh_10000_0.5_v2.npy")

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

if(l1[0] == -1 or l2[0] == -1):
    print("Labelling failed")
    exit(0)

check_match(g1, g2, l1, l2)
# print(sorted(ind.get_label()) == list(range(10000)))