import numpy as np

"""
Check if g1 and g2 are isomorphic having applied labellings l1 and l2
"""
def check_match(g1, g2, l1, l2):

    print("\nChecking if labeled graphs are isomorphic")

    if(l1[0] == -1 or l2[0] == -1):
        print("Error: Labelling not generated")     ## Full error would have been mentioned previously
        return

    g1dash = np.copy(g1)
    g1dash[l1] = g1             ## Rearrange rows
    g1dd = np.copy(g1dash)
    g1dd[:, l1] = g1dash        ## Rearrange columns

    g2dash = np.copy(g2)
    g2dash[l2] = g2             ## Rearrange rows
    g2dd = np.copy(g2dash)
    g2dd[:, l2] = g2dash        ## Rearrange columns

    print("Labels applied")
    if(np.array_equal(g1dd, g2dd)):     ## Check if identical
        print("Verified isomorphic\n")
    else:
        print("Not isomorphic\n")