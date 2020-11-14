# IMPORTS FOR EVERY PART
from misc import insert_every_second_black_frame
from misc import lin_interpol
from misc import exp_interpol


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
EXPORT_FILENAME = "030"

N_EVENTS = None     # 40 defined through length of lists below

MIN_VAL = None
MUL_SET = None
MUL_SET_IDX = None

COLOR = None
SHAPE = None

ELEM_MINSIZE = 0.1
ELEM_MAXSIZE = 0.15
N = 7      # Number of images for each shape/color combination.
IMG_CHANGE_FREQ = 1
AMP = 0.25

MAPPING_KEY = "color"    # For audio configuration in SC-script


# SPECIFICALLY FOR THE AUGMENTATION PART
BEG = 0.3
END = 1.1




COLOR_TRANSFORMATION = [ # Overwriting default colors assignements with new colors (for the same symbols, "r", "g", "b")
("r", (205,92,92)),      # indianred
#("g", (143,188,143)),   # darkseagreen
("g", (138,188,134)),    # custom darkseagreen
("b", (71,128,182))      # steelblue
]


# ----- MAKING DATA SEQUENCES -----
# Taken from C2, and shortened down
c, t, r = "circle", "triangle", "rectangle"
shape_original_seq =  [
    c, t, r, c, t, r, c, t, r, c,
    ]

r, g, b = "R", "G", "B"
color_original_seq = [
    r, g, b, r, g, b, r, r, g, g,
    ]


# -- Making sequence of color values and shapes --
color_seq = insert_every_second_black_frame(color_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row
shape_seq = insert_every_second_black_frame(shape_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row

N_EVENTS = len(color_seq)

duration_seq = [exp_interpol(BEG, END, N_EVENTS, i) for i in range(len(color_seq))]

# Shortening down last value, to  have a shorter pause between each part
duration_seq[-1] = BEG * 2


print(sum(duration_seq))
