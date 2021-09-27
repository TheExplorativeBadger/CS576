def complement(base):
    if base == 'A':
        return 'T'
    elif base == 'T':
        return 'A'
    elif base == 'C':
        return 'G'
    elif base == 'G':
        return 'C'
    else:
        raise ValueError(base + " is not a valid DNA base")
    return

def reverse_complement(s):
    # we first start with an empty list
    opposite_bases = []
    # using a for loop, we loop through the bases of s in *reverse* order
    # and append the complementary base to the opposite bases list
    for base in reversed(s):
        opposite_bases.append(complement(base))
    # we can use the 'join' method with an empty string
    # to concatenate all strings in the list
    return ''.join(opposite_bases)