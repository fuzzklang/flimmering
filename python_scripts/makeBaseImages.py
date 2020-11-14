# Function to make baseImages. Will be used in FrameGeneration

from PIL import Image
from PIL import ImageDraw


# Figures:
# Square, Circle, Triangle

# Size of figures
# Random size

# How many of each? (n)

def center_shape(shape_coords, img_size):
    """ Centers a rect or ellipse based on (usually) four coordinates.
    shape_coords must be in format [x0, y0, x1, y1]
    """
    img_w = img_size[0]
    img_h = img_size[1]
    shape_w = shape_coords[2] - shape_coords[0]
    shape_h = shape_coords[3] - shape_coords[1]
    pos_x0 = int((img_w / 2) - (shape_w / 2))    # Centering x-axis
    pos_y0 = int((img_h / 2) - (shape_h / 2))    # Centering y-axis
    pos_x1 = pos_x0 + shape_w
    pos_y1 = pos_y0 + shape_h
    return [pos_x0, pos_y0, pos_x1, pos_y1]


def get_size_from_mult(mult, img_size):
    """ Returns an array of [x0, y0, x1, y1] coordinates
    for a shape. It calculates size of the to last values based on
    a multiple of img_size. This multiple ("mult") is in range 0-1
    (0 to covering the whole image), but can also be bigger.
    """
    w = img_size[0]
    h = img_size[1]
    x = w * mult
    y = h * mult
    return [0, 0, x, y]


def get_circle_size_from_mult(mult, img_size):
    """ Returns an array of [x0, y0, x1, y1] coordinates
    for a circle shape. It calculates size of radius based on
    a multiple of img_w. This multiple ("mult") is in range 0-1
    (0 to covering the whole image), but can also be bigger.
    """
    w = img_size[0]
    h = img_size[1]
    y = h * mult
    x = y
    return [0, 0, x, y]


# Old version of triangle
#def get_triangle_size_from_mult(mult, img_size):
#    """Find a way to calculate position for a triangle.
#    """
#    img_w, img_h = img_size[0], img_size[1]
#    side_length = img_h * mult
#    pos1 = (int(img_w / 2), int((img_h / 2) - (side_length / 2)))  # Center pos
#    pos2 = (int(img_w / 2 - side_length / 2), int(pos1[1] + side_length))
#    pos3 = (int(img_w / 2 + side_length / 2), int(pos1[1] + side_length))
#    return [pos1, pos2, pos3]


def get_triangle_size_from_mult(mult, img_size):
    """Find a way to calculate position for a triangle.
    """
    img_w, img_h = img_size[0], img_size[1]
    side_length = img_h * mult           # Where sidelength is hypotenuse
    cathetus = ((side_length ** 2) - ((side_length / 2) ** 2)) ** (1/2)   # Pythagoras

    pos1 = (int(img_w / 2), int((img_h / 2) - (cathetus * (2 / 3))))    # Center pos
    pos2 = (int((img_w / 2) - (side_length / 2)), int(pos1[1] + cathetus))
    pos3 = (int((img_w / 2) + (side_length / 2)), int(pos1[1] + cathetus))
    return [pos1, pos2, pos3]


def get_img(xy, shape, color, img_size, background=(0,0,0)):
    """Returns an image.
    Takes coordinates (xy) and a string specifying which shape
    to return.
    In other words must the format of the xy correspond to the
    type of shape.
    Args:
    xy: coordinates for shape.
    shape: specifying type of shape.
    color: color of shape.
    background: color of background (default: black)
    img_size: the size of the image.
    """
    img = Image.new('RGB', img_size, background)
    draw = ImageDraw.Draw(img)

    if shape != None:
        shape = shape.lower()   # Compatible with strings with upper case letters.

    if shape == "rectangle":
        draw.rectangle(xy, color, color)
    elif shape == "triangle":
        draw.polygon(xy, color, color)
    elif shape == "circle":
        draw.ellipse(xy, color, color)
    elif shape == "black" or shape == None:
        pass    # Returns just the black image if shape = "black" or None.
    else:
        raise ValueError("Function 'get_img' has received a non-valid shape name")

    return img


