# Main script for generating text-frames

from generateAbsTextSeq import generate_abs_text_seq

from renderToTextFrameSeq import render_text_frame_sequence

from makeTextBaseImages import get_text_img_list_dict

from generateFrames import generate_frames

from makeAnimation import make_animation

from misc import get_text_elems_list
from misc import check_and_adjust_list_length
from misc import get_framerate_from_header
from misc import get_n_digits_from_header
from misc import insert_every_second_black_frame

from csvFunctions import write_from_seq_to_csv
from csvFunctions import simple_write_csv
from csvFunctions import read_csv

#from makeTextBaseFrames import get_txt_img_list_dict

#from misc import insert_every_second_black_frame

import datetime
import os

# ---------- GLOBAL VARIABLES AND PATHS ----------
now = datetime.datetime.now()
timestamp = "{}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
IMG_SIZE = (1920, 1280) # default size of video image
#IMG_SIZE = (800, 600)
FRAMERATE = 30           # framerate for video

# TODO: GET PROPER PATH
DIRECTORY = "flimmering"

FRAMEPATH = DIRECTORY + "/frames/textFrames/" + timestamp        # Creates subfolder for current run in /frames
VIDEOPATH = DIRECTORY + "/videos"                   # Export folder for videos
#CSV_PATH = DIRECTORY + "/csv_export_data/text/" + timestamp    # Export directory for csv-files
#JSON_PATH = DIRECTORY + "/json_data"               # Currently unused
TMP = DIRECTORY + "/tmp"                            # tmp directory for testing etc

# TEMPORARY FOR TESTING
FRAMEPATH = TMP + "/textFrames/" + timestamp
VIDEOPATH = TMP + "/textVideos/" + timestamp
CSV_PATH = TMP + "/csv_data/" + timestamp


# TEMPORARY FOR CREATING TEST FRAMES
#FRAMEPATH = DIRECTORY + "/frames/TEST-TEXT-FRAMES"
#CSV_PATH = DIRECTORY + "/csv_export_data/TEST-TEXT-DATA/" + timestamp
#VIDEOPATH = DIRECTORY + "/videos/TEST-TEXT-VIDEOS"




# MAKE NEEDED DIRECTORIES IF NOT EXISTING
if not os.path.exists(FRAMEPATH):
    os.makedirs(FRAMEPATH)

if not os.path.exists(VIDEOPATH):
    os.makedirs(VIDEOPATH)

if not os.path.exists(CSV_PATH):
    os.makedirs(CSV_PATH)

# Need functions that make text list
# text_elems = ["A", "B", "C"]
# durations = [1, 1, 1]
# and then make an absolute sequence of that. DONE
#   (special case needed for when font and font_size are not given.)    DONE
# Then translates it into a frame_sequence  DONE
# Then makes images based on content of text_elems
# And then creates frames from frame_sequence and text_elems_list




# -------------------- INSERT HERE --------------------
# ---------- DATA DECLARATIONS ----------
# ---------- (WRITING "SCORE") ----------

# MAIN PARAMETERS TO CONTROL:
IMG_CHANGE_FREQ = 1
ELEM_MINSIZE_MUL = 0.2
ELEM_MAXSIZE_MUL = 0.5
N = 10      # Number of images for each shape/color combination.

FONT = '/System/Library/Fonts/Menlo.ttc'
FONT_SIZE = 84


# ----- DATA SEQUENCES -----
text_seq = ["A", "B"*2, "C"*3, "a\nc", "\nv"]
text_seq = ["HEI DER", "DETTE ER FØRSTE FORSØK", "NÅ TAR DET AV!", "\nHIYAH!!!", "SE \nHVOR DET GÅR?"]
duration_seq = [0.5]


text_seq = insert_every_second_black_frame(text_seq)
duration_seq = check_and_adjust_list_length(ref_list=text_seq, adj_list=duration_seq)    # Returns the two lists as tuple

# -------------------- END INSERT --------------------



# ----- MAKING ABS_SEQ AND FRAME_SEQ -----
# Making absolute sequence:
abs_sequence = generate_abs_text_seq(duration_seq=duration_seq, text_seq=text_seq, header_framerate=30)
# Rendering to frame_sequence
frame_sequence = render_text_frame_sequence(abs_sequence)



# ----- MAKING BASIS IMAGES -------
# Checking which different strings are in frame sequence
text_elems = get_text_elems_list(frame_sequence)


#get_text_img_list_dict(n, minsize_mul, maxsize_mul, text_elems, img_size, font, font_size)
img_list_dict = get_text_img_list_dict(
                    n=N,        # Number of images of each text elem, global var N
                    minsize_mul=ELEM_MINSIZE_MUL,
                    maxsize_mul=ELEM_MAXSIZE_MUL,
                    text_elems=text_seq,
                    img_size=IMG_SIZE,
                    font=FONT,
                    font_size=FONT_SIZE
                    )



# ----- WRITE TO CSV FILE -----
write_from_seq_to_csv(directory_path=CSV_PATH, sequence=abs_sequence, csv_header_order=None)
# CSV-directory is created from 'now'-variable and specific for each run (in write_from_seq_to_csv)
# Filename is created internally by function, default: "/csv_data.txt"
# The reason for this is because the function must check if header is passed or not.
# If a header is passed (from sequence) a csv_header.txt file and a csv_data.txt
# file are both created within the directory, which path is given as parameter.
# Otherwise there would be a conflict between path as directory name or as filename


# ----- MAKE FRAMES -----
if frame_sequence[0]["type"] == "header":
    print("Number of frames to generate:", frame_sequence[0]["num_frames"])
else:
    print("Number of frames to generate:", len(frame_sequence))

frame_generation_result = generate_frames(
                            frame_sequence=frame_sequence,    # Expecting 0
                            basis_images_dicts=img_list_dict,
                            img_size=IMG_SIZE,
                            path=FRAMEPATH,
                            img_change_freq=None,  # per x frame(s), if None, first image in list from img_list_dict is picked for all frames.
                            count=True
                            )



# ----- MAKE ANIMATION -----
FRAMERATE = get_framerate_from_header(frame_sequence, default=30)  # if no header, then 30
N_DIGITS = get_n_digits_from_header(frame_sequence, default=6)      # if no header, then 6

#frame_generation_result = 1

if frame_generation_result == 0:         # if generating frames were succesful
    print("\nExited with code {}".format(frame_generation_result))
    print("\nContinuing with rendering video\n")

    make_animation_result = make_animation(        # Expecting it to return 0
                export_path=VIDEOPATH,
                framepath=FRAMEPATH,
                framerate=FRAMERATE,
                img_size=IMG_SIZE,
                n_digits=N_DIGITS,
                timestamp=timestamp)

    if make_animation_result == 0:
        print("\nProcess successfully finished!\n")
    else:
        print("\nProcess exited with unexpected result\n")
else:
    print("\nProgram did not exit as expected\n")




# ----- PRINTING -----
"""
for i in abs_seq:
    print(i)
print("\n")
for i in frame_sequence:
    print(i)

# Check content of image lists:
for i in img_list_dict:
    #print(img_list_dict[i])
    for x in img_list_dict[i]["list"]:
        x.show()
"""
