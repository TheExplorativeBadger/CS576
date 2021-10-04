def is_eulerian(g):
    """Checks if a directed graph is Eulerian.  Assumes that g is connected.
    
    Args:
        g: a DirectedGraph object
    Returns:
        True if g is Eulerian, False otherwise.
    """
    returnValue = True
    for node in range(g.num_vertices()):
        if not (g.indegree(node) == g.outdegree(node)):
            returnValue = False
    return returnValue

def find_cycle_in_eulerian_graph(g, start_vertex):
    """Finds an arbitrary cycle starting at a given vertex in a directed graph.
    Assumes that the graph is Eulerian, and thus that such a cycle exists."
    
    Args:
        g: a DirectedGraph object
        start_vertex: the index of the vertex from which the cycle should start
    Returns:
        A cycle represented by a list of indices of the vertices traversed, in order, by the cycle.  
        The first and last entries of the list will be identical and equal to start_vertex.
    """
    usedEdges = set()
    usedEdgesList = []
    continueLooping = True
    currentVertex = start_vertex
    while continueLooping:
        currentNodeOutgoingEdges = g.out_edges(currentVertex)
        
        chosenEdge = (-1,-1)
        for edge in currentNodeOutgoingEdges:
            if not edge in usedEdges:
                chosenEdge = edge
                break
        
        usedEdges.add(chosenEdge)
        usedEdgesList.append(chosenEdge)
        currentVertex = chosenEdge[1]
        
        if currentVertex == start_vertex:
            continueLooping = False
        
    responseList = []
    responseList.append(start_vertex)
    for edge in usedEdgesList:
        responseList.append(edge[1])
    
    return responseList
    