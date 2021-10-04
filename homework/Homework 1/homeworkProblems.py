from application_driver.ApplicationDriver import ApplicationDriver

MainApplicationDriver = ApplicationDriver()

def greedy_assemble(reads, min_overlap=0):

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

    return MainApplicationDriver.greedyHamiltonianPathAssembly(reads, min_overlap)

def strain_variant_identification_matching(unknownVariantFilePath, knownVariantsFilePath, overlapRangeMin, overlapRangeMax):
    overlapRange = range(overlapRangeMin, (overlapRangeMax + 1))
    return MainApplicationDriver.strainVariantIdentificationMatching(unknownVariantFilePath, knownVariantsFilePath, overlapRange)

def problem2Execute():
    unknownVariantFileName = 'sarscov2_reads.fasta'
    knownVariantsFileName = 'sarscov2_variant_genomes.fasta'
    overlapRangeMinimum = 1
    overlapRangeMaximum = 29

    problem2Results = strain_variant_identification_matching(unknownVariantFileName, knownVariantsFileName, overlapRangeMinimum, overlapRangeMaximum)
    print(problem2Results)