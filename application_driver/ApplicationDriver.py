from application_driver.data_structure_driver.DataStructureDriver import DataStructureDriver
from application_driver.task_driver.TaskDriver import TaskDriver
from application_driver.file_utils.FileUtils import FileUtils
import collections

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

    def readToGenomeAlignmentWithSkipsDynamicProgramming(self, readSequence, genomeSequence, substitutionMatrix, spaceScore, skipIntervals, skipScore):
        
        '''
            HW 2, PROBLEM 1: Dynamic Programming Algorithm for Read-to-Genome Alignment with Skips.
            
            INTRODUCTION:
            Finding an optimal read-to-genome alignment with skips and a linear gap penalty function can be solved using a few 
            modifications to the standard Needleman–Wunsch global alignment algorithm. We are given the following as inputs:

                x : a read sequence
                y : a genome sequence
                S : a substitution matrix
                s : space score
                R : a set of intervals, each represented as a pair  (start_position,end_position)(start_position,end_position),
                     that can be "skipped" in the genome (positions use 1-based indexing).
                r : skip score

            RECURRENCE:
            The dynamic programming recurrence for this task is:

            M(i,j)=max{ M(i−1,j−1)+S(xi,yj), M(i−1,j)+s, M(i,j−1)+s, max(k,ℓ)∈R:ℓ=jM(i,k−1)+r
            
            where the  maxmax  in the fourth case (the "skip" case) is taken over all skip intervals in  RR  that have end position 
            equal to  jj . This fourth case is not considered for positions in the genome that are not the end of any skip interval in  RR .

            INITIALIZATION:
            The initialization procedure is the same as for Needleman–Wunsch except that the first row is set to all zeros 
            (this effectively allows for a gap before the read sequence,  xx , to have zero cost).

            ∀j≥0,M(0,j)=0∀j≥0,M(0,j)=0 
            ∀i>0,M(i,0)=s×i∀i>0,M(i,0)=s×i

            TRACEBACK:
            The traceback procedure for semi-global alignment is slightly different from that of global alignment. Traceback starts at 
            the cell with the maximum value in the last row (instead of the lower right corner) and stops when a cell is reached in the 
            first row (the convention used here is that  xx  indexes the rows and  yy  indexes the columns). Such a traceback path 
            corresponds to an alignment of the entirety of the read,  xx , and a substring of the genome,  yy . Below is a sketch of what
             a traceback looks like for this task.

            TASK:
            Implement the dynamic programming algorithm described above as a function align_read_to_genome_with_skips below, that takes as 
            input a read sequence, x, a genome sequence, y, a substitution matrix, a space score, a skip score, and a list of intervals in 
            the genome that may be "skipped."

            Your function should output a tuple of three elements:

            1. an optimal alignment (with '=' denoting skips and '-' denoting spaces)
            2. the score of the optimal alignment
            3. the start position of the given alignment within the genome (i.e., the position of the aligned genomic substring within the genome).

            Your implementation must use an efficient (polynomial-time) dynamic programming algorithm (i.e., either top-down or bottom-up).

            TIE-BREAKING:
            In the case that there are multiple optimal alignments, during the traceback, if there are ties for which case of the recurrence 
            gives the maximum, use the case that traces back to a cell with coordinates that are lexicographically largest. For example, if 
            a cell has traceback pointers to cells  (i,j)(i,j) , and  (k,l)(k,l) , traceback to  (i,j)(i,j)  if  (i,j)>(k,l)(i,j)>(k,l)  and 
            to  (k,l)(k,l)  if  (k,l)>(i,j)(k,l)>(i,j) .
    
            Similarly, if there are multiple cells in the last row that have the maximum value, choose the cell with coordinates  (i,j)(i,j)  
            that are lexicographically largest.

            ASSUMPTIONS:
            You may assume that the lengths of all skip intervals are greater than one.
        '''

        taskType = 'READ_TO_GENOME_DYNAMIC_ALIGNMENT_SKIPS'
        data = {
            'read_sequence': readSequence,
            'genome_sequence': genomeSequence,
            'substitution_matrix': substitutionMatrix,
            'skip_intervals': skipIntervals,
            'space_score': spaceScore,
            'skip_score': skipScore
        }
        dataStructure = self._DataStructureDriver.buildApplicationDataStructure(taskType, data)
        return self._TaskDriver.execute(taskType, dataStructure)
    
    def identifySubgenomicRNAVariants(self, readsFile, genomeFile, subMatrix, spaceScore, skipIntervals, skipScore):
        readsFileContents = self._FileUtils.readFastaFile(readsFile)
        genomeFileContents = self._FileUtils.readFastaFile(genomeFile)
        genomeName = genomeFileContents[0][0]
        genomeSequence = genomeFileContents[0][1]
        
        skipIntervalList = []
        for key in skipIntervals:
            curSkipInterval = skipIntervals[key]
            skipIntervalList.append(curSkipInterval)

        skipIntervalLengthsDict = collections.defaultdict()
        for key in skipIntervals:
            curSkipInterval = skipIntervals[key]
            skipIntervalLengthsDict[key] = (curSkipInterval[1] - curSkipInterval[0]) + 1

        alignmentDict = collections.defaultdict()
        for readIndex in range(len(readsFileContents)):
            curRead = readsFileContents[readIndex]

            curReadName = curRead[0]
            curReadSequence = curRead[1]

            alignmentDict[curReadName] = self.readToGenomeAlignmentWithSkipsDynamicProgramming(curReadSequence, genomeSequence, subMatrix, spaceScore, skipIntervalList, skipScore)

        taskType = 'SUBGENOMIC_RNA_VARIANT_IDENTIFICATION'
        metadata = {
            'variant_length_dict': skipIntervalLengthsDict
        }
        return self._TaskDriver.execute(taskType, alignmentDict, metadata)