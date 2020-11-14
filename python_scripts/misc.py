# MISCELLANOUS FUNCTIONS WHICH COME IN HANDY

def get_total_duration(seq):
    total_duration = 0
    begin = 0
    if seq[0]["type"] == "header":  # Checking for header or not
        begin = 1
    for event_dict in seq[begin:]:
        total_duration += event_dict["duration"]
    return total_duration

def print_dict(dictionary):
    for key in dictionary:
        print("\n-------\n\n{}\n".format(key))
        for i in dictionary[key] :
            print(i)
    print("\n")

def print_seq(seq, start=0, end=None):
    if end == None:
        end = len(seq)

    for elem in seq[start:end]:
        print()
        for key in elem:
            print(key, ":", elem[key])

def flatten_1st_depth_list(ls):
    out_list = []
    for l in ls:
        for i in l:
            out_list.append(i)
    return out_list


def get_colors_list(frame_sequence):
    """ Returns a list of all colors in a frame_sequence """
    colors = []
    if frame_sequence[0]["type"] == "header":
        start = 1
    else:
        start = 0
    for dic in frame_sequence[start:]:
        if dic["color"] not in colors:
            colors.append(dic["color"])
    return colors


def get_shapes_list(frame_sequence):
    """ Returns a list of all shapes in a frame_sequence """
    shapes = []
    if frame_sequence[0]["type"] == "header":
        start = 1
    else:
        start = 0
    for dic in frame_sequence[start:]:
        if dic["shape"] not in shapes:
            shapes.append(dic["shape"])
    return shapes


def get_text_elems_list(frame_sequence):
    """ Returns a list of all text_elems in a frame_sequence """
    text_elems = []
    if frame_sequence[0]["type"] == "header":
        start = 1
    else:
        start = 0
    for dic in frame_sequence[start:]:
        if dic["text"] not in text_elems:
            text_elems.append(dic["text"])
    return text_elems


def insert_every_second_black_frame(in_list, insert_at_start=True, insert_at_end=True):
    """
    Takes a list of values and inserts None.
    Optionally not insert empty frame at start end and of list. Default: True
    """
    out_list = []
    count = 0
    idx = 0
    if insert_at_start == True:
        beg = 1
    else:
        beg = 0

    while count < len(in_list) * 2:    # Adding one None for each value in in_list, thus twice the length
        if count % 2 == 0 + beg:
            # Idx from i (even number, 2, 4, 6) to range 0 -> len(color_pool) (here: 3)
            out_list.append(in_list[idx])
            count += 1
            idx += 1
        else:
            #out_list.append("Black")   # If breakage, uncomment this one
            out_list.append(None)       # and remove this line
            count += 1

    if insert_at_start == False and insert_at_end == False: # Removing the None which is added in loop when insert_at_start is False
        del out_list[-1]
    elif insert_at_start == False and insert_at_end == True:
        pass
    elif insert_at_start == True and insert_at_end == False:
        pass
    else:   # Adding the last None which is not added in loop when insert_at_start is True
        out_list.append(None)

    return out_list


def get_framerate_from_header(sequence, default):
    """
    Takes a sequence (list) and a default value (integer) as parameters.
    Checks if there is header in sequence.
    Returns default if not.
    Returns framerate if there is.
    """
    if sequence[0]["type"] == "header":
        framerate = sequence[0]["framerate"]
    else:
        framerate = default
    return framerate


def get_n_digits_from_header(sequence, default):
    """
    Takes a sequence (list) and a default value (integer) as parameters.
    Checks if there is header in sequence.
    Returns default if not.
    Returns n_digits_if_there_is"""
    if sequence[0]["type"] == "header":
        n_frames = sequence[0]["num_frames"]
        n_digits = len(str(n_frames))   # Checking for max digits in number
    else:
        n_digits = default
    return n_digits


def check_and_adjust_list_length(ref_list, adj_list):
    """
    Takes two lists as parameter.
    Returns only the adjusted list, since it is assumed that the reference
    list remains unmodified.
    Returns an error if receiving any empty lists.

    Adjusts the length of the adjustment-list (adj_list) so that it's length
    is the same as the length of the reference-list (ref_list).
    If adj_list is shorter than ref_list, adj_list's values are "cycled through",
    repeated until it reaches the same length as ref_list.
    (e.g:
    ref_list = ["r", "g", "b", "r", "g", "b"]
    adj_list = [1, 2]
    -->
    adj_list = [1, 2, 1, 2, 1, 2])
    """
    assert len(ref_list) > 0 and len(adj_list) > 0, "\n\nEmpty lists received, returning error.\n[In function 'check_and_adjust_list_length' in module 'misc']\n"
    if len(ref_list) < len(adj_list):
        adj_list = adj_list[0:len(ref_list)]
    else:
        idx = 0
        while len(ref_list) > len(adj_list):
            adj_list.append(adj_list[idx])
            idx += 1
    return adj_list


def flatten_n_depth_list(ls):
    """
    Takes a list of unknown elements (lists or items)
    and of unknown depth and flattens it to one list.
    Can handle lists, numbers, bools or strings as elems,
    but not dictionaries.
    """
    out_list = []

    def rec_func(in_list, out_list):
        for elem in in_list:
            if type(elem) == type(list()):
                out_list = rec_func(elem, out_list)
            else:
                out_list.append(elem)
        return out_list

    return rec_func(ls, out_list)


def escape_newlines(string):
    """
    Takes a string and returns a new string equal to the string given,
    except that all newlines '\n' have been escaped with an '\\' character.
    """
    new_string = ""
    for char in string:
        if char == "\n":
            new_string = new_string + "\\n"
        else:
            new_string += char
    return new_string


def lin_interpol(beg, end, steps, i):
    """
    Takes a start value (beg), an end value (end), number of steps between them,
    (steps), and the current step (i) and returns the value at that step.
    Interpolates linearily.
    Catches ZeroDivisionCases by adjusting steps if steps <= 1.
    In those cases, where only one (1) steps is given, it instead adjusted to 2.
    """
    if steps <= 1:
        steps = 2
    return ((end-beg) / (steps - 1) * i) + beg


def exp_interpol(beg, end, steps, i):
    """
    Takes a start value and an end value, the number of steps between them
    (steps) and the current step (i), and returns the value at that step.
    Interpolates exponentially.
    Catches ZeroDivisionCases by adjsuting if steps <= 1.
    In those cases the only one (1) as 'steps'-value is given, it is instead
    adjusted to 2.
    (This to ensure that when i = 0, beg value is returned,
    and when i = steps, end value is returned.)

    Args: beg, end, steps, i;

    Formula:    (end / beg ** (i/steps)) * beg

        or:     x ** (i/n) * y

    With range from 'y' to 'x * y' (when 'i' is smaller or equal to 'n'),
    with 'n' steps (exponentially distributed) between y and x * y and where 'i'
    is the current step.
    """
    if steps <= 1:
        steps = 2
    return ((end / beg) ** (i / (steps - 1))) * beg
