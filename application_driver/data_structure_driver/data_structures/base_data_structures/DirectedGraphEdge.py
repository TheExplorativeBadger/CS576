class DirectedGraphEdge:

    '''
        A Directed Edge base class, which takes an optional weight argument on construction
    '''

    def __init__(self, sourceKey, destinationKey, weight = 0):
        self.sourceKey = sourceKey
        self.destinationKey = destinationKey
        self.weight = weight

    def getSourceKey(self):
        return self.sourceKey

    def getDestinationKey(self):
        return self.destinationKey

    def updateEdgeWeight(self, newWeight):
        self.weight = newWeight

    def getEdgeWeight(self):
        return self.weight

    def __hash__(self):
        ''' Hashes on the source value, destination value, and weight '''
        return hash((self.sourceKey, self.destinationKey, self.weight))

    def __eq__(self, other):
        ''' Does not support comparison to a different object type. Compares equality across weight, source value, destination value '''
        if not isinstance(other, type(self)): return NotImplemented
        return self.sourceKey == other.sourceKey and self.destinationKey == other.destinationKey and self.weight == other.weight

    def __lt__(self, other):
        ''' Sorts by ascending weight, with ties broken by lexigraphical order of source value, followed by destination value '''
        return ((self.weight, self.sourceKey, self.destinationKey) < (other.weight, other.sourceKey, other.destinationKey))