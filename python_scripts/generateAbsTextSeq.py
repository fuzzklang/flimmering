# GENERATE ABS SEQUENCE

# The functions here should generate a list of dictionaries
# each containing information about color/shape and absolute duration

from misc import get_total_duration

def generate_abs_text_seq(duration_seq, text_seq, font_size=90, font='/System/Library/Fonts/Menlo.ttc', header_framerate=None):
    """ GENERATE_ABS_SEQUENCE
    Function for generating a sequence of dictionaries containing
    info on text-string and duration for each of these.

    If a header_framerate is passed it will be added to beginning of the sequence.
    The header_framerate must be passed as an integer representing fps.
    If no header_framerate is given, the sequence will begin directly with the
    ordinary dictionaries containing the aforementioned attributes.

    Text is passed as a string of arbitrary length. (though limits on size and
        fitting to image may occur)
    Duration is given in seconds.
    Font_size is given as integer (default: 48).
    Font is given as a path. (default: '/System/Library/Fonts/Menlo.ttc')
    Should also handle black frames and make frame dictionaries which makes
    black images. (Problematic format/naming for those. "Black" at the moment.
    Should be changed for later, but risks breakage with the image sequences ++)

    Example, output format:
    [
    {"type" : "header", "framerate" : 30, "num_frames" : 100},
    {"type" : "text_event", "event_num" : 0, "text" : "Word1", "duration" : 0.5},
    {"type" : "text_event", "event_num" : 1, "text" : "Word2", "duration" : 1.5}
    ...,
    {"type" : "text_event", "event_num" : 99, "text" : "Word100", "duration" : 0.75}
    ]
    """

    # Checking that the lists corresponds in length. If not, raises Error
    def raiseUnequalListError():
        raise RuntimeError("Length of data lists are not equal. In function 'generate_abs_text_seq'. Interrupting program")

    if len(duration_seq) != len(text_seq):
        raiseUnequalListError()


    sequence = []

    def get_black_event_dict(idx, dur):
        event_dict = {
            "type" : "text_event",
            "event_num" : idx,
            "text" : text_seq[idx], # Get text elem from text_seq
            "duration" : dur
            }
        return event_dict

    def get_event_dict(idx, dur):
        event_dict = {
            "type" : "text_event",
            "event_num" : idx,
            "text" : text_seq[idx], # Get text elem from text_seq
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
                        "total_duration" : total_duration,
                        "font_size" : font_size,    # Sticking font size
                        'font' : font     # and font to header. (good idea?)
                        }
        sequence.insert(0, header_dict)

    return sequence
