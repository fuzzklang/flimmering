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


# MAIN PARAMETERS TO CONTROL:
N_EVENTS = None
IMG_CHANGE_FREQ = 1
ELEM_MINSIZE = 0.7
ELEM_MAXSIZE = 0.72
N = 5      # Number of images for each shape/color combination.
EXPORT_FILENAME = "009"
AMP = 0.25
MAPPING_KEY = "color"

MIN_VAL = x5
MUL_SET = mul_set0
MUL_SET_IDX = None

COLOR = None
SHAPE = None


COLOR_TRANSFORMATION = [ # Overwriting default colors assignements with new colors (for the same symbols, "r", "g", "b")
("r", (205,92,92)),      # indianred
#("g", (143,188,143)),   # darkseagreen
("g", (138,188,134)),    # custom darkseagreen
("b", (71,128,182))      # steelblue
]


# ----- MAKING DATA SEQUENCES -----

c, t, r = "CIRCLE", "TRIANGLE", "RECTANGLE"
shape_original_seq =  [r, t, c, t, r]

r, g, b = "R", "G", "B"
color_original_seq = [b, r, g, b, r]


# -- Durations --
translation_table = {"circle" : MUL_SET[3], "triangle" : MUL_SET[4], "rectangle" : MUL_SET[1]}
duration_seq = [(translation_table[shape.lower()] * MIN_VAL) for shape in shape_original_seq]
stuttered_list = [i for val in duration_seq for i in [val] * 2] # Stutter every value in list twice
duration_seq = stuttered_list

# -- Making sequence of color values and shapes --
color_seq = insert_every_second_black_frame(color_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row
shape_seq = insert_every_second_black_frame(shape_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row

# Manipulating last entry to have a shorter transition to next part/shorter empty frame
duration_seq[-1] = MIN_VAL * MUL_SET[0]

#print(duration_seq)
#print(len(duration_seq), len(color_seq), len(shape_seq))
