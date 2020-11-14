# GENERATE ABS SEQUENCE

# The functions here should generate a list of dictionaries
# each containing information about color/shape and absolute duration

def get_total_duration(seq):
    total_duration = 0
    begin = 0
    if seq[0]["type"] == "header":  # Checking for header or not
        begin = 1
    for event_dict in seq[begin:]:
        total_duration += event_dict["duration"]
    return total_duration


def generate_abs_seq(duration_seq, color_seq=None, shapes=None, header_framerate=None):
    """ GENERATE_ABS_SEQUENCE
    Function for generating a sequence of dictionaries containing
    info on color_seq, shapes and duration for each of these dictionaries.

    If a header_framerate is passed it will be added to beginning of the sequence.
    The header_framerate must be passed as an integer representing fps.
    If no header_framerate is given, the sequence will begin directly with the
    ordinary dictionaries containing the aforementioned attributes.

    Color is given in "R", "G" or "B".
    Duration is given in seconds.
    Shapes in "Triangle", "Circle" or "Rectangle".

    Example, output format:
    [
    {"type" : "header_framerate", "framerate" : 30, "num_frames" : 100},
    {"type" : "event", "event_num" : 0, "color" : "R", "shape" : "Circle", "duration" : 0.5},
    {"type" : "event", "event_num" : 1, "color" : "G", "shape" : "Square", "duration" : 1.5}
    ...,
    {"type" : "event", "event_num" : 99, "color" : "B", "shape" : "Triangle", "duration" : 0.75}
    ]
    """

    # Checking that the lists corresponds in length. If not, raises Error
    def raiseUnequalListError():
        raise RuntimeError("Length of data lists are not equal. In function 'generate_abs_seq'. Interrupting program")

    if shapes != None and color_seq != None:
        if len(duration_seq) != len(color_seq) or len(duration_seq) != len(shapes):
            raise RuntimeError("Need at least one list of either color_seq or shapes\
             given as argument to function 'generate_abs_seq'. \nInterrupting program")
    elif shapes and color_seq == None:
        if len(duration_seq) != len(shapes):
            raiseUnequalListError()
    elif color_seq and shapes == None:
        if len(duration_seq) != len(color_seq):
            raiseUnequalListError()
    else:
        if len(duration_seq) != len(color_seq) or len(duration_seq) != len(shapes):
            raiseUnequalListError()

    sequence = []

    default_shapes = {
        "R" : "Circle",
        "G" : "Rectangle",
        "B" : "Triangle",
        "Black" : "None",
        "Tuple" : "Rectangle",
        "None" : None}
    default_color_seq = {
        "Circle" : "R",
        "Rectangle" : "G",
        "Triangle" : "B",
        "None" : None}

    def get_event_dict(idx, dur):
        if color_seq == None:
            event_dict = {
                "type" : "event",
                "event_num" : idx,
                "color" : default_color_seq[shapes[idx]], # Get color from default_color_seq
                "shape" : shapes[idx],                 # Get shape from parameter list
                "duration" : dur
                }

        elif shapes == None:
            if type(color_seq[idx]) == type(tuple()):
                shape = default_shapes["Tuple"]        # If color is a tuple and not a string
            else:
                shape = default_shapes[str(color_seq[idx])] # String to convert possible None to "None"

            event_dict = {
                "type" : "event",
                "event_num" : idx,
                "color" : color_seq[idx],
                "shape" : shape,                       # Get shape from default_shapes. 'shape' is defined in previous conditional statements.
                "duration" : dur
                }

        elif shapes:
            event_dict = {
                "type" : "event",
                "event_num" : idx,
                "color" : color_seq[idx],
                "shape" : shapes[idx],   # Get shape from 'shapes' list
                "duration" : dur
                }
        return event_dict


    for idx, duration in enumerate(duration_seq):
        event_dict = get_event_dict(idx, duration)
        sequence.append(event_dict)

    if header_framerate:
        total_duration = get_total_duration(sequence)
        header_dict = { "type" : "header",
                        "framerate" : header_framerate,
                        "num_events" : len(duration_seq),
                        "total_duration" : total_duration}
        sequence.insert(0, header_dict)

    return sequence





# ----- PRINTING/TESTING -----
"""
duration_seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
color_seq = ["R", "G", "B", "R", "G", "B", "R", "G", "B",]

duration_seq = [1, 2, 3, 4]
color_seq = ["R", "G", "B", "R"]
shapes = ["Triangle", "Circle", "Square", "XXX"]

seq = generate_abs_seq(duration_seq, color_seq, shapes=shapes, header_framerate=30)
#for i in seq:
#    print(i)


#print(generate_abs_seq.__doc__)
print(seq)

print("TOTAL_DURATION:", seq[0]["total_duration"])
"""
