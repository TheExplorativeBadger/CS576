class DirectedWeightedEdge:

    def __init__(self, sourceKey, destinationKey, weight):
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
        return hash((self.sourceKey, self.destinationKey, self.weight))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.sourceKey == other.sourceKey and self.destinationKey == other.destinationKey and self.weight == other.weight

    def __lt__(self, other):
        return ((self.weight, self.sourceKey, self.destinationKey) < (other.weight, other.sourceKey, other.destinationKey))

class DirectedWeightedVertex:

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

    def removeParentEdge(self, sourceKey):
        try:
            for edge in self.parentEdges:
                if edge.getSourceKey() == sourceKey:
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

    def removeChildEdge(self, destinationKey):
        try:
            for edge in self.childEdges:
                if edge.getDestinationKey() == destinationKey:
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
    

from collections import defaultdict

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
#         print("Starting a New Connected Component")
#         print("Start Vertex Index: ", startVertexIndex)
#         print("Starting Visited Array: ", visited)
        curVertexIndex = startVertexIndex
        continueLooping = True
        connectedComponentStartVertexIndex = None
        while continueLooping:
            curVertexKey = self.vertexKeys[curVertexIndex]
            curVertexParentEdgeSet = self.graph[curVertexKey].getParentEdges()

#             print("Length of parent edge set: ", len(curVertexParentEdgeSet))
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

def createEdgeQueue(reads, min_overlap):
    unsorted_edges_list = []
    for sourceRead in reads:
        for destinationRead in reads:
            if (not sourceRead == destinationRead):
                curOverlap = shortestSuperstring.overlap_length(sourceRead, destinationRead)
                if (curOverlap >= min_overlap):
                    newEdge = DirectedWeightedEdge(sourceRead, destinationRead, (-1 * curOverlap))
                    unsorted_edges_list.append(newEdge)
    sortedEdgeList = sorted(unsorted_edges_list)
    return sortedEdgeList

def buildGraphFromEdgeQueue(reads_graph, edgeQueue):
    
    # Think about a stopping criteria for detecting if the graph is connected
    while len(edgeQueue) > 0:
        curEdge = edgeQueue.pop(0)
        sourceKey = curEdge.getSourceKey()
        destinationKey = curEdge.getDestinationKey()

        if (reads_graph.getOutDegree(sourceKey) == 0 and reads_graph.getInDegree(destinationKey) == 0):
            reads_graph.addEdge(sourceKey, destinationKey, curEdge)
    return reads_graph

def findGraphContigs(reads_graph):
    connectedReadComponentList = reads_graph.getConnectedComponents()
    responseContigsList = []
    for component in connectedReadComponentList:
        curContig = shortestSuperstring.merge_ordered_reads(component)
        responseContigsList.append(curContig)
    return responseContigsList

# Code for PROBLEM 1
# You are welcome to develop your code as a separate Python module
# and import it here if that is more convenient for you.

# Import the Application Driver and create an instance. All other dependencies are 
# managed in sub-modules
from application_driver.ApplicationDriver import ApplicationDriver
MainApplicationDriver = ApplicationDriver()

def greedy_assemble(reads, min_overlap=0):
    """Assembles a set of reads using the graph-based greedy algorithm.
    
    Args:
        reads: a list of strings
        min_overlap: the minimum length of an allowed overlap between two reads
    Returns:
        A list of strings (contigs) that collectively contain all input reads
    """
    

    # Create the initial un-edged graph
    reads_graph = DoubleAdjacencyListDirectedWeightedGraph(reads)
#     print(reads_graph)
    # This will create a list of (N * (N-1)) - X edges, where X represents the variable number
    # in which the overlap length is smaller than min_overlap, sorted in ascending lexigraphical order
    edgeQueue = createEdgeQueue(reads, min_overlap)

    # Add the edges into the graph according to greedy algorithm
    edgedGraph = buildGraphFromEdgeQueue(reads_graph, edgeQueue)

    # By this point, the entire graph is constructed and consists of N cnnected components
    # Need to find the connected components and construct a superstring with their sequences
    finalContigsList = findGraphContigs(edgedGraph)
#     print
#     print("Final Contigs List: ", finalContigsList)

    return finalContigsList


import fasta

unknownVariantFileName = 'sarscov2_reads.fasta'
unknownVariantReads = fasta.read_sequences_from_fasta_file(unknownVariantFileName)
knownVariantsFileName = 'sarscov2_variant_genomes.fasta'
knownVariantsFullReads = fasta.read_sequences_from_fasta_file(knownVariantsFileName)

unkownVariantReadsList = []
for read in unknownVariantReads:
    unkownVariantReadsList.append(read[1]) 

# NOTE: This will take a few minutes to run since it goes through all overlap values in {1, 29}
# Change the range below in 'overlapRange' to adjust the number of runs, they're all the same anyway

overlapRange = range(1,30)
strandMatches = [0] * len(knownVariantsFullReads)

for overlapMinimum in overlapRange:
    curOverlapContigList = greedy_assemble(unkownVariantReadsList, overlapMinimum)
    
    counter = 0
    for variant in knownVariantsFullReads:
        curVariantName = variant[0]
        curVariantSequence = variant[1]
        
        if (shortestSuperstring.overlap_length(curOverlapContigList[0], curVariantSequence) == len(curVariantSequence)):
            print("Overlap minimum: ", overlapMinimum)
            print("Variant Name: ", curVariantName)
            strandMatches[counter] += 1
            break
        
        counter += 1
        
maxMatches = len(overlapRange)     
print()
print("Final Results:")
print("----------------------")
print("Number of Overlap Values Run: ", maxMatches)
print()
print()
index = 0
for variant in knownVariantsFullReads:
    curVariantName = variant[0]
    curVariantSequence = variant[1]
    
    print()
    print("Variant Name: ", curVariantName)
    print("Number of Matches: ", strandMatches[index])
    
    index += 1      
print("----------------------")