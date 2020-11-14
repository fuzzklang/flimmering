# DATA LIST CONSTRUCTOR

# Making list of multiples based on ratios

def get_multiples(ratio, n):
    """ Makes a list of multiples based on ratio
    and how many values to make (n).
    Formula: <ratio ** i> for each i from 0 to n
    """
    ls = [ratio ** i for i in range(n)]
    return ls

def get_multiples_list(ratios, n):
    """ Makes list of lists of multiples.
    All sublists share length (n).
    Output-format:
    [
    [x1, x2, x3, x4, x5],
    [y1, y2, y3, y4, y5],
    [z1, z2, z3, z4, z5]
    ]
    """
    out_list = []
    for ratio in ratios:
        temp_list = get_multiples(ratio, n)
        out_list.append(temp_list)
    return out_list
