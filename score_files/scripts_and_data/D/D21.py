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
EXPORT_FILENAME = "039"

N_EVENTS = 25

MIN_VAL = x1
MUL_SET = mul_set1
MUL_SET_IDX = 0     # If static duration, which multiplier from mul_set to select

COLOR = None
SHAPE = None

ELEM_MINSIZE = 0.95
ELEM_MAXSIZE = 1.35
N = 7      # Number of images for each shape/color combination.
IMG_CHANGE_FREQ = 1
AMP = 0.12

MAPPING_KEY = "color"    # For audio configuration in SC-script


COLOR_TRANSFORMATION = [ # Overwriting default colors assignements with new colors (for the same symbols, "r", "g", "b")
("r", (205,92,92)),      # indianred
#("g", (143,188,143)),   # darkseagreen
("g", (138,188,134)),    # custom darkseagreen
("b", (71,128,182))      # steelblue
]


# ----- MAKING DATA SEQUENCES -----

color_original_seq = []
shape_original_seq = []

for i in range(N_EVENTS):
    idx = random.randint(0, 2)
    color_original_seq.append(["r", "g", "b"][idx])

for i in range(N_EVENTS):
    idx = random.randint(0, 2)
    shape_original_seq.append(["CIRCLE", "TRIANGLE", "RECTANGLE"][idx])


# -- Making sequence of color values and shapes --
color_seq = insert_every_second_black_frame(color_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row
shape_seq = insert_every_second_black_frame(shape_original_seq, insert_at_start=False, insert_at_end=True) # Inserting a "black" for every value in color_row

# -- Durations --
base_durations = [MIN_VAL * i for i in MUL_SET]
duration_seq = []
for i in range(len(color_seq)):
    idx = random.randint(0, 5)
    duration_seq.append(base_durations[idx])


print(color_seq)
print(shape_seq)
print(duration_seq)
print(sum(duration_seq))