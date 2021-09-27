import random
from . import dnaBasics

def kmer_spectrum(dna_sequence, k):
    """Gives the k-mer spectrum of a DNA sequence.
    
    Args:
        dna_sequence: a DNA sequence
        k: an integer length
    Returns:
        A set object containing all unique k-mers within dna_sequence
    """
    
    returnSet = set()
    
    if k <= len(dna_sequence):
        for i in range(len(dna_sequence) - k + 1):
            returnSet.add(dna_sequence[i:i+k])
    
    return returnSet


def getKmerSpectrums(dnaSequence, k):
    k_values = range(1, k+1)
    spectrum_sizes = []

    for i in k_values:
        kmerSpectrumSet = kmer_spectrum(dnaSequence, i)
        spectrum_sizes.append(len(kmerSpectrumSet))
    return spectrum_sizes

def random_cuts(length, k):
    """Generates a random set of k distinct cut positions along a DNA sequence of a given length.
    
    Args:
        length: an integer specifying the length of the sequence
        k: the number of distinct cut positions
    Returns:
        A sorted list of k integers, representing the cut positions, with a cut position i representing
        a cut immediately after the ith base of the sequence.
    """
    randomSamples = random.sample(range(1, length),k)
    randomSamples.sort()
    return randomSamples

def fragment_dna(length, k):
    """Randomly cuts a sequence of a given length into k fragments.
    
    Args:
        length: an integer specifying the length of the sequence
        k: the number of fragments that should result from random cuts
    Returns:
        A sorted list of fragment intervals, where each interval
        is specified as a tuple (start, end).  For each interval, 
        the coordinates are 0-based and the end coordinate is 
        *not* included in the fragment.
    """
    cut_positions = random_cuts(length, k)
    sliceList = []
    startIndex = 0
    for cut in cut_positions:
        sliceList.append((startIndex, cut))
        startIndex = cut
    sliceList.append((startIndex,length))
    return sliceList

def fragment_multiple_dna_copies(length, k, num_copies):
    """Randomly cuts multiple sequences of a given length, each sequence
    cut into k fragments.
    
    Args:
        length: an integer specifying the length of each sequence
        k: the number of fragments that should result from each sequence
        num_copies: the number of sequences
    Returns:
        A sorted list of fragment intervals from all sequences, where intervals
        are represented in the same way as for the fragment_dna function.
    """
     
    intervals = []
    for i in range(num_copies):
        intervals.extend(fragment_dna(length, k))
    return sorted(intervals)

def filter_for_long_fragments(fragment_list, min_length):
    """Returns a list of all fragments that are at least as long as a
    given minimum length.

    Args:
        fragment_list: a list of fragments, in the format returned by fragment_dna
        min_length: the minimum length of a fragment to return in the output
    Returns:
        A list of fragments.
    """
    return list(filter(lambda x: x[1] - x[0] >= min_length, fragment_list))

def sample_fragments(fragment_list, num_fragments):
    """Randomly samples a specified number of fragments from a 
    a list of fragments without replacement.
    
    Args:
        fragment_list: a list of fragments, in the format returned by fragment_dna
        num_fragments: the number of fragments to randomly sample from the list
    Returns:
        A sorted list of fragments.
    """
    if (num_fragments > len(fragment_list)):
        raise ValueError("The number of fragments to be sampled ({0}) is larger than the fragment pool ({1})".format(num_fragments, len(fragment_list)))
    return sorted(random.sample(fragment_list, num_fragments))

def read_fragment(fragment, read_length):
    """Returns the interval sequenced from one end of a given fragment, 
    given a maximum read length and a randomly sampled orientation.
    
    Args:
        fragment: a fragment, represented as a tuple (start, end)
        read_length: the maximum length of a read
    Returns:
        The interval of the read, represented as a tuple (start, end, orientation),
        where orientation is "+" for a forward strand read and "-" for a reverse strand
        read. If the fragment is shorter than the maximum read length, the entire fragment
        is read.
    """
    
    strand = random.choice("+-")
    startIndex = fragment[0]
    endIndex = fragment[1]
    if (strand == "+"):
        if fragment[0] + read_length <= fragment[1]:
            endIndex = fragment[0] + read_length
        else:
            endIndex = fragment[1]
    else:
        if fragment[1] - read_length >= fragment[0]:
            startIndex = fragment[1] - read_length
        else:
            startIndex = fragment[0]
    
    return (startIndex, endIndex, strand)

