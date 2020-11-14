# Script to list all filenames in a directory and pipe them to a txt-file.
# Overwrites the "filenames.txt" every time it is run.

from subprocess import Popen, PIPE
from shlex import split

def write_filenames_file(path, file_format="mkv", project_path):
    """ This function writes all the filenames in directory to filenames.txt-file
    which is created in the same directory. The txt-file is overwritten for each run.
    This text-file is needed for ffmpegs concat function.
    For safety the function compares given path to project_path, to avoid
    executing system commands in other directories than in the project directory.
    Args: path (to the directory in which names of the files will be written to a text-file),
    project_path (given by default)
    file_format: a video format (ex. 'mov', 'mp4', 'mkv' etc.)
    """
    assert (project_path in path), "Given path and project_path not matching. Interrupting program"

    p1 = Popen(split("ls"), stdout=PIPE, cwd=path)

    output = p1.communicate()[0]
    output = output.decode('ascii').split()

    with open(path + "/filenames.txt", "w") as f:
        for i in output:
            if i not in "filenames.txt" and file_format in i:
                string = "file '{}'".format(str(i))
                f.write(string + "\n")

    return 0



# ----- TESTING -----
if __name__ == '__main__':
    # TODO: GET PROPER PATH
    path = "flimmering/tmp/video/"
    file_format = "mkv"
    write_filenames_file(path, file_format=file_format)
