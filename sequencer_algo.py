import numpy as np

class sequencer(object):
    
    def __init__(self, g, use_modifies=1):

        self.g = np.copy(g)
        self.use_modifies = use_modifies
        self.dim = g.shape[0]
        self.deg = np.sum(g, axis=1)
        self.label = np.array([-1 for i in range(self.dim)])
    
    def get_deg_nbh(self, n):

        neighbours = np.where(self.g[n])
        deg_nbh = self.deg[neighbours]
        deg_nbh = sequencer.countsort(deg_nbh)
        # print(np.pad(deg_nbh, (0, self.dim), "constant"))
        return deg_nbh
    
    @staticmethod
    def countsort(unsorted):
        ## Credits - http://stackoverflow.com/a/18502321/2399799
        # unsorted = numpy.asarray(unsorted)
        return np.repeat(np.arange(1+unsorted.max()), np.bincount(unsorted))
    
    @staticmethod
    def arraysort(indices, keymatrix):
        hashes = [hash(i.tostring()) for i in keymatrix]
        unique = (len(set(hashes)) == len(hashes))
        if(unique):
            indices.sort(key=(lambda i: hashes[i]))
        else:
            print("Warning: Hashes not unique, performing regular sort")
            indices.sort(key=(lambda i: keymatrix[i]))

    @staticmethod
    def check_duplicates(g):
        l = list(g)
        s = set([i.tostring() for i in l])
        return (len(l) - len(s))
    
    def get_label(self):

        print("\nGenerating degree neighbourhoods")
        neighbourhoods = np.array([self.get_deg_nbh(i) for i in range(self.dim)])

        print("Checking for duplicates")
        differences = sequencer.check_duplicates(neighbourhoods)

        if(differences):
            print("Error: Algorithm Failed - Duplicate Degree Neighbourhood Cases - " + str(differences))
            return [-1]
        
        print("Ordering")
        l = list(range(self.dim))
        sequencer.arraysort(l, neighbourhoods)
        # l.sort(key=(lambda i:list(neighbourhoods[i])))

        print("Labelling")
        for i in range(self.dim):
            self.label[l[i]] = i
        
        print("Labelling complete")        
        return self.label