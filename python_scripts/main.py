from ratioConstr import get_ratios
from ratioConstr import get_averages
from ratioConstr import make_union

from multiples import get_multiples
from multiples import get_multiples_list

from generateAbsSeq import generate_abs_seq
from generateAbsSeq import get_total_duration

from renderToFrameSeq import render_frame_sequence

from makeBaseImages import get_img_list_dict

from misc import print_dict
from misc import print_seq
from misc import flatten_1st_depth_list
from misc import flatten_n_depth_list
from misc import get_colors_list
from misc import get_shapes_list
from misc import insert_every_second_black_frame
from misc import get_framerate_from_header
from misc import get_n_digits_from_header
from misc import check_and_adjust_list_length
from misc import lin_interpol
from misc import exp_interpol

from csvFunctions import write_from_seq_to_csv
from csvFunctions import simple_write_csv
from csvFunctions import read_csv

from changeScdData import change_scd_data
from runSCfromPy import run_sc_script
from writeFilenameList import write_filenames_file

from generateFrames import generate_frames
from makeAnimation import make_animation

import json
import pprint
import random

import datetime
import os
import sys
import time

# ---------- GLOBAL VARIABLES AND PATHS ----------
now = datetime.datetime.now()
timestamp = "{}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
IMG_SIZE = (1920, 1080) # default size of video image
#IMG_SIZE = (640, 480)
FRAMERATE = 30           # framerate for video

# Project directory
# Change this according to your homefolder.
# All subfolders will be created within this directory.


DIRECTORY = os.getcwd()

FRAMEPATH = DIRECTORY + "/frames/videoframes" + "/" + timestamp        # Creates subfolder for current run in /frames
VIDEOPATH = DIRECTORY + "/video"                   # Export folder for video
CSV_PATH = DIRECTORY + "/csv_export_data" + "/" + timestamp    # Export directory for csv-files
#JSON_PATH = DIRECTORY + "/json_data"               # Currently unused
#TMP = DIRECTORY + "/tmp"                            # tmp directory for testing etc

# TEMPORARY FOLDER:
#FRAMEPATH = TMP + "/frames/videoframes" + "/" + timestamp
#VIDEOPATH = TMP + "/video"
#CSV_PATH = TMP + "/csv_export_data" + "/" + timestamp

#FRAMEPATH = DIRECTORY + "/frames/SC-TEST"
#CSV_PATH = DIRECTORY + "/csv_export_data/SC-TEST"


# TEMPORARY FOR CREATING TEST FRAMES
#FRAMEPATH = DIRECTORY + "/frames/TEST-FRAMES"
#CSV_PATH = DIRECTORY + "/csv_export_data/TEST-DATA" + "/" + timestamp
#VIDEOPATH = DIRECTORY + "/video/TEST-VIDEOS"


# MAKE NEEDED DIRECTORIES IF NOT EXISTING
if not os.path.exists(FRAMEPATH):
    os.makedirs(FRAMEPATH)

if not os.path.exists(CSV_PATH):
    os.makedirs(CSV_PATH)



# ––––– STATIC VARIABLES –––––
#   NEEDED FOR EVERY PART

# Root ratios
r0 = 2/1
r1 = 3/2
r2 = 4/3
r3 = 5/4
r4 = 6/5
ratios = [r0, r1, r2, r3, r4]

# Minimum durations
x0 = 1/30
x1 = x0 * r0
x2 = x1 * r1
x3 = x2 * r2
x4 = x3 * r3
x5 = x4 * r4

# Multiplication arrays/sets
n = 6   # Length of each array
mul_set0 = [r0 ** i for i in range(n)]
mul_set1 = [r1 ** i for i in range(n)]
mul_set2 = [r2 ** i for i in range(n)]
mul_set3 = [r3 ** i for i in range(n)]
mul_set4 = [r4 ** i for i in range(n)]





# -------------------- INSERT HERE --------------------
# ---------- DATA DECLARATIONS ----------
# ---------- (WRITING "SCORE") ----------






# ––––– SCORE –––––
#
# PART 1
#
# First part, regular rhythm, one color (Red), one shape (circle)

# MAIN PARAMETERS TO CONTROL:
N_EVENTS = 14
IMG_CHANGE_FREQ = 1
ELEM_MINSIZE = 0.2
ELEM_MAXSIZE = 0.25
N = 7      # Number of images for each shape/color combination.
EXPORT_FILENAME = "000"
AMP = 0.25
MAPPING_KEY = "color"

MIN_VAL = x3
MUL_SET = mul_set1
MUL_SET_IDX = 3     # If static duration, which multiplier from mul_set to select

COLOR = "R"
SHAPE = "CIRCLE"


COLOR_TRANSFORMATION = [ # Overwriting default colors assignements with new colors (for the same symbols, "r", "g", "b")
("r", (205,92,92)),      # indianred
#("g", (143,188,143)),   # darkseagreen
("g", (138,188,134)),    # custom darkseagreen
("b", (71,128,182))      # steelblue
]


# ----- MAKING DATA SEQUENCES -----

color_original_seq = [COLOR]

for i in range(N_EVENTS):
    color_original_seq.append(COLOR)

shape_original_seq = [SHAPE for i in range(len(color_original_seq))]

