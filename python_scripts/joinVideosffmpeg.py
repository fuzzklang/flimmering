# Join video files
#
# Script to join several videofiles which are placed in the same directory
# Files must be in same directory and consistently named.

import subprocess
from writeFilenameList import write_filenames_file
import datetime
import sys
import os

DIRECTORY = os.getcwd()
DIRECTORY = DIRECTORY + "/score_files/merged_audio_video"
VIDEOPATH = DIRECTORY + "/export"                   # Export folder for video
#TMP = DIRECTORY + "/tmp"                            # tmp directory for testing etc
FILE_FORMAT = "mkv"

print("\n\nDIRECTORY:\n", DIRECTORY, "\n\n")

now = datetime.datetime.now()
timestamp = "{}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)


def concat_videos(directory, output_file_format, output_name="output"):
    cmd= [
    "ffmpeg", "-f", "concat", "-safe", "1",
    "-i", "{}/filenames.txt".format(directory),
    "-c", "copy",
    "./export/{}.{}".format(output_name, output_file_format)
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=directory)
    process.communicate()
    process.wait()
    exit_code = process.returncode
    return exit_code


write_filenames_result = write_filenames_file(DIRECTORY, file_format=FILE_FORMAT, project_path="/shit_going_on/flimmering")


if write_filenames_result == 0:
    print("Succesful file list creation.\nContinuing with concatenating videos in given directory")
    exit_code = concat_videos(DIRECTORY, output_name=timestamp, output_file_format=FILE_FORMAT)
    print("ffmpeg exited with exit code", exit_code)
