# Script to rename a sequence of files (or slices of it),
# thus pushing the idx of the sequence (from selected idx) one step
# allowing another entry (or entries).
#
# Ex:
# in /directory
# 000.mp4, 001.mp4, 002.mp4, 003.mp4
# python_function()
# --> 000.mp4, 001.mp4, 004.mp4, 003.mp4


# CAREFUL! THIS SCRIPT ACTUALLY REMOVES FILES, AND CAN POTENTIALLY HAVE
# HAZARDOUS CONSEQUENCES IF USED WRONG.

def get_number_of_files_in_dir(path, file_ending=False, count_hidden=False):
    """
    Counts the number of files in a given directory.
    If count_hidden flag is True, it also counts hidden files.
    If file_ending is specified, it only counts files containing that string.
    Also, if file_ending is specified, hidden files are skipped by default.
    (Careful, this might return unexpected results in certain cases, and should
    be rewritten later).
    Args: path, file_ending=None, count_hidden=False.
    """

    import os

    count = 0
    out_list = []
    if file_ending:                                    # count specified only
        assert type(file_ending) == type(str()), "file_ending must be of type string. In function 'get_number_of_files_in_dir'"
        for item in os.listdir(path):
            if os.path.isfile(path + "/" + item) and file_ending in item:
                count += 1
    elif count_hidden:                                   # count all
        for item in os.listdir(path):
            if os.path.isfile(path + "/" + item):
                count += 1
    else:
        for item in os.listdir(path):
            if os.path.isfile(path + "/" + item) and item[0] is not ".":
                count += 1
    return count


def get_filenames_in_directory(path, file_ending=False, count_hidden=False):
    """
    Returns a list with filenames in a directory.
    If count_hidden flag is True, it also appends hidden files.
    If file_ending is specified, it only appends files containing that string".
    Also, if file_ending is specified, hidden files are skipped by default.
    (Careful, this might return unexpected results in certain cases, and should
    be rewritten later).

    Args: path, file_ending=None, count_hidden=False.
    File_ending can be given either with or without period. I.e. ".txt" or "txt"
    """
    out_list = []
    if file_ending:                                    # count specified only
        assert type(file_ending) == type(str()), "file_ending must be of type string. In function 'get_number_of_files_in_dir'"
        for item in os.listdir(path):
            if os.path.isfile(path + "/" + item) and file_ending in item:
                out_list.append(item)
    elif count_hidden:                                   # count all
        for item in os.listdir(path):
            if os.path.isfile(path + "/" + item):
                out_list.append(item)
    else:
        for item in os.listdir(path):
            if os.path.isfile(path + "/" + item) and item[0] is not ".":
                out_list.append(item)
    return out_list


def get_number_of_digits(path, file_ending=None, count_hidden=False):
    """
    Returns an integer of how many digits there are in the file names.
    """
    filenames = get_filenames_in_directory(path, file_ending, count_hidden)
    longest = ""
    for item in filenames:
        if len(item) > len(longest):
            longest = item
    n_digits = longest.split(".")   # splits at file ending
    return len(n_digits[0])         # returns number of the chars before file ending


def rename_files(path, slc, offset, file_ending=None, projectpath):
    """
    [WARNING: this function renames (and can therefore potentially delete) files
    in the given the directory! As a safety measure, a 'projectpath' parameter
    must be provided, so that only files within this directory can be modified
    (default set to flimmering-project)]

    Renames a sequence of files in a folder. Important: all files in the folder
    must be of the same filetype! (Unless file_ending is specified).
    Also assumes that the files are numbered in a consistent manner.

    Depends on functions 'get_filenames_in_directory' and 'get_number_of_digits'

    Arguments:
    slc: (slice) how many files from last file in the sequence should be renamed.
        This is counted from the last file and backwards.
        Passing 3 as parameter means that the filename of the three last
        files will be modified by given offset.
    offset: what number should be added (positive or negative) to the filenames.
    file_ending: discriminate on files to be handled based on a file_ending.
        I.e: only modify name of .txt files. Passed as a string either with or without "."

    """

    # Check that path-string is within projectpath-string.
    # This to avoid accidental and unintended overwrites in other directories.
    assert projectpath in path, "Careful, check your path given to function 'rename_files'. Does not correspond to projectpath"

    filelist = get_filenames_in_directory(path, file_ending, count_hidden=False)    # count_hidden should not be set to True, to avoid any modification of hidden system files.
    n_digits = get_number_of_digits(path,file_ending,count_hidden=False)

    filelist.reverse()      # Read from the back to avoid overwrite
    old_filelist = [i for i in filelist[:slc]]  # old_filelist, just use the slice that has been modified.

    if len(str(offset)) > n_digits:
        n_digits_flag = True
        n_digits = len(str(offset))     # Adjusting all filenames to new number of digits
        old_filelist = [i for i in filelist]
    else:
        n_digits_flag = False

    for idx, name in enumerate(filelist[:slc:]):   # Reading list from backwards
        name = name.split(".")  # Makes a list of filename and ending
        new_name = int(name[0])
        ending = name[1]
        new_name += offset
        new_name = "{:0{n_digits}d}.{ending}".format(new_name, n_digits=n_digits, ending=ending)
        filelist[idx] = new_name

    print(old_filelist)
    print(filelist)

    for idx, old_name in enumerate(old_filelist):
        if n_digits_flag:   # If so, also adjusting number of trailing zeros in other filenames as well
            name = filelist[idx].split(".")
            new_name = name[0]
            ending = name[1]
            new_name = "{:0{n_digits}d}.{ending}".format(int(new_name), n_digits=n_digits, ending=ending)
        else:
            new_name = filelist[idx]
        os.rename(path + "/" + old_name, path + "/" + new_name)
    return 0
