def get_ratios(n, symbolic=False):
    """Constructs list of harmonious ratios (1/1, 2/1, 3/2, 4/3 etc).
    Returns either a list of floats (if param symbolic==False) or a list
    of whole ratios represented as strings (if param symbolic==True)
    ('1/1', '2/1' etc.)
    """

    ratios = []

    if symbolic == True:
        for i in range(n):
            if i == 0:
                ratios.append("1/1")
            else:
                ratios.append(str(i+1)+"/{}".format(i))

        return ratios

    for i in range(n):
        i += 1                      # To avoid ZeroDivisionError. Begins on 1, not 0
        ratios.append((i+1) / i)    # 2/1, 3/2, 4/3 etc.

        ## OLD VERSION. Will append 1/1 to beginning
        ## (which returns some unexpected results when this function is used at
        ## a later stage in other scripts.)
        #if i == 0:
        #    ratios.append(1)            # 1 / 1
        #else:
        #    ratios.append((i+1) / i)    # 2/1, 3/2, 4/3 etc.

    return ratios


def get_averages(in_list):
    """ Constructs a list of the average value from every value in the list given as param.
    in: [1, 0.5, 0.25] --> out: [0.75, 0.375]
    Thus, the list returned contains one item less than the in_list."""

    out_list = []

    if len(in_list) <= 1:   # Exits the function and returns []
        return out_list     # if there are less than 2 items in in_list

    for idx, i in enumerate(in_list[0:-1]):     # Cuts the last idx, because it's accessed in the next line
        avg = (i + in_list[idx + 1]) / 2        # Average of current item and next (idx + 1) item
        out_list.append(avg)

    return out_list


def make_union(data):
    """Returns a sorted list containing all the combined values
    in one level nested lists or dictionaries"""
    out_list = []
    if type(data) == type(list()):
        for l in data:
            for i in l:
                out_list.append(i)

    elif type(data) == type(dict()):
        for key in data:
            for i in data[key]:
                out_list.append(i)

    out_list.sort()

    return out_list
