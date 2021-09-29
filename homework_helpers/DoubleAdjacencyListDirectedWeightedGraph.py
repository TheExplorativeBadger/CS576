from collections import defaultdict
from data_structures import DirectedWeightedEdge
from data_structures import DirectedWeightedVertex

def default_value():
    return {}

class DoubleAdjacencyListDirectedWeightedGraph:

    def __init__(self, vertexLabels):
        self.vertexKeys = vertexLabels
        self.numberVertices = len(vertexLabels)
        graph = defaultdict(default_value)
        for vertex in vertexLabels:
            newVertex = DirectedWeightedVertex(vertex)
            graph[vertex] = newVertex
        self.graph = graph

    def getNumberVertices(self):
        return self.numberVertices

    def getVertexKeys(self):
        return self.vertexKeys

    def hasEdge(self, sourceKey, destinationKey):
        sourceVertex = self.graph[sourceKey]
        destinationVertex = self.graph[destinationKey]
        return sourceVertex.hasChildEdge(destinationKey) and destinationVertex.hasParentEdge(sourceKey)

    def addEdge(self, sourceKey, destinationKey, edge):
        self.graph[sourceKey].addChildEdge(edge)
        self.graph[destinationKey].addParentEdge(edge)
        if self.isCyclic():
            self.removeEdge(sourceKey, destinationKey)

    def removeEdge(self, sourceKey, destinationKey):
        self.graph[sourceKey].removeChildEdge(destinationKey)
        self.graph[destinationKey].removeParentEdge(sourceKey)
    
    def getEdgesFromSource(self, sourceKey):
        return self.graph[sourceKey].getChildEdges()
    
    def getEdgesToDestination(self, destinationKey):
        return self.graph[destinationKey].getParentEdges()
    
    def getInDegree(self, key):
        return len(self.graph[key].getParentEdges())
    
    def getOutDegree(self, key):
        return len(self.graph[key].getChildEdges())

    def getDegree(self, key):
        return self.getInDegree(key) + self.getOutDegree(key)

    def getNumberGraphEdges(self):
        totalSum = 0
        for key in self.vertexKeys:
            totalSum += self.getInDegree(key)
        return totalSum

    def __str__(self):
        responseString = str(self.graph)
        return responseString

    def getConnectedComponents(self):
        responseComponentList = []
        visited = [False] * self.numberVertices
        for vertexIndex in range(self.numberVertices):
            if not visited[vertexIndex]:
                responseComponentList.append(self.buildConnectedComponent(vertexIndex, visited))
        return responseComponentList

    def buildConnectedComponent(self, startVertexIndex, visited):
        print("Starting a New Connected Component")
        print("Start Vertex Index: ", startVertexIndex)
        print("Starting Visited Array: ", visited)
        curVertexIndex = startVertexIndex
        continueLooping = True
        connectedComponentStartVertexIndex = None
        while continueLooping:
            curVertexKey = self.vertexKeys[curVertexIndex]
            curVertexParentEdgeSet = self.graph[curVertexKey].getParentEdges()

            print("Length of parent edge set: ", len(curVertexParentEdgeSet))
            if (len(curVertexParentEdgeSet) < 1):
                connectedComponentStartVertexIndex = curVertexIndex
                continueLooping = False
            else:
                curVertexParentKey = curVertexParentEdgeSet.pop().getSourceKey()
                parentVertexIndex = self.vertexKeys.index(curVertexParentKey)
                curVertexIndex = parentVertexIndex
        
        if (connectedComponentStartVertexIndex > -1):

            curConnectedComponentList = []
            continueLooping = True
            curVertexIndex = connectedComponentStartVertexIndex
            while continueLooping:
                curVertexKey = self.vertexKeys[curVertexIndex]
                curConnectedComponentList.append(curVertexKey)
                visited[curVertexIndex] = True

                curVertexChildEdgeSet = self.graph[curVertexKey].getChildEdges() 

                if (len(curVertexChildEdgeSet) < 1):
                    continueLooping = False
                else:
                    curVertexChildKey = curVertexChildEdgeSet.pop().getDestinationKey()
                    childVertexIndex = self.vertexKeys.index(curVertexChildKey)
                    curVertexIndex = childVertexIndex
            return curConnectedComponentList
        else:
            return "Something went wrong"


    # Returns true if graph is cyclic else false
    def isCyclic(self):
        visited = [False] * self.numberVertices
        recStack = [False] * self.numberVertices
        for node in range(self.numberVertices):
            if visited[node] == False:
                if self.isCyclicUtil(node,visited,recStack) == True:
                    return True
        return False

    def isCyclicUtil(self, v, visited, recStack):
 
        # Mark current node as visited and
        # adds to recursion stack
        visited[v] = True
        recStack[v] = True
 
        nodeLabel = self.vertexKeys[v]
        curNodeChildEdges = self.graph[nodeLabel].getChildEdges()
        destinationKeyList = []
        for edge in curNodeChildEdges:
            curDestinationKey = edge.getDestinationKey()
            curDestinationKeyIndex = self.vertexKeys.index(curDestinationKey)
            destinationKeyList.append(curDestinationKeyIndex)

        # Recur for all neighbours
        # if any neighbour is visited and in
        # recStack then graph is cyclic
        for neighbour in destinationKeyList:
            if visited[neighbour] == False:
                if self.isCyclicUtil(neighbour, visited, recStack) == True:
                    return True
            elif recStack[neighbour] == True:
                return True
 
        # The node needs to be poped from
        # recursion stack before function ends
        recStack[v] = False
        return False