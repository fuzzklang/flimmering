# Join video and audio files
#
# Script to join several video and audio files
# Files must be in seperate directories and consistently named.
#
# Must include -shortest argument, to ensure cutting of audio files which
# possibly are longer than the video files they are combined with.

import datetime
import subprocess
import sys
import os

#FRAMERATE = 30
#IMG_SIZE = (1920, 1080)

now = datetime.datetime.now()
timestamp = "{}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
N_DIGITS = 3

DIRECTORY = os.getcwd()
DIRECTORY = DIRECTORY + "/score_files"
VIDEODIR = DIRECTORY + "/video"
AUDIODIR = DIRECTORY + "/audio"
EXPORT_DIR = DIRECTORY + "/merged_audio_video"


num_files = input("Set the number of files to merge. \nThe files must be consistently named ('000.format', '001.format' etc): ")
num_files = int(num_files)
offset = input("Set the offset index (from which number the file numbering is starting): ")
offset = int(offset)

first_file = "{:03d}.MOVFORMAT".format(offset)

confirmation = input("{} is first file, confirm with Y.\nIf wrong, write any other character ".format(first_file))

# Exit script if wrong first file number
if str(confirmation).lower() != "y":
    exit()

#assert type(num_files) == type(int()), "Input must be of type integer"

for i in range(num_files):
    filename = "{:03d}".format(i+offset)
    command = ["ffmpeg",
        "-i", "{}/{}.mkv".format(VIDEODIR, filename),
        "-i", "{}/{}.aiff".format(AUDIODIR, filename),
        "-ac", "2",
        "-vcodec", "libx265",
        "-pix_fmt", "yuv444p",
        "-crf", "2",
        "{}.mkv".format(EXPORT_DIR + "/" + str(filename))]

    subprocess.run(command)


# This command sadly not working.
# Would want to handle an arbitrary number of consistently named audio and video
# files and merge them to one video file.
command = ["ffmpeg",
    "-i", "{}/%03d.mkv".format(VIDEODIR, N_DIGITS),
    #"ac", "2",
    "-i", "{}/%03d.aiff".format(AUDIODIR, N_DIGITS),
    "{}.mkv".format(EXPORT_DIR + "/" + str(timestamp))]
