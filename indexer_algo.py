import math
import numpy as np

class indexer(object):

    def __init__(self, g, use_modifies=1):

        self.g = np.copy(g)
        self.use_modifies = use_modifies
        self.dim = g.shape[0]
        self.deg = np.sum(g, axis=1)
        self.label = np.array([-1 for i in range(self.dim)])
    
    def get_deg_nbh(self, n):

        neighbours = np.where(self.g[n])
        deg_nbh = self.deg[neighbours]
        deg_nbh = np.sort(deg_nbh)
        # print(deg_nbh)
        # deg_nbh = indexer.countsort(deg_nbh)
        return deg_nbh
    
    @staticmethod
    def countsort(unsorted):
        ## Credits - http://stackoverflow.com/a/18502321/2399799
        # unsorted = numpy.asarray(unsorted)
        return np.repeat(np.arange(1+unsorted.max()), np.bincount(unsorted))
    
    def set_key(self):

        print("\nGenerating key")

        self.top_count = int(3 * math.log2(self.dim))
        self.tops = np.argpartition(self.deg, -self.top_count)[-self.top_count:]

        sorted_key = list(self.tops)
        sorted_key.sort(key=(lambda i: self.deg[i]), reverse=True)

        extras = np.where(self.deg == self.deg[sorted_key[-1]])[0]
        for i in extras:
            if(i not in sorted_key):
                sorted_key.append(i)
                self.top_count += 1
        top_degs = self.deg[sorted_key]

        if(len(top_degs) != len(set(list(top_degs)))):

            print("Warning: Cases of Duplicate Key Degree: " + str(len(top_degs) - len(set(list(top_degs)))))
            if(self.use_modifies == 0):
                print("Error: Algorithm Failed - Duplicate key degree\n")
                return -1
            print("Warning: Hashing key with degree neighbourhood")

            sorted_key.sort(key=(lambda i: list(self.get_deg_nbh(i))))
            for i in range(1, self.top_count):
                if(self.deg[sorted_key[i]] != self.deg[sorted_key[i-1]]):
                    continue
                if(np.array_equal(self.get_deg_nbh(sorted_key[i]), self.get_deg_nbh(sorted_key[i-1]))):
                    print("Error: Algorithm Failed - Duplicate degree neighbourhood\n")
                    return -1
        
        self.key_indices = sorted_key
        print("Key generated")

        self.key = np.zeros((self.dim,), dtype=np.bool_)
        self.key[self.key_indices] = True

        for i in range(self.top_count):
            self.label[sorted_key[i]] = i
        
        print("Key labeled")
    
    @staticmethod
    def check_duplicates(g):
        l = list(g)
        s = set([i.tostring() for i in l])
        return (len(l) - len(s))
    
    def index_with_key(self):

        self.g = self.g[:, self.key_indices]

        l = list(np.where(self.key == False)[0])
        duplicates = indexer.check_duplicates(self.g[l])
        
        if(duplicates):
            print("Error: Algorithm Failed - Duplicate Indexing Cases: " + str(duplicates) + "\n")
            return -1
        
        l.sort(key=(lambda i: list(self.g[i])))
        print("Labelling remaining nodes")
        for i in range(self.top_count, self.dim):
            self.label[l[i - self.top_count]] = i
        print("Labelling complete\n")
    
    def get_label(self):

        if(self.set_key() == -1):
            return [-1]
        if(self.index_with_key() == -1):
            return [-1]
        return self.label