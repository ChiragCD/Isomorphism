import numpy as np

def check_match(g1, g2, l1, l2):

    print("\nChecking if labeled graphs are isomorphic")
    
    g1dash = np.copy(g1)
    g1dash[l1] = g1
    g1dd = np.copy(g1dash)
    g1dd[:, l1] = g1dash

    g2dash = np.copy(g2)
    g2dash[l2] = g2
    g2dd = np.copy(g2dash)
    g2dd[:, l2] = g2dash

    # print(sum(g1[0]), sum(g2[6799]))
    # print(sum(g1dd[0]), sum(g2dd[0]))
    # print(sum(g1dd[1]), sum(g2dd[1]))
    # print(sum(g1dd[2]), sum(g2dd[2]))
    # print(list(np.sum(g1dd, axis=1))[:100])
    # print(list(np.sum(g2dd, axis=1))[:100])
    # print(list(np.sum(g1dash, axis=1)) == list(np.sum(g2dash, axis=1)))
    # print(g1dd[0], g2dd[0])

    print("Labels applied")
    if(np.array_equal(g1dd, g2dd)):
        print("Verified isomorphic")
    else:
        print("Not isomorphic")