import DirectedGraph

class AdjacencyListDirectedGraph(DirectedGraph):
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        self._edges = {}
        for i in range(num_vertices):
            newNode = {
                "in_edges": set(),
                "out_edges": set()
            }
            self._edges[i] = newNode
    
    def add_edge(self, i, j):
        self._edges[i]['out_edges'].add(j)
        self._edges[j]['in_edges'].add(i)
    
    def has_edge(self, i, j):
        return j in self._edges[i]['out_edges']
        
    def out_edges(self, i):
        return [(i, outEdge) for outEdge in self._edges[i]['out_edges']]
        
    def in_edges(self, j):
        return [(inEdge, j) for inEdge in self._edges[j]['in_edges']]
    
    def indegree(self, i):
        return len(self._edges[i]['in_edges'])
        
    def outdegree(self, i):
        return len(self._edges[i]['out_edges'])
    
    def edges(self):
        for i in range(self._num_vertices):
            for outNode in self._edges[i]['out_edges']:
                yield (i, outNode)