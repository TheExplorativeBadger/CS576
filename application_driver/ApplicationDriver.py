from application_driver.data_structure_driver.DataStructureDriver import DataStructureDriver
from application_driver.task_driver.TaskDriver import TaskDriver
from application_driver.file_utils.FileUtils import FileUtils

class ApplicationDriver:

    _DataStructureDriver = DataStructureDriver()
    _TaskDriver = TaskDriver()
    _FileUtils = FileUtils()

    def __init__(self):
        self._state = 'ACTIVE'

    def getTestString(self):
        return 'Hello from Application Driver'

    def getTestStringFromDD(self):
        return self._DataStructureDriver.getTestString()
    
    def getTestStringFromTD(self):
        return self._TaskDriver.getTestString()

    def greedyHamiltonianPathAssembly(self, reads, min_overlap):

        """
            Assembles a set of reads using the graph-based greedy algorithm.
        
            Args:
                reads: a list of strings
                min_overlap: the minimum length of an allowed overlap between two reads
            Returns:
                A list of strings (contigs) that collectively contain all input reads
        """

        '''
            HW 1, PROBLEM 1: The greedy algorithm for fragment assembly (60 points)
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

        taskType = 'GREEDY_HAMILTONIAN_PATH'
        data = {
            'reads': reads,
            'min_overlap': min_overlap
        }
        dataStructure = self._DataStructureDriver.buildApplicationDataStructure(taskType, data)
        return self._TaskDriver.execute(taskType, dataStructure)

    def strainVariantIdentificationMatching(self, unkownVariantFilePath, knownVariantsFilePath, overlap_range):
        '''
            HW 1, PROBLEM 2: Strain Variant Identification (10 points)
             Included with this notebook is the file `sarscov2_reads.fasta` which is a set of reads from a 
             SARS-CoV-2 variant genome.  Use your `greedy_assemble` function to assemble this genome and then 
             *determine the identity of the variant*.  The file `sarscov2_variant_genomes.fasta` contains 
             the genome sequences for five SARS-CoV-2 variants of concern or variants of interest: alpha, beta, 
             delta, gamma, and epsilon.  If your code is correct, these reads should assemble to a sequence that 
             is identical to one of these genomes (*note: typically, a newly sequenced viral genome will not 
             match exactly to a reference genome, but we are keeping it simple in this assignment*)

            A few notes:
            1. The reads are free of sequencing errors
            2. The reads are all in the same orientation as the SARS-CoV-2 genome
            3. Any minimum overlap value between 0 and 30 should succeed in assembling the genome.
            4. If your `greedy_assemble` function is not correct, you may use an alternative strategy for 
               determining the identity of the variant (e.g., by examining the reads and the candidate variant 
               genome sequences provided)
            5. This problem will be manually graded.  The majority of the credit will be providing the code that you 
               used to determine the identity of the variant.
        '''

        unknownVariantFileContents = self._FileUtils.readFastaFile(unkownVariantFilePath)
        unknownVariantReads = self._FileUtils.getReadsFromFastaFileContentsAsList(unknownVariantFileContents)

        knownVariantsFileContents = self._FileUtils.readFastaFile(knownVariantsFilePath)
        knownVariantReads = self._FileUtils.getReadsFromFastaFileContentsAsList(knownVariantsFileContents)
        knownVariantLabels = self._FileUtils.getLabelsFromFastaFileContentsAsList(knownVariantsFileContents)

        UnknownContigsLists = []

        for overlapValue in overlap_range:
            contigsList = self.greedyHamiltonianPathAssembly(unknownVariantReads, overlapValue)
            UnknownContigsLists.append(contigsList)

        taskType = 'VARIANT_IDENTIFICATION'
        metadata = {
            'known_variant_reads': knownVariantReads,
            'known_variant_labels': knownVariantLabels
        }
        return self._TaskDriver.execute(taskType, UnknownContigsLists, metadata)