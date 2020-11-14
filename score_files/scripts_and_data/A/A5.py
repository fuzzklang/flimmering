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
#

# MAIN PARAMETERS TO CONTROL:
N_EVENTS = 15     # Not applicable, defined through length of original_shape_seq
IMG_CHANGE_FREQ = 1
ELEM_MINSIZE = 0.2
ELEM_MAXSIZE = 0.3
N = 7      # Number of images for each shape/color combination.
EXPORT_FILENAME = "004"
AMP = 0.25
MAPPING_KEY = "color"

MIN_VAL = x2
MUL_SET = mul_set1
MUL_SET_IDX = None     # Not applicable, varied according to the shapes

COLOR = "R"
SHAPE = None    # Not applicable


COLOR_TRANSFORMATION = [ # Overwriting default colors assignements with new colors (for the same symbols, "r", "g", "b")
("r", (205,92,92)),      # indianred
#("g", (143,188,143)),   # darkseagreen
("g", (138,188,134)),    # custom darkseagreen
("b", (71,128,182))      # steelblue
]


# ----- MAKING DATA SEQUENCES -----

color_original_seq = []

#for i in range(N_EVENTS):
#    color_original_seq.append(COLOR)

c, t, r = "circle", "triangle", "rectangle"
#shape_original_seq = [SHAPE for i in range(len(color_original_seq))]

shape_original_seq =  [
    c, t, r, t, r, t, c, r, c, r,
    c, c, c, c, c]

for i in shape_original_seq:
    color_original_seq.append("r")

#translation_table = {"circle" : MUL_SET[3], "triangle" : MUL_SET[4], "rectangle" : MUL_SET[1]}
#duration_seq = [(translation_table[shape.lower()] * MIN_VAL) for shape in shape_original_seq]



# -- Making sequence of color values and shapes --
color_seq = insert_every_second_black_frame(color_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row
shape_seq = insert_every_second_black_frame(shape_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row


# -- Durations --
base_durations = [MIN_VAL * i for i in MUL_SET]
#duration_seq = [root_durations[MUL_SET_IDX] for i in range(len(color_seq))]

duration_seq = []
duration_idxes = [int(lin_interpol(beg=0.0, end=5.999999, steps=len(color_seq), i=i)) for i in range(len(color_seq))]
for idx in duration_idxes:
    duration_seq.append(base_durations[idx])
