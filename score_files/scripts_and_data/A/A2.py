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
# PART 1
#
# First part, regular rhythm, one color (Red), one shape (circle)

# MAIN PARAMETERS TO CONTROL:
N_EVENTS = None
IMG_CHANGE_FREQ = 1
ELEM_MINSIZE = 0.2
ELEM_MAXSIZE = 0.25
N = 7      # Number of images for each shape/color combination.
EXPORT_FILENAME = "001"
AMP = 0.25
MAPPING_KEY = "color"

MIN_VAL = x3
MUL_SET = mul_set1
MUL_SET_IDX = None     # If static duration, which multiplier from mul_set to select

COLOR = "R"
SHAPE = None


COLOR_TRANSFORMATION = [ # Overwriting default colors assignements with new colors (for the same symbols, "r", "g", "b")
("r", (205,92,92)),      # indianred
#("g", (143,188,143)),   # darkseagreen
("g", (138,188,134)),    # custom darkseagreen
("b", (71,128,182))      # steelblue
]


# ----- MAKING DATA SEQUENCES -----

c = "circle"
t = "triangle"
r = "rectangle"


shape_original_seq = [
    c, t, c, c, t,
    c, t, c, t, c,
    r, t
    ]

color_original_seq = []

for i in range(len(shape_original_seq)):
    color_original_seq.append(COLOR)

mul_set_indexes = [4, 4, 3, 4, 3, 4, 3, 4, 3, 4, 1, 4]
root_durations = [MUL_SET[idx] for idx in mul_set_indexes]
duration_seq = [i * MIN_VAL for i in root_durations]


# -- Making sequence of color values and shapes --
color_seq = insert_every_second_black_frame(color_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row
shape_seq = insert_every_second_black_frame(shape_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row


# -- Durations --

# Set 1 multiplied with minimum value 3
stuttered_list = [i for val in duration_seq for i in [val] * 2] # Stutter every value in list twice
duration_seq = stuttered_list


print(duration_seq)
print(shape_seq)
print(color_seq)