# -- Making sequence of color values and shapes --
color_seq = insert_every_second_black_frame(color_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row
shape_seq = insert_every_second_black_frame(shape_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row


# -- Durations --

# Set 1 multiplied with minimum value 3
root_durations = [MIN_VAL * i for i in MUL_SET]

duration_seq = [root_durations[MUL_SET_IDX] for i in range(len(color_seq))]




















# -------------------- END INSERT --------------------





# Checking that durations and color lists are of equal length,
# and adjusting thereafter (adjusted list compared to reference list)
assert len(color_seq) == len(duration_seq), "Length of color_seq and duration_seq is not equal. Interrupting."
#duration_seq = check_and_adjust_list_length(ref_list=color_seq, adj_list=duration_seq)    # Returns the adjusted list


# -- Making sequences of dictionaries with all data --
abs_sequence = generate_abs_seq(duration_seq=duration_seq, color_seq=color_seq, shapes=shape_seq, header_framerate=FRAMERATE)
frame_sequence = render_frame_sequence(abs_sequence, framerate=FRAMERATE, header=True)





# ----- MAKING BASIS IMAGES -------
colors = get_colors_list(frame_sequence)    # list of all colors present in frame_sequence
shapes = get_shapes_list(frame_sequence)    # list of all shapes present in frame_sequence


img_list_dict = get_img_list_dict(
                            n=N,            # Number of imgs of each colors
                            minsize=ELEM_MINSIZE,    # Minsize as multiple of image img_size. GLOBAL variable here in script
                            maxsize=ELEM_MAXSIZE,    # Maxsize as multiple of image img_size. GLOBAL variable here in script
                            colors=colors,  # List of which colors that needs to be generated
                            shapes=shapes,  # List of which shapes that needs to be generated
                            img_size=IMG_SIZE,  # Tuple of image_size
                            color_symbol_transform=COLOR_TRANSFORMATION # Transforming a symbol to other RGB-values than specified by default
                            )




# ----- WRITE TO CSV FILE -----
write_from_seq_to_csv(directory_path=CSV_PATH, sequence=abs_sequence, csv_header_order=None, export_filename=EXPORT_FILENAME)
# CSV-directory is created from 'now'-variable and specific for each run (in write_from_seq_to_csv)
# Filename is created internally by function, default: "/csv_data.txt"
# The reason for this is because the function must check if header is passed or not.
# If a header is passed (from sequence) a csv_header.txt file and a csv_data.txt
# file are both created within the directory, which path is given as parameter.
# Otherwise there would be a conflict between path as directory name or as filename


# change_scd_data(timestamp=timestamp, name=EXPORT_FILENAME, amp=AMP, mapping=MAPPING_KEY, filepath=DIRECTORY + "/score_files/run_data")  # Needs only directory path for filepath! # FOR DEBUG




# ----- GENERATING FRAMES -----
# Running generate_frames function, expecting 0 returned

if frame_sequence[0]["type"] == "header":
    print("Number of frames to generate:", frame_sequence[0]["num_frames"])
else:
    print("Number of frames to generate:", len(frame_sequence))

frame_generation_result = generate_frames(
                            frame_sequence=frame_sequence,    # Expecting 0
                            basis_images_dicts=img_list_dict,
                            img_size=IMG_SIZE,
                            path=FRAMEPATH,
                            img_change_freq=IMG_CHANGE_FREQ,  # per x frame(s), global variable here in script
                            count=True
                            )



# ----- MAKE VIDEO -----
# Check for header
# If header, get framerate and number of digits for filenames from it
# If not, set manually (for now specified to 30 and 6)
FRAMERATE = get_framerate_from_header(frame_sequence, default=30)  # if no header, then 30
N_DIGITS = get_n_digits_from_header(frame_sequence, default=6)      # if no header, then 6


if frame_generation_result == 0:         # if generating frames were succesful
    print("\nExited with code {}".format(frame_generation_result))
    print("\nContinuing with rendering video\n")

    make_animation_result = make_animation(        # Expecting it to return 0
                export_path=VIDEOPATH,
                framepath=FRAMEPATH,
                framerate=FRAMERATE,
                img_size=IMG_SIZE,
                n_digits=N_DIGITS,
                filename=EXPORT_FILENAME)

    if make_animation_result == 0:
        print("\nProcess successfully finished!\n Continuing with generating audio")
        # Updating metadata for sclang run:
        # Takes timestamp, name of audio export file, amp level (0.0 - 1.0),
        # mapping ('shape' or 'color') and an export path.
        change_scd_data(timestamp=timestamp, name=EXPORT_FILENAME, amp=AMP, mapping=MAPPING_KEY, filepath=DIRECTORY + "/score_files/run_data")  # Needs only directory path for filepath!
        time.sleep(0.05)
        # Running sclang
        run_sc_script(script= DIRECTORY + "/sc-files/exportAudio.scd")

    else:
        print("\nProcess exited with unexpected result\n")
else:
    print("\nProgram did not exit as expected\n")


# Create overview file for ffmpeg concat (txt-file containing all files names
# of videos to be concatenated)




# OLD STUFF
# for later, if needed
"""
# Would rather, in some way or another import this from some file
# Not that relevant for this script

ratios_a = get_ratios(12, symbolic=False)
ratios_b = get_averages(ratios_a)
ratios_c = get_averages(ratios_b)
ratios = {
    "a" : ratios_a,
    "b" : ratios_b,
    "c" : ratios_c
    }
union = make_union(ratios)
union = make_union([ratios_a, ratios_b, ratios_c])
union = make_union([ratios_a])

#data = get_multiples_list(union, 2)
"""
