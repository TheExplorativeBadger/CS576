from collections import defaultdict
from application_driver.data_structure_driver.data_structures.base_data_structures.DirectedGraphVertex import DirectedGraphVertex

class DirectedGraph:

    ''' 
        A Directed Graph base class implemented using DirectedWeightedVertex objects as nodes 
    '''

    def __init__(self, numberVertices = 0, vertexLabels = []):
        self.vertexKeys = []
        if (len(vertexLabels) > 0):
            for vertexLabel in vertexLabels:
                self.vertexKeys.append(vertexLabel)
            if (numberVertices > len(vertexLabels)):
                differenceList = range(len(vertexLabels) + 1, numberVertices + 1)
                for difference in differenceList:
                    self.vertexKeys.append(difference)   
        else:
            if (numberVertices > 0):
                for vertexIndex in range(1, numberVertices + 1):
                    self.vertexKeys.append(vertexIndex)

        self.numberVertices = len(self.vertexKeys)
        graph = defaultdict(self.default_vertex_value)
        for vertexKey in self.vertexKeys:
            newVertex = DirectedGraphVertex(vertexKey)
            graph[vertexKey] = newVertex
        self.graph = graph

    def default_vertex_value(self, value):
        defaultVertex = DirectedGraphVertex(value)
        return defaultVertex

    def getNumberVertices(self):
        return self.numberVertices

    def getVertexKeys(self):
        return self.vertexKeys

    def addEdge(self, sourceKey, destinationKey, edge):
        self.graph[sourceKey].addChildEdge(edge)
        self.graph[destinationKey].addParentEdge(edge)

    def hasEdge(self, sourceKey, destinationKey):
        sourceVertex = self.graph[sourceKey]
        destinationVertex = self.graph[destinationKey]
        return sourceVertex.hasChildEdge(destinationKey) and destinationVertex.hasParentEdge(sourceKey)

    def removeEdge(self, sourceKey, destinationKey, weight = None):
        self.graph[sourceKey].removeChildEdge(destinationKey, weight)
        self.graph[destinationKey].removeParentEdge(sourceKey, weight)

    def getInDegree(self, key):
        return len(self.graph[key].getParentEdges())

    def getOutDegree(self, key):
        return len(self.graph[key].getChildEdges())

    def getDegree(self, key):
        return self.getInDegree(key) + self.getOutDegree(key)

    def getEdgesFromSource(self, sourceKey):
        return self.graph[sourceKey].getChildEdges()

    def getEdgesToDestination(self, destinationKey):
        return self.graph[destinationKey].getParentEdges()

    def getTotalNumberOfEdges(self):
        totalSum = 0
        for key in self.vertexKeys:
            totalSum += self.getInDegree(key)
        return totalSum

    def getAllEdges(self):
        edgeList = []
        for key in self.vertexKeys:
            curVertexChildEdges = self.getEdgesFromSource(key)
            for childEdge in curVertexChildEdges:
                edgeList.append(childEdge)
        return edgeList

    def getConnectedComponents(self):
        responseComponentList = []
        visited = [False] * self.numberVertices
        for vertexIndex in range(self.numberVertices):
            if not visited[vertexIndex]:
                print("Building connected component starting at index: ", vertexIndex)
                responseComponentList.append(self._buildConnectedComponent(vertexIndex, visited))
        return responseComponentList

    def _buildConnectedComponent(self, startVertexIndex, visited):
        curVertexIndex = startVertexIndex
        continueLooping = True
        connectedComponentStartVertexIndex = None
        while continueLooping:
            curVertexKey = self.vertexKeys[curVertexIndex]
            curVertexParentEdgeSet = self.getEdgesToDestination(curVertexKey)

            if (len(curVertexParentEdgeSet) < 1):
                connectedComponentStartVertexIndex = curVertexIndex
                continueLooping = False
            else:
                curVertexParentKey = curVertexParentEdgeSet.pop().getSourceKey()
                parentVertexIndex = self.vertexKeys.index(curVertexParentKey)
                curVertexIndex = parentVertexIndex
        
        if (connectedComponentStartVertexIndex > -1):

            print("Found CC Start Vertex: ", connectedComponentStartVertexIndex)
            curConnectedComponentList = []
            continueLooping = True
            curVertexIndex = connectedComponentStartVertexIndex
            while continueLooping:
                curVertexKey = self.vertexKeys[curVertexIndex]
                if (not visited[curVertexIndex]):
                    curConnectedComponentList.append(curVertexKey)
                    visited[curVertexIndex] = True
                print("Current Node Value: ", curVertexKey)
                curVertexChildEdgeSet = self.getEdgesFromSource(curVertexKey) 
                print("Current Node Child Edge Set: ", curVertexChildEdgeSet)
                if (len(curVertexChildEdgeSet) < 1):
                    continueLooping = False
                else:
                    curVertexChildKey = curVertexChildEdgeSet.pop().getDestinationKey()
                    childVertexIndex = self.vertexKeys.index(curVertexChildKey)
                    curVertexIndex = childVertexIndex
            return curConnectedComponentList
        else:
            return "Something went wrong"

    def isCyclic(self):
        visited = [False] * self.numberVertices
        recursionStack = [False] * self.numberVertices
        for vertexIndex in range(self.numberVertices):
            if visited[vertexIndex] == False:
                if self._isCyclicRecursor(vertexIndex, visited, recursionStack) == True:
                    return True
        return False

    def _isCyclicRecursor(self, vertexIndex, visited, recursionStack):
        # Mark current vertex as visited and adds to recursion stack
        visited[vertexIndex] = True
        recursionStack[vertexIndex] = True
 
        curVertexKey = self.vertexKeys[vertexIndex]
        curVertexChildEdges = self.getEdgesFromSource(curVertexKey)
        destinationKeyList = []
        for edge in curVertexChildEdges:
            curDestinationKey = edge.getDestinationKey()
            curDestinationKeyIndex = self.vertexKeys.index(curDestinationKey)
            destinationKeyList.append(curDestinationKeyIndex)

        # Recur for all neighbours
        # if any neighbour is visited and in recursionStack then graph is cyclic
        for neighbour in destinationKeyList:
            if visited[neighbour] == False:
                if self._isCyclicRecursor(neighbour, visited, recursionStack) == True:
                    return True
            elif recursionStack[neighbour] == True:
                return True
 
        # The node needs to be poped from recursion stack before function ends
        recursionStack[vertexIndex] = False
        return False
    
    def __hash__(self):
        pass

    def __eq__(self):
        pass

    def __lt__(self):
        pass

    def __str__(str):
        pass
