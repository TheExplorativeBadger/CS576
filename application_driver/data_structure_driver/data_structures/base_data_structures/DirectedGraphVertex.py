class DirectedGraphVertex:

    ''' 
        A Directed Weighted Vertex base class implemented using a double adjacency set 
        to store  DirectedWeightedEdge objects as edges 
    '''

    def __init__(self, key):
        self.key = key
        self.numberParentEdges = 0
        self.parentEdges = set()
        self.numberChildEdges = 0
        self.childEdges = set()

    def getKey(self):
        return self.key

    def addParentEdge(self, edge):
        self.parentEdges.add(edge)
        self.numberParentEdges = len(self.parentEdges)

    def removeParentEdge(self, sourceKey, weight = None):
        try:
            for edge in self.parentEdges:
                if edge.getSourceKey() == sourceKey:
                    if weight == None:
                        self.parentEdges.remove(edge)
                        self.numberParentEdges -= 1
                        break
                    else:
                        if edge.getEdgeWeight() == weight:
                            self.parentEdges.remove(edge)
                            self.numberParentEdges -= 1
                            break 
            return
        except KeyError:
            return
        
    def hasParentEdge(self, sourceKey):
        hasEdge = False
        for parentEdge in self.parentEdges:
            if (parentEdge.getSourceKey() == sourceKey):
                hasEdge = True
        return hasEdge

    def getParentEdges(self):
        return self.parentEdges

    def addChildEdge(self, edge):
        self.childEdges.add(edge)
        self.numberChildEdges = len(self.childEdges)

    def removeChildEdge(self, destinationKey, weight = None):
        try:
            for edge in self.childEdges:
                if edge.getSourceKey() == destinationKey:
                    if weight == None:
                        self.parentEdges.remove(edge)
                        self.numberChildEdges -= 1
                        break
                    else:
                        if edge.getEdgeWeight() == weight:
                            self.childEdges.remove(edge)
                            self.numberChildEdges -= 1
                            break 
            return
        except KeyError:
            return
    
    def hasChildEdge(self, destinationKey):
        hasEdge = False
        for childEdge in self.childEdges:
            if (childEdge.getDestinationKey() == destinationKey):
                hasEdge = True
        return hasEdge

    def getChildEdges(self):
        return self.childEdges

    def __hash__(self):
        return hash((self.key, self.numberParentEdges, self.numberChildEdges))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.key == other.key and self.numberParentEdges == other.numberParentEdges and self.numberChildEdges == other.numberChildEdges