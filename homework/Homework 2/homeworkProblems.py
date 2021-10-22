from application_driver.ApplicationDriver import ApplicationDriver

MainApplicationDriver = ApplicationDriver()

def align_read_to_genome_with_skips(x, y, S, s, R, r):
    """Computes a read-to-genome alignment with possible skips.
    
    Args:
        x: a string representing the read sequence
        y: a string representing the genome sequence
        S: a substitution matrix (represented as a dictionary)
        s: the space score
        T: a list of intervals in the genome that may be "skipped".  Each interval
           is represented as a tuple (start_position, end_position), using 1-based indexing
           for positions.
        t: the skip score
    Returns:
        A tuple of three elements, (alignment, score, start_position), where
             alignment: a list of two strings representing the optimal alignment
                        in the alignment, '=' denotes a skip and '-' denotes a space
                 score: a numeric value giving the score of the alignment
        start_position: the start position (1-based indexing) of the
                        aligned genomic substring within the genome
    """    
    