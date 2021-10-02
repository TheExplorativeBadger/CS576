from application_driver.helper_modules import shortestSuperstring
from application_driver.data_structure_driver.data_structures.base_data_structures.DirectedGraph import DirectedGraph
from application_driver.data_structure_driver.data_structures.base_data_structures.DirectedGraphEdge import DirectedGraphEdge

class GreedyHamiltonianPathDirectedGraph(DirectedGraph):

    def __init__(self, reads, min_overlap):
        super().__init__(len(reads), reads)
        self._build(reads, min_overlap)

    def _build(self, reads, min_overlap):
        edgeQueue = self._createEdgeQueue(reads, min_overlap)
        self._buildSelfFromEdgeQueue(edgeQueue)

    def _createEdgeQueue(self, reads, min_overlap):
        unsorted_edges_list = []
        for sourceRead in reads:
            for destinationRead in reads:
                if (not sourceRead == destinationRead):
                    curOverlap = shortestSuperstring.overlap_length(sourceRead, destinationRead)
                    if (curOverlap >= min_overlap):
                        newEdge = DirectedGraphEdge(sourceRead, destinationRead, (-1 * curOverlap))
                        unsorted_edges_list.append(newEdge)
        sortedEdgeList = sorted(unsorted_edges_list)
        return sortedEdgeList

    def _buildSelfFromEdgeQueue(self, edgeQueue):
        # Think about a stopping criteria for detecting if the graph is connected
        while len(edgeQueue) > 0:
            curEdge = edgeQueue.pop(0)
            sourceKey = curEdge.getSourceKey()
            destinationKey = curEdge.getDestinationKey()
            self.addEdge(sourceKey, destinationKey, curEdge)
                
    def addEdge(self, sourceKey, destinationKey, edge):
        if (self.getOutDegree(sourceKey) == 0 and self.getInDegree(destinationKey) == 0):
            self.graph[sourceKey].addChildEdge(edge)
            self.graph[destinationKey].addParentEdge(edge)
            if self.isCyclic():
                # print('Removing Edge From ', sourceKey, ' To ', destinationKey)
                self.removeEdge(sourceKey, destinationKey)