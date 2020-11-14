# IMPORTS FOR EVERY PART
from misc import insert_every_second_black_frame
from misc import lin_interpol

import random


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




# ––––– SCORE –––––


# MAIN PARAMETERS TO CONTROL:
N_EVENTS = None     # Sequence based
IMG_CHANGE_FREQ = 1
ELEM_MINSIZE = 0.3
ELEM_MAXSIZE = 0.35
N = 7      # Number of images for each shape/color combination.
EXPORT_FILENAME = "012"
AMP = 0.25
MAPPING_KEY = "None"

MIN_VAL = x5
MUL_SET = mul_set1
MUL_SET_IDX = None

COLOR = None
SHAPE = "CIRCLE"


COLOR_TRANSFORMATION = [ # Overwriting default colors assignements with new colors (for the same symbols, "r", "g", "b")
("r", (205,92,92)),      # indianred
#("g", (143,188,143)),   # darkseagreen
("g", (138,188,134)),    # custom darkseagreen
("b", (71,128,182))      # steelblue
]


# ----- MAKING DATA SEQUENCES -----

r, g, b = "R", "G", "B"
color_original_seq = [
    b, g, b, b, b, g, r, b, b, g,
    r, b, b, g, b, g, g, g, g, b,
    r, b, r, b, r, g, r, r, r, r
]


shape_original_seq =  [SHAPE for i in color_original_seq]

# -- Making sequence of color values and shapes --
color_seq = insert_every_second_black_frame(color_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row
shape_seq = insert_every_second_black_frame(shape_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row

# -- Durations --
base_durations = [MIN_VAL * i for i in MUL_SET]
#duration_seq = [root_durations[MUL_SET_IDX] for i in range(len(color_seq))]

duration_seq = []
duration_idxes = [int(lin_interpol(beg=0.0, end=5.99999, steps=len(color_seq), i=i)) for i in range(len(color_seq))]
for idx in duration_idxes:
    duration_seq.append(base_durations[idx])
