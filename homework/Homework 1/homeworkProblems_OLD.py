from application_driver import ApplicationDriver

'''
PROBLEM 1: The greedy algorithm for fragment assembly (60 points)
Write a function, greedy_assemble, that takes as input a list of read strings and uses the greedy fragment 
assembly algorithm to assemble them. In this problem we will be more realistic and require that pairs of reads 
have overlap of at least a specified minimum length in order for them to be allowed to be merged. Specifically, 
we will only have an edge in the overlap graph from read  uu  to read  vv  if the length of the largest overlap 
of a suffix of  uu  with a prefix of  vv  is at least  min_overlapmin_overlap . The parameter  
min_overlapmin_overlap  may be set to any integer, including zero (which allows for edges between all pairs 
of reads).

Because  min_overlap  may be set to a value greater than zero, the result of the greedy_assemble 
algorithm may not be a single superstring. Rather, the result of the algorithm will be a list of "contigs", 
where each contig is the superstring for one of the connected components of the final graph resulting from 
the algorithm. Therefore, the return value of the function will be a list of strings.

You must use the graph-based (Hamiltonian path) version of the greedy algorithm. Because of the  
min_overlap  parameter, the stopping condition for the algorithm should be slightly modified 
to also stop when there are no more edges to be considered. We will assume that:

- we are assembling a single-stranded sequence and that 
- no read is a substring of any other read.

Tie-breaking criteria 
- For the purpose of making this algorithm deterministic, we must establish tiebreaking criteria for 
edges in the overlap graph that have the same weight. For two edges with the same weight, we will first 
choose the edge whose source vertex read is first in lexicographical order. If the source vertices are 
identical, then we choose the edge whose target vertex read is first in lexicographical order. For example, 
if e1 = ATCGGA → GGAT and e2 = ATCGGA → GGAA, we will attempt to use edge e2 first because GGAA < GGAT 
according to lexicographical order. You may find the fact the comparison operators for sequences in Python 
(e.g., tuples) use lexicographical ordering. For example,

(-3, "ATCGGA", "GGAA") < (-3, "ATCGGA", "GGAT")

'''

def greedy_assemble(reads, min_overlap=0):
    """Assembles a set of reads using the graph-based greedy algorithm.
    
    Args:
        reads: a list of strings
        min_overlap: the minimum length of an allowed overlap between two reads
    Returns:
        A list of strings (contigs) that collectively contain all input reads
    """

    # # Create the initial un-edged graph
    # reads_graph = DoubleAdjacencyListDirectedWeightedGraph(reads)
    # # This will create a list of (N * (N-1)) - X edges, where X represents the variable number
    # # in which the overlap length is smaller than min_overlap, sorted in ascending lexigraphical order
    # edgeQueue = createEdgeQueue(reads, min_overlap)

    # # Add the edges into the graph according to greedy algorithm
    # edgedGraph = buildGraphFromEdgeQueue(reads_graph, edgeQueue)

    # # By this point, the entire graph is constructed and consists of N cnnected components
    # # Need to find the connected components and construct a superstring with their sequences
    # finalContigsList = findGraphContigs(edgedGraph)

    # return finalContigsList