def get_img_list_dict(n, minsize, maxsize, colors, shapes, img_size, color_symbol_transform=None):
    """ Uses get_img to make a dictionary of dictionaries. Each dictionary contains
    information about the images in the dictionary and a list of the images.

    This function creates a dict of each combination of color and shape with the
    specified other parameters. Top dictionary keys are the names of the dictionaries.
    For instance will parameters 'shapes' = ["triangle", "rectangle", None] and
    'colors' = ["R", "G"] make a list of four dictionaries, each containing
    the color and shape combinations of 'shapes' and 'colors'.
    Also supports transformation of colors, so that color_symbols (i.e "G") will
        be interpreted as the new tuple assigned to that symbol.
    Format will be:
        {
        'triangleR' : {'color':'R', 'shape':'triangle', 'list':[...list of images...]},
        'triangleG': {'color':'G', 'shape':'triangle', 'list':[...list of images...]},
        'rectangleR' : {'color':'R', 'shape':'rectangle', 'list':[...list of images...]},
        'rectangleG' : {'color':'G', 'shape':'rectangle', 'list':[...list of images...]}
        'black' : {'color' : None, 'shape' : None, 'list' : [... black image ...]}
        }

    Arguments:
    n: specifies number of images of each color/shape combination
    min: minimum size of these shapes (multiple of img_size)
    max: maximum size of these shapes (multiple of img_size)
    colors: list of colors (strings or tuples) or just a tuple or a string.
    shapes: list of strings or just a string specifying which kind of shape.
    color_symbol_transform: list of tuple, each containing symbol (e.g "r") and new tuple of RGB-values
    """

    def get_color_tuple(x):
        if type(x) == type(tuple()):
            return x    # Assume it is already a valid RGB-tuple
        else:
            colors = {
                'r' : (255,0,0),
                'g' : (0,255,0),
                'b' : (0,0,255),
                'black' : (0,0,0),
                'none' : (0,0,0)
            }

            if color_symbol_transform:              # Color symbol transform.
                for tup in color_symbol_transform:
                    key = tup[0]
                    new_color = tup[1]
                    colors[key.lower()] = new_color
            x = x.lower()
            if x not in colors:
                raise ValueError("Color name given to function 'get_color_tuple is not a valid name'")

            return colors[x]


    if type(colors) != type(list()):
        colors = [colors]
    if type(shapes) != type(list()):
        shapes = [colors]

    add_black = False
    output = {}

    # Dependency on other functions in script.
    # Changes the function according to the given shape.
    # They all take the same number of arguments (mult, img_size)
    shape_funcs = {
    'triangle' : get_triangle_size_from_mult,
    'rectangle' : get_size_from_mult,
    'circle' : get_circle_size_from_mult,
    'ellipse' : get_size_from_mult,
    }

    for shape in shapes:
        # If shape = black or None set add_black-flag to True
        # and continue with next shape.
        if shape == None or shape.lower() == 'black' or shape.lower() == "none":
            add_black = True
            continue

        make_shape_func = shape_funcs[shape.lower()]       # dictionary of functions making different shapes

        for color in colors:
            # Iterating over each color for each shape.

            # If color = black or None set add_black-flag to True
            # and continue with next color.

            if type(color) != type(tuple()):
                if color == None or color.lower() == "black":
                    add_black = True
                    continue

            current_dict = {'shape' : shape, 'color' : color, 'list':[]}

            for i in range(n):
                # Making list of images.
                if n == 1:      # To avoid ZeroDivision below + get correct min and max sizes of shapes.
                    steps = 2   # (Not sure about this variable name...)
                else:
                    steps = n

                current_size = (((maxsize - minsize) / (steps - 1)) * i) + minsize  # (steps - 1) to make sure images start at minsize and end at maxsize.
                xy = make_shape_func(current_size, img_size)       # Gets coordinates from function (which is changed according to which shape is being made)
                if shape.lower() in ['circle', 'ellipse', 'rectangle']: # shapes in this list must be centered
                    xy = center_shape(xy, img_size)
                color_tuple = get_color_tuple(color)    # Converts color name to tuple
                img = get_img(xy=xy, shape=shape, color=color_tuple, img_size=img_size)
                current_dict['list'].append(img)

            # Adding to output dictionary where name (the dictionary key)
            # is a combination of shape and color.
            # i.e 'triangleB' or 'noneBLACK' or 'rectangle(178,255,100)'
            output[str(shape.lower()) + str(color).upper()] = current_dict


    # Add an empty/black image
    if add_black == True:
        empty_img = get_img(xy=(0,0,0,0), shape=None, color=(0,0,0), img_size=img_size)
        #empty_img_dict = {'shape':None, 'color':'black', 'list':[empty_img]}   # Decomment if breakage
        empty_img_dict = {'shape':None, 'color':None, 'list':[empty_img]}
        output[None] = empty_img_dict

    return output



# TEST THE FUNCTIONS
"""
shapes = [None, 'triangle', 'circle', 'rectangle']
colors = ['black', "R", "G", "B"]
#shapes = ['rectangle', 'circle']
#colors = ["r"]

img_dict_list = get_img_list_dict(1, 0.2, 0.7, colors, shapes, IMG_SIZE)


frame_num = 0

for i in img_dict_list:
    #name = str(str(i['shape']) + str(i['color']))
    name = 'img'
    for img in i['list']:
        #img.save(PATH + "/{0}{1:05d}.png".format(name, frame_num))
        frame_num += 1

for i in img_dict_list:
    print(i['color'])
    print(i['shape'])
    print(i['list'])

#print(img_dict_list)

pos1 = get_triangle_size_from_mult(mult=0.1, img_size=[1280, 800])
pos2 = get_circle_size_from_mult(mult=0.1, img_size=[1280, 800])
pos2 = center_shape(shape_coords=pos2, img_size=[1280, 800])
img1 = get_img(xy=pos1, shape="triangle", color=(255,0,0), img_size=[1280,800], background=(0,0,0))
img2 = get_img(xy=pos2, shape="circle", color=(255,0,0), img_size=[1280,800], background=(0,0,0))
img1.show()
img2.show()

"""
