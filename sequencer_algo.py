import numpy as np

"""
For convenience, designed as an object oriented class
"""
class sequencer(object):
    
    def __init__(self, g, use_modifies=1):

        self.g = np.copy(g)                 ## Do not modify original
        self.use_modifies = use_modifies    ## Set whether to use modified key in case of failure
        self.dim = g.shape[0]               ## Dimension
        self.deg = np.sum(g, axis=1)        ## Degrees of each node
        self.label = np.array([-1 for i in range(self.dim)])    ## Fresh label
    
    """
    Returns degree of each neighbour as an array
    Used to identify each node
    """
    def get_deg_nbh(self, n):

        neighbours = np.where(self.g[n])        ## Get neighbours
        deg_nbh = self.deg[neighbours]          ## Get their degrees
        deg_nbh = sequencer.countsort(deg_nbh)  ## Sort
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
    Check if duplicates exist in a matrix
    """
    @staticmethod
    def check_duplicates(g):
        l = list(g)
        s = set([i.tostring() for i in l])
        return (len(l) - len(s))
    
    """
    Main function
    Generate labels and return them
    """
    def get_label(self):

        print("\nGenerating degree neighbourhoods")
        neighbourhoods = np.array([self.get_deg_nbh(i) for i in range(self.dim)])       ## Get all degree neighborhoods

        print("Checking for duplicates")
        differences = sequencer.check_duplicates(neighbourhoods)                        ## Verify uniqueness

        if(differences):
            print("Error: Algorithm Failed - Duplicate Degree Neighbourhood Cases - " + str(differences))   ## Give up
            return [-1]
        
        print("Ordering")
        l = list(range(self.dim))
        sequencer.arraysort(l, neighbourhoods)                  ## Sort by neighborhood
        # l.sort(key=(lambda i:list(neighbourhoods[i])))

        print("Labelling")
        for i in range(self.dim):
            self.label[l[i]] = i        ## Label
        
        print("Labelling complete")
        return self.label