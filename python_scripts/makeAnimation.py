# FUNCTIONS to make animation film with ffmpeg
# Takes these arguments:

import subprocess

def make_animation(export_path, framepath, framerate, img_size, n_digits, filename):
    """
    Uses ffmpeg to make animation video.
    Takes the arguments
    export_path (output folder for video),
    framerate,
    framepath (where to find images to make animation from)
    img_size (tuple, of min and maxsize),
    n_digits (for number of digits in img-files names),
    filename
    """

    # For safety, removing leading and trailing "/" and adding them instead here in function
    filename = filename.strip("/")

    subprocess.call([
    "ffmpeg", "-framerate", "{}".format(framerate),
    "-f", "image2",
    "-s", "{}x{}".format(img_size[0], img_size[1]),
    "-i", "{}/%0{}d.png".format(framepath, n_digits),

    "-vcodec", "libx265",
    "-pix_fmt", "yuv444p",
    "-framerate", "{}".format(framerate),
    "-crf", "2",
    "{}.mkv".format(export_path + "/" + str(filename))])

    # ORIGINAL SETTINGS
    #subprocess.call([
    #"ffmpeg", "-r", "{}".format(framerate),
    #"-f", "image2",
    #"-s", "{}x{}".format(img_size[0], img_size[1]),
    #"-i", "{}/%0{}d.png".format(framepath, n_digits),
    #"-vcodec", "libx264",
    #"-pix_fmt", "yuv420p",
    #"{}.mp4".format(export_path + str(filename))])

    return 0





# ----- TESTING ------
# Only running if main.

if __name__ == '__main__':
    import datetime
    now = datetime.datetime.now()
    FILENAME = "{}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)

    # TODO: GET PROPER PATH!
    DIRECTORY = "flimmering"
    #EXPORT_PATH = DIRECTORY + "/video/TEST-VIDEOS/"
    #FRAMEPATH = DIRECTORY + "/frames/TEST-FRAMES/"
    FRAMEPATH = DIRECTORY + "/frames/videoframes/2018-03-24_16-53-39"
    EXPORT_PATH = DIRECTORY + "/video"
    FRAMERATE = 30
    IMG_SIZE = (1920, 1080)
    N_DIGITS = 4


    make_animation(
            export_path=EXPORT_PATH,
            framepath=FRAMEPATH,
            framerate=FRAMERATE,
            img_size=IMG_SIZE,
            n_digits=N_DIGITS,
            filename=FILENAME
            )



# Other configuration originally from main.py
#ffmpeg -r 60 -f image2 -s 1920x1080 -i pic%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4
