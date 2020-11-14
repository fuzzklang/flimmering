# Make text base frames. Will be used in FrameGeneration

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# NEEDED???
def assign_center_pos(tup, img_size):
    """
    Takes a tuple of two values, width and height, and returns a tuple of x and
    y positions, adjusted so that the object is centered according to
    image_size. Thus needs global img_size tuple for img_w and img_height.
    Arguments: tup, img_size
    """
    img_width, img_height = img_size[0], img_size[1]
    t_width, t_height = tup[0], tup[1]

    pos_x = (img_width-t_width)/2	# Center position x-axis
    pos_y = (img_height-t_height)/2	# Center position y-axis

    return (pos_x, pos_y)


def get_empty_img(img_size, background=(0,0,0)):
    """
    Returns an empty image.
    """
    img = Image.new('RGB', img_size, background)
    return img


def get_text_img(text, font, font_size, img_size, background=(0,0,0), center_text=True, xy=None):
    """
    Returns an image with text.
    Takes a text (string), font, font_size, img_size as required arguments.
    If center_img is True text gets centered. If xy is given (not None) it gets
    priority over center_img. (makes center_text argument kinda redundant, but
    at least it's easier to read and understand what's going on with it still
    there)
    If is given, it is a tuple giving the position of the top left corner of
    the text obj.

    Args:
    xy: coordinates for text elem.
    text: text, a string, being drawn to image.
    background: color of background (default: black)
    img_size: the size of the image.
    center_img: whether or not to center text (default: True).
    xy: position of text elem (default: None)
    """

    img = Image.new('RGB', img_size, background)
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(font, font_size)

    # Return empty/black image if given as text element
    #if text.lower() == "none" or text.lower() == "black":  # Decomment if breakage
    #    return img

    if xy:
        pos=xy
    else:
        obj_size = draw.textsize(text, fnt)
        pos = assign_center_pos(obj_size, img_size)
    # (xy, text, fill=None, font=None, anchor=None, spacing=0, align="left", direction=None, features=None)

    draw.multiline_text(
                        xy=pos,
                        text=text,
                        fill=None,
                        font=fnt,
                        spacing=font_size/2,    # This can be freely adjusted and experimented with
                        align="center"
                        )
    return img


def get_text_img_list_dict(n, minsize_mul, maxsize_mul, text_elems, img_size, font, font_size):
    """
    Returns a dictionary of dictionaries, each containing a list of image(s)
    with text written on them, in addition to metadata about the images.

    Arguments:
    n: specifies number of images of each color/shape combination
    minsize_mul: minimum size of font (multiple of font_size)
    maxsize_mul: maximum size of font (multiple of font_size)
    text_elems: list of all strings there needs to be maken base images for.
    img_size:
    font:
    font_size:

    output format: {
        dictionary_key1 : { "text" : "string1", list : [img1, ... img_n]},
        dictionary_key2 : { "text" : "string2", list : [img1, ... img_n]},
        ...,
        dictionary_key_n: { "text" : "string_n", list : [img1, ... img_n]},
        }
    """
    assert n > 0, "n must be greather than zero. In function 'get_text_img_list_dict'"

    output = {}

    if n == 1:      # To avoid ZeroDivision below + get correct min and max sizes of shapes.
        steps = 2   # (Not sure about this variable name...)
    else:
        steps = n

    for text in text_elems:

        text = text
        current_dict = {}
        dictionary_key = text
        current_dict["text"] = text
        current_dict["list"] = []

        if text == None:                # Special handling for None/Empty frames
            empty_img = get_empty_img(img_size=img_size)
            current_dict["list"].append(empty_img)
        else:
            for i in range(n):
                current_size_mul = (((maxsize_mul - minsize_mul) / (steps - 1)) * i) + minsize_mul  # (steps - 1) to make sure images start at minsize and end at maxsize.

                # args: (xy, text, font, font_size, img_size, background=(0,0,0))
                # xy should be given, and recalculated in get_text_img function so that
                # it corresponds to center of object.
                #x = img_size[0] / 2
                #y = img_size[1] / 2
                adj_font_size = int(round(font_size * current_size_mul))    # adj font_size for current img, according to multiplier

                text_img = get_text_img(text, font, adj_font_size, img_size)    # getting img.
                current_dict["list"].append(text_img)   # adding img to current_dictionary["list"]


        output[dictionary_key] = current_dict   # Adding current dictionary to main dictionary.

    return output




# ---------- TESTING ----------
"""

IMG_SIZE = (640, 480)
#IMG_SIZE = (120, 120)
FONT = '/System/Library/Fonts/Menlo.ttc'
FONT_SIZE = 120

#t = ['A', 'BB', 'CCC', 'a\nc', '\nv']
t = ['A longer text \nwith newlines\nlet\'s test this', "BBBB"]

g = get_text_img_list_dict(
                    n=3,
                    minsize_mul=0.5,
                    maxsize_mul=2,
                    text_elems=t,
                    img_size=IMG_SIZE,
                    font=FONT,
                    font_size=FONT_SIZE
                    )

#print(g)
for i in g:
    print(repr(i), g[i])

#g[t[0]]["list"][0].show()
#g["A"]["list"][1].show()
for d in g:
    for i in g[d]["list"]:
        i.show()
        #pass
"""
