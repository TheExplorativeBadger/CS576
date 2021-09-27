import itertools

def overlap_length(left, right):
    """Returns the length of the longest suffix of left that is a prefix of right
    
    Args:
        left: a string
        right: a string
    Returns:
        An integer length of the longest overlap (0 if there is no overlap)
    """
    counter = 0
    overlapCount = 0
    continueLooping = True
    while continueLooping == True:
        leftPrefix = left[counter:len(left)]
        if (right.startswith(leftPrefix)):
            overlapCount = len(left) - counter
            continueLooping = False
        else:
            counter += 1
            if (counter == len(left)):
                continueLooping = False

    return overlapCount

def merge_ordered_reads(reads):
    """Returns the shortest superstring resulting from
    merging a list of ordered reads.
    
    Args:
        reads: a list of strings
    Returns:
        A string that is a shortest superstring of the ordered input read strings.
    """

    shortestSuperstring = ""
    if (len(reads) != 0):
        shortestSuperstring = reads[0]
        for i in range(len(reads)-1):
            leftRead = reads[i]
            rightRead = reads[i+1]
            overlapCount = overlap_length(leftRead, rightRead)
            superstringAddition = rightRead[overlapCount:len(rightRead)]
            shortestSuperstring = shortestSuperstring + superstringAddition
    
    return shortestSuperstring

def shortest_superstring(reads):
    """Returns the shortest superstring of a set of reads.

    Assumes that no string in the input is a substring of another input string.
    
    Args:
        reads: a list of strings
    Returns:
        A string that is a shortest superstring of reads.  In the case
        of multiple shortest superstrings, the lexicographically
        smallest is returned.
    """
    shortestSuperstringLength = 9223372036854775807
    shortestSuperstrings = []
    for ordering in itertools.permutations(reads):
        shortestPermSuperstring = merge_ordered_reads(list(ordering))
        if len(shortestPermSuperstring) < shortestSuperstringLength:
            shortestSuperstringLength = len(shortestPermSuperstring)
            shortestSuperstrings = [shortestPermSuperstring]
        elif len(shortestPermSuperstring) == shortestSuperstringLength:
            shortestSuperstrings.append(shortestPermSuperstring)

    shortestSuperstrings.sort()
    return shortestSuperstrings[0]