def simulate_shotgun_sequencing_read_intervals(genome_length, 
                                               num_copies, 
                                               k,
                                               min_fragment_length,
                                               num_fragments, 
                                               read_length):
    """Simulates shotgun sequence read intervals.
    
    Args:
        genome_length: the integer length of the DNA sequence
        num_copies: the number of identical copies of the DNA in the sample
        k: the number of cuts in each DNA during fragmentation
        min_fragment_length: the minimum length of a fragment to be sequenced
        num_fragments: the number of fragments to sequence
        read_length: the length of the reads
    Returns:
        A list of oriented read intervals, each represented as a tuple (start, end, orientation)
    """    
    finalFilteredFragmentList = []
    unfilteredFragmentList = fragment_multiple_dna_copies(genome_length, k, num_copies)
    lengthFilteredFragmentList = filter_for_long_fragments(unfilteredFragmentList, min_fragment_length)
    quantityFilteredFragmentsList = sample_fragments(lengthFilteredFragmentList, num_fragments)
    for fragment in quantityFilteredFragmentsList:
        finalFilteredFragmentList.append(read_fragment(fragment, read_length))
    return finalFilteredFragmentList

def read_coverage(read_intervals, genome_length):
    """Computes the number of reads covering (overlapping) each position
    along the genome.
    
    Args:
        read_intervals: a list of oriented read intervals
        genome_length: the integer length of the genome sequence
    Returns:
        A list of coverage values with the ith entry in the list giving
        the read coverage at position i in the genome.
    """    
    num_reads_starting = [0] * genome_length
    num_reads_ending = [0] * genome_length
    for start, end, strand in read_intervals:
        num_reads_starting[start] += 1
        num_reads_ending[end - 1] += 1
    coverage = [0] * genome_length
    coverage[0] = num_reads_starting[0]
    for i in range(1, genome_length):
        coverage[i] = coverage[i - 1] - num_reads_ending[i - 1] + num_reads_starting[i] 
    return coverage

def sequence_for_read_interval(read_interval, genome_sequence):
    """Returns the sequence of a read given its oriented interval along
    a genome sequence.
    
    Args:
        read_interval: an oriented read interval, represented as a tuple (start, end, orientation)
        genome_sequence: the genome sequence as a string
    Returns:
        The sequence of the read as a string.
    """    
    returnSequence = ""
    if (read_interval[2] == "+"):
        returnSequence = genome_sequence[read_interval[0] : read_interval[1]]
    else:
        returnSequence = dnaBasics.reverse_complement(genome_sequence[read_interval[0] : read_interval[1]])
    return returnSequence

def simulate_shotgun_sequencing_reads(genome_sequence, 
                                      num_copies, 
                                      k,
                                      min_fragment_length,
                                      num_fragments, 
                                      read_length):
    """Simulates shotgun sequence reads from a genome.
    
    Args:
        genome_sequence: the genome sequence as a string
        num_copies: the number of identical copies of the DNA in the sample
        k: the number of cuts in each DNA during fragmentation
        min_fragment_length: the minimum length of a fragment to be sequenced
        num_fragments: the number of fragments to sequence
        read_length: the length of the reads
    Returns:
        A list of read sequences.
    """    
    
    read_intervals = simulate_shotgun_sequencing_read_intervals(len(genome_sequence),
                                                                num_copies,
                                                                k,
                                                                min_fragment_length,
                                                                num_fragments,
                                                                read_length)
    reads = [sequence_for_read_interval(interval, genome_sequence)
             for interval in read_intervals]
    return reads