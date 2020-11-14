# RENDER SEQUENCE TO FRAME SEQUENCE
#
# The functions here should render a list of absolute values
# to a list of dictionaries containing information for one frame each

# Also with Discrepancy check
# (comparing actual number of frames generated with expected number of frames)

from misc import get_total_duration

def render_text_frame_sequence(abs_sequence, framerate=30, header=True):
    """ This function generates a Sequence of dictionaries, each containing
    info on a frame to be generated.

    The function returns a list of dictionaries in the following format (example):
    [
    {"type" : "header", "framerate" : 30, "num_frames" : 200, },
    {"type" : "text_frame", "frame_num" : 0, "text" : "Word1"},
    {"type" : "text_frame", "frame_num" : 1, "text" : "Word1"},
    ...,
    {"type" : "text_frame", "frame_num" : 200, "text" : "Word50"},
    ]
    """
    def get_frame_dict(frame_num, text):
        event_dict = {  "type"  : "text_frame",
                        "frame_num" : frame_num,
                        "text" : text
                        }
        return event_dict


    frame_sequence = []

    global_frame_num = 0
    local_frame_check = 0
    total_duration = 0

    if abs_sequence[0]["type"] == "header":
        begin = 1
        framerate = abs_sequence[0]["framerate"]
        font = abs_sequence[0]["font"]              # get font and
        font_size = abs_sequence[0]["font_size"]    # font size from there
        framerate = abs_sequence[0]["framerate"]
    else:
        begin = 0
        font = '/System/Library/Fonts/Menlo.ttc'    # Set default font and
        font_size = 48                              # default font size if no header


    for idx, event_dict in enumerate(abs_sequence[begin:]):
        #print("     NEW EVENT\n", event_dict)
        duration = event_dict["duration"]
        total_duration += duration          # Registers total_duration so far

        # Sets number of frames for this particular event:
        number_of_frames = int(round(framerate * duration))

        text = event_dict["text"]

        for frame in range(number_of_frames):
            frame_dict = get_frame_dict(frame_num=global_frame_num, text=text)
            #print("frame_dict['frame_num']", frame_dict['frame_num'])
            frame_sequence.append(frame_dict)   # Add dicts to out_sequence
            global_frame_num += 1
            local_frame_check += 1


        # Expected numbers of frames so far based on total_duration:
        expected_number_of_frames = int(round(total_duration * framerate))

        # --- Discrepancy check ---
        # Expected number of frames compared to local_frame_num:
        discrepancy = expected_number_of_frames - local_frame_check

        if discrepancy > 0:
            # If too few frames generated. Adding the ones lacking to the frame_sequence.
            # Generate n frames, where n = discrepancy.
            # The added frames are copies of the last frame in the frame_sequence.
            # For each frame global_frame_num += 1 and local_frame_check += 1
            text = frame_sequence[-1]["text"]
            for i in range(discrepancy):
                frame_dict = get_frame_dict(global_frame_num, text=text)
                frame_sequence.append(frame_dict)
                global_frame_num += 1
                local_frame_check += 1

        elif discrepancy < 0:   # If too many frames are generated.
            #print("DISCREPANCY")
            #print("global_frame_num before", global_frame_num)
            # Deletes the extra dictionaries in the frame_sequence
            del frame_sequence[discrepancy:]    # (Discrepancy is already a negative value)
            global_frame_num += discrepancy     # Adds negative value of discrepancy
            local_frame_check += discrepancy
            #print("global_frame_num after", global_frame_num)


    # ADD HEADER (needs to know exactly number of events)
    if header:
        header = {  "type" : "header",
                    "framerate" : framerate,
                    "num_frames" : len(frame_sequence),
                    "font" : font,
                    "font_size" : font_size
                    }
        frame_sequence.insert(0, header)

    return frame_sequence
