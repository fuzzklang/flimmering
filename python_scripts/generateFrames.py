# GENERATE FRAMES
# The functions here should be able to take an input list of dictionaries
# Shall output frames based on frame_sequence and list of base images

#import PIL
import random
from makeBaseImages import get_img_list_dict
from misc import get_colors_list
from misc import get_shapes_list

def generate_frames(frame_sequence, basis_images_dicts, img_size, path, img_change_freq=1, framerate=30, count=False, img_idx=0):
    """This function should generate all frames from frame_sequence and
    from basis_images.

    img_change_freq: how many frames per change of image.
    Can be given as None. If so, img_idx (default: 0) is assumed, and this
    image_list[img_idx] is used for all frames.
    """
    # Checking if header dictionary in sequence or not
    if frame_sequence[0]["type"] == "header":
        framerate = frame_sequence[0]["framerate"]
        n_digits = frame_sequence[0]["num_frames"]
        n_digits = len(str(n_digits))
        start = 1
        if frame_sequence[0]["num_frames"] < 200:
            count_step = 10
        elif frame_sequence[0]["num_frames"] < 500:
            count_step = 50
        else:
            count_step = 100
    else:
        n_digits = 6    # Number of digits for frame files.
        start = 0
        count_step = 100

    # Update frequency of image change, modulable?
    # img_name will only work as identifier.
    # This function handles both shape/color frames and text-frames.
    for frame_dict in frame_sequence[start:]:
        frame_num = frame_dict['frame_num']
        if 'color' in frame_dict and 'shape' in frame_dict:
            if frame_dict['color'] == None and frame_dict['shape'] == None:   # Empty frame, special handling.
                img_name = None
            else:
                frame_color = frame_dict['color']
                frame_shape = frame_dict['shape']
                # Defining name, also making sure that last part is upper case
                # i.e triangleR --> red triangle dictionary.
                img_name = str(frame_shape).lower() + str(frame_color).upper()
        elif 'text' in frame_dict:
            if frame_dict['text'] == None:  # Special handling for empty frames. If breakage remove this line.
                img_name = None
            else:
                img_name = str(frame_dict['text'])


        # Support for no flimmering. If None is given, an img_idx is assumed, default 0.
        if img_change_freq == None:
            img_list = basis_images_dicts[img_name]["list"]
            img = img_list[img_idx]
        else:
            if frame_num % img_change_freq == 0:
                img_list = basis_images_dicts[img_name]["list"]
                random_idx = random.randint(0, len(img_list) - 1)
                img = img_list[random_idx]


        if count == True and frame_num % count_step == 0:
            print("At frame number", frame_num)
        img.save(path + "/{:0{n_digits}d}.png".format(frame_num, n_digits=n_digits))

    return 0
