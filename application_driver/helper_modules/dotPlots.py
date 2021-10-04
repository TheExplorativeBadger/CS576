from helper_modules import submatrix

def dot_plot_points(seq1, seq2):
    """Computes the coordinates of the points in a dot plot for seq1 compared to seq2.
    A point, (x,y), in such a plot represents positions at which seq1[x] == seq2[y].

    Args:
        seq1: the first string
        seq2: the second string
    Returns:
        A list of points, where each point is represented as a tuple, (x, y)
    """
    responseCoordinatesList = []
    for characterIndex in range(len(seq1)):
        for secondaryCharacterIndex in range(len(seq2)):
            
            if seq1[characterIndex] == seq2[secondaryCharacterIndex]:
                responseCoordinatesList.append((characterIndex, secondaryCharacterIndex))

    return responseCoordinatesList

def data_frame_from_tuple_list(tuples, column_names):
    """Converts a tabular dataset from a row-based data structure to a 
    column-based data structure.

    Args:
        tuples: a list of rows, where each row is a tuple of the same length
        column_names: a list of strings giving the names of the columns
    Returns:
        A dictionary with column names as keys and columns as values.
    """    
    columns = zip(*tuples) if tuples else [[] for i in range(len(column_names))]
    return dict(zip(column_names, columns))

def dot_plot_points_with_matrix(seq1, seq2, matrix):
    """Computes the coordinates and scores of the points in a dot plot for seq1 compared to seq2.
    
    A point, (x,y), in such a plot represents positions at which matrix[(seq1[x], seq2[y])] > 0, i.e.,
    only points with positive score are returned.

    Args:
        seq1: the first string
        seq2: the second string
        matrix: a substitution matrix, using the representation of the submatrix module
    Returns:
        A list of scored points, where each point is represented as a tuple, (x, y, score)
    """
    responseCoordinatesList = []
    for characterIndex in range(len(seq1)):
        for secondaryCharacterIndex in range(len(seq2)):
            currentScore = matrix[(seq1[characterIndex], seq2[secondaryCharacterIndex])]
            if currentScore > 0:
                responseCoordinatesList.append((characterIndex, secondaryCharacterIndex, currentScore))
    return responseCoordinatesList

def dot_plot_kmer_points(seq1, seq2, k):
    """Computes the coordinates of the points in a k-mer dot plot for seq1 compared to seq2.
    
    A point, (x,y), in such a plot represents positions at which the length k substrings 
    starting at position x in seq1 and position y in seq2 are identical.

    Args:
        seq1: the first string
        seq2: the second string
        k: the length of the substrings to compare
    Returns:
        A list of points, where each point is represented as a tuple, (x, y)
    """
    responseCoordinatesList = []
    for characterIndex in range(len(seq1)):
        if (characterIndex + k) <= len(seq1):
            lengthKSeq1 = seq1[characterIndex : characterIndex + k]
            for secondaryCharacterIndex in range(len(seq2)):
                if (secondaryCharacterIndex + k) <= len(seq2):
                    lengthKSeq2 = seq2[secondaryCharacterIndex : secondaryCharacterIndex + k]

                    if lengthKSeq1 == lengthKSeq2:
                        responseCoordinatesList.append((characterIndex, secondaryCharacterIndex))
    return responseCoordinatesList

def score_alignment(alignment, matrix, space_penalty):
    """Scores an alignment with the given substitution_matrix and space_penalty.
    Assumes a linear gap penalty, i.e., that the score of a length k gap is w(k) = space_penalty * k
    
    Args:
        alignment: a list of two strings, each string representing one row of the alignment
        matrix: a substitution matrix, using the representation of the submatrix module
        space_penalty: a number giving the score of an individual space in the alignment.
    Returns:
        A number representing the score of the alignment.
    """
    alignmentScore = 0
    string1 = alignment[0]
    string2 = alignment[1]
    stringIndexRange = range(len(string1))
    
    for charIndex in stringIndexRange:
        if string1[charIndex] == "-" or string2[charIndex] == "-":
            alignmentScore += space_penalty
        else:
            alignmentScore += matrix[(string1[charIndex], string2[charIndex])]
    return alignmentScore

def get_blosum62_submatrix():
    return submatrix.read_substitution_matrix("BLOSUM62.txt")
