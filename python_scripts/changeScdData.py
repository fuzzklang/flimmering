# Script to edit first line in text file (to change audio output name)
# This line is used in scd script when it is run with sclang for audio generating
# Also add support for amp level?

def change_scd_data(timestamp, name, amp, mapping, filepath=None, projectdirectory="/shit_going_on/flimmering"):
    """
    'Filepath' is the directory path for the run_data.txt which the SC-script
    fetches metadata/run-data from.
    Filepath must be a directory.

    The different information is seperated by a newline.

    Timestamp gets written into run_data.
        It gives the filename for csv-file (where SC-scripts finds csv data).
    New audio output filename is written as string into 'run_data'-file.
    Amp is written to run_data. Gives the audio level of audio file being made by sc.
        Between 0.0 and 1.0. (inf to 0 dB)
    Mapping tells SC-script to map synths-configurations either to 'color'-array
        or 'shape'-array.
        Must be either 'color' or 'shape'

   This function returns 0.
    """

    # TODO: GET PROPER PATH
    if filepath == None:
        from sys import platform
        if platform == "darwin":
            filepath = "flimmering/score_files/run_data"
        elif platform == "linux":
            filepath = "flimmering/score_files/run_data"

    if projectdirectory not in filepath:
        raise RuntimeError("Given directory is not matching with project directory. Interrupting program. (in function changeScdData)")

    datafile = "/run_data.txt"
    filepath = filepath + datafile
    print("FILEPATH", filepath) # DEBUG
    with open(filepath, "w") as f:
        timestamp = "{}".format(str(timestamp))
        name = '{}'.format(str(name))
        amp = '{}'.format(str(amp))
        mapping = '{}'.format(str(mapping))
        f.write(timestamp + "\n")
        f.write(name + "\n")
        f.write(amp + "\n")
        f.write(mapping)

    return 0
