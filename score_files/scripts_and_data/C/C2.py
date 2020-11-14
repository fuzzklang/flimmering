# IMPORTS FOR EVERY PART
from misc import insert_every_second_black_frame
from misc import lin_interpol


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
#
# Abrupt flash of big shape!
# Low audio levels

# MAIN PARAMETERS TO CONTROL:
EXPORT_FILENAME = "014"

N_EVENTS = None     # 40 defined through length of lists below

MIN_VAL = x1
MUL_SET = mul_set4
MUL_SET_IDX = None

COLOR = None
SHAPE = None

ELEM_MINSIZE = 0.2
ELEM_MAXSIZE = 0.25
N = 7      # Number of images for each shape/color combination.
IMG_CHANGE_FREQ = 1
AMP = 0.25

MAPPING_KEY = "color"    # For audio configuration in SC-script


COLOR_TRANSFORMATION = [ # Overwriting default colors assignements with new colors (for the same symbols, "r", "g", "b")
("r", (205,92,92)),      # indianred
#("g", (143,188,143)),   # darkseagreen
("g", (138,188,134)),    # custom darkseagreen
("b", (71,128,182))      # steelblue
]


# ----- MAKING DATA SEQUENCES -----

c, t, r = "circle", "triangle", "rectangle"
shape_original_seq =  [
    c, t, r, c, t, r, c, t, r, c,
    t, t, t, r, t, t, r, t, r, r,
    c, c, t, c, c, t, c, c, t, c,
    r, r, r, r, c, t, c, t, c, t,
    r, t, r, r, r, t, r, r, t, t,
    r, c, r, r, r, c, r, c, t, c,
    r, t, c, r, r, t, t, t, r, c,
    c, c, r, c, t, c, t, c, r, c

    ]

r, g, b = "R", "G", "B"
color_original_seq = [
    r, g, b, r, g, b, r, r, g, g,
    g, g, g, r, g, g, r, g, r, r,
    b, b, r, r, g, g, b, b, r, r,
    b, b, b, b, r, g, r, g, r, g,
    r, g, g, g, b, b, b, r, r, r,
    b, g, r, b, b, g, g, g, b, r,
    g, g, g, b, b, b, r, r, r, r,
    r, r, b, r, g, r, g, r, b, r,
    ]

# -- Durations --
# BIG QUESTION HERE: SHOULD COLORS BE MAPPED TO DURATIONS AS WELL, OR JUST SHAPES?
translation_table = {"circle" : MUL_SET[0], "triangle" : MUL_SET[3], "rectangle" : MUL_SET[5]}
duration_seq = [(translation_table[shape.lower()] * MIN_VAL) for shape in shape_original_seq]

# -- Making sequence of color values and shapes --
color_seq = insert_every_second_black_frame(color_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row
shape_seq = insert_every_second_black_frame(shape_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row

stuttered_list = [i for val in duration_seq for i in [val] * 2] # Stutter every value in list twice
duration_seq = stuttered_list

#print(duration_seq[-2:])
