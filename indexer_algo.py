import math
import numpy as np

"""
For convenience, designed as an object oriented class
"""
class indexer(object):

    def __init__(self, g, use_modifies=1):

        self.g = np.copy(g)                 ## Do not modify original
        self.use_modifies = use_modifies    ## Set whether to use modified key in case of failure
        self.dim = g.shape[0]               ## Dimension
        self.deg = np.sum(g, axis=1)        ## Degrees of each node
        self.label = np.array([-1 for i in range(self.dim)])    ## Fresh label
    
    """
    Returns degree of each neighbour as an array
    Used only to hash key alternatively in case of duplicate degree in the original
    """
    def get_deg_nbh(self, n):

        neighbours = np.where(self.g[n])        ## Get neighbours
        deg_nbh = self.deg[neighbours]          ## Get their degrees
        deg_nbh = indexer.countsort(deg_nbh)  ## Sort
        return deg_nbh
    
    """
    Counting sort
    """
    @staticmethod
    def countsort(unsorted):
        ## Credits - http://stackoverflow.com/a/18502321/2399799
        # unsorted = numpy.asarray(unsorted)
        if(len(unsorted) == 0):
            return np.array([])
        return np.repeat(np.arange(1+unsorted.max()), np.bincount(unsorted))
    
    """
    Set up a key to index other nodes with
    """
    def set_key(self):

        print("\nGenerating key")

        self.top_count = int(3 * math.log2(self.dim))
        self.tops = np.argpartition(self.deg, -self.top_count)[-self.top_count:]        ## Get most connected nodes

        sorted_key = list(self.tops)
        sorted_key.sort(key=(lambda i: self.deg[i]), reverse=True)

        extras = np.where(self.deg == self.deg[sorted_key[-1]])[0]      ## If there are more nodes with degree equal
        for i in extras:                                                ## to last key node, add them as well
            if(i not in sorted_key):
                sorted_key.append(i)
                self.top_count += 1
        top_degs = self.deg[sorted_key]

        duplicates = len(top_degs) - len(set(list(top_degs)))
        if(duplicates):                                                 ## Duplicate degree among key nodes
            print("Warning: Cases of Duplicate Key Degree: " + str(duplicates))
            if(self.use_modifies == 0):
                print("Error: Algorithm Failed - Duplicate key degree\n")
                return -1
            
            print("Warning: Hashing key with degree neighbourhood")     ## Use alternative key hashing

            neighbourhoods = [self.get_deg_nbh(i) for i in sorted_key]  ## Sort by hashed neighborhood
            temps = list(range(self.top_count))
            indexer.arraysort(temps, neighbourhoods)
            sorted_key = np.array(sorted_key)[temps]

            # sorted_key.sort(key=(lambda i: list(self.get_deg_nbh(i))))
            for i in range(1, self.top_count):                          ## Ensure no further duplicates. If any, give up
                if(self.deg[sorted_key[i]] != self.deg[sorted_key[i-1]]):
                    continue
                if(np.array_equal(self.get_deg_nbh(sorted_key[i]), self.get_deg_nbh(sorted_key[i-1]))):
                    print("Error: Algorithm Failed - Duplicate degree neighbourhood\n")
                    return -1
        
        self.key_indices = sorted_key
        print("Key generated")

        self.key = np.zeros((self.dim,), dtype=np.bool_)
        self.key[self.key_indices] = True       ## Note down key

        for i in range(self.top_count):
            self.label[sorted_key[i]] = i       ## Label key nodes
        
        print("Key labeled")
    
    """
    Check if duplicates exist in a matrix
    """
    @staticmethod
    def check_duplicates(g):
        l = list(g)
        s = set([i.tostring() for i in l])
        return (len(l) - len(s))
    
    """
    Sort an array of indices by the value of its row in the keymatrix
    """
    @staticmethod
    def arraysort(indices, keymatrix):
        hashes = [hash(i.tostring()) for i in keymatrix]
        unique = (len(set(hashes)) == len(hashes))
        if(unique):
            indices.sort(key=(lambda i: hashes[i]))         ## If possible, use hashes of lists rather than lists themselves
        else:
            print("Warning: Hashes not unique, performing regular sort")
            indices.sort(key=(lambda i: keymatrix[i]))      ## When lists are comoared instead of hashes, complexity rises
    
    """
    Label non-key nodes using the key
    """
    def index_with_key(self):

        self.g = self.g[:, self.key_indices]        ## Keep only columns that mention connections to the key

        l = list(np.where(self.key == False)[0])            ## Indices of non-key nodes
        duplicates = indexer.check_duplicates(self.g[l])    ## Check for duplicate key connection among non-key nodes
        
        if(duplicates):
            print("Error: Algorithm Failed - Duplicate Indexing Cases: " + str(duplicates) + "\n")      ## Give up
            return -1
        
        indexer.arraysort(l, self.g)        ## Sort by key connections
        
        print("Labelling remaining nodes")
        for i in range(self.top_count, self.dim):
            self.label[l[i - self.top_count]] = i   ## label
        print("Labelling complete\n")
    
    """
    Wrapper function
    Labels graph and returns the labeling
    """
    def get_label(self):

        if(self.set_key() == -1):           ## If gave up, give up
            return [-1]
        if(self.index_with_key() == -1):    ## If gave up, give up
            return [-1]
        return self.label