from notebook_modules import shortestSuperstring
from data_structures import DirectedWeightedEdge
from data_structures import DirectedWeightedVertex
from data_structures import DoubleAdjacencyListDirectedWeightedGraph

def createEdgeQueue(reads, min_overlap):
    unsorted_edges_list = []
    for sourceRead in reads:
        for destinationRead in reads:
            if (not sourceRead == destinationRead):
                curOverlap = shortestSuperstring.overlap_length(sourceRead, destinationRead)
                if (curOverlap >= min_overlap):
                    newEdge = DirectedWeightedEdge(sourceRead, destinationRead, (-1 * curOverlap))
                    unsorted_edges_list.append(newEdge)
    return unsorted_edges_list.sort()

def buildGraphFromEdgeQueue(reads_graph, edgeQueue):
    # Think about a stopping criteria for detecting if the graph is connected
    while len(edgeQueue) > 0:
        curEdge = edgeQueue.pop() 
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