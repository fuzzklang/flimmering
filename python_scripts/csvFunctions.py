# WRITE CSV-FILES
#
# Contains several functions for reading and writing CSV-files.
#
# Write functions in this script takes input from a sequence (here:
# list of dictinaries) and output the data to a CSV file.
# Also supports headers, which get written to their own file.
#
# Read functions read from a CSV-file and convert it to appropriate format for
# data generation and to other parts of the project.

import datetime
import os

from misc import escape_newlines

def simple_write_csv(filepath, lists, csv_header):
    """
    A simple CSV function writing to a txt-file.
    Header line required to assure compatability with other functions in
    the project.
    Each list in the 'lists' is a column of values.
    Thus each list correspond the their value in the header.
    All lists must also be of same length.

    Arguments:
    path: filepath
    lists: list of lists. Each list correspond to a column in the CSV file
        Must be of same length, and correspond to header values.
    csv_header: items/strings describing values in columns.
        Number of items must correspond to number of lists/columns
    """

    assert csv_header and type(csv_header) == type(list()), "\n\nA valid csv_header must be passed to function 'simple_write_csv'\n"
    assert len(csv_header) == len(lists), "\n\nNumber of columns/lists must correspond to number of items in header line. In function 'simple_write_csv'\n"

    # Checking that all lists are of equal length
    length = len(lists[0])  # Comparison list, first list in 'lists'
    if not all(len(lst) == length for lst in lists):    # If not, raise an Error
        raise RuntimeError("\n\nAll list in 'lists' must be of equal length. In function 'simple_write_csv'\n")

    with open(filepath, "w") as f:
        # Writing header
        s = str()
        for item in csv_header[0:-1]:
            s += str(item) + ","        # temporary string, to write to file
        s += str(csv_header[-1]) + "\n" # adding last element (or just the single element) without adding commas, and adding newline
        f.write(s)                      # writing to file

        # Adding data from lists
        s = str()
        for idx, lst in enumerate(lists[0]):    # First list is reference list
            s += str().join(str(lst[idx]) + "," for lst in lists[0:-1]) # adding all but last items + comma
            s += str(lists[-1][idx]) + "\n"                             # adding last item + newline

        # Escaping newlines with backslash. Delete this part if not working properly
        if "\n" in s:
            s = escape_newlines(s)
        #

        f.write(s)                              # Writing to file

    return 0


def write_from_seq_to_csv(directory_path, sequence, csv_header_order=None, export_filename=None):
    """
    This function writes from a sequence (list of dictionaries) to a csv-file,
    and in the context of this project, it should be readible by SuperCollider.

    (In this project, the 'absolute_sequence' will be used for this purpose.)

    Arguments:
    directory_path: exportpath (directory)
    sequence: sequence specifying values, durations, etc.
    csv_header_order: an (ordered) list specifying header names for each column
        in CSV-file. Reading of dictionaries in sequence is based on this
        csv_header_order, thus names in this list must correspond with keys in
        sequence-dictionaries.
    export_filename: name (usually a number) for exported video and audio files.

    NB:
    Filename is created internally by function, and only directory_path, not a
    filepath, is given as argument. The reason for this is because the function
    must check if a header is passed or not. If a header is passed (from
    sequence) a csv_header.txt file and a csv_data.txt file are both created
    within the same directory. It is the path of this directory which is given
    as parameter. Otherwise there would be a conflict between path as directory
    name or as filename
    """

    #if not os.path.exists(directory_path):  # Comment out when this script not __main__
    #    os.makedirs(directory_path)         # Only for troubleshooting/testing

    if sequence[0]["type"] == "header":
        start_idx = 1           # Setting starting idx for reading the dictionary later in function
        keys = list(sequence[0].keys())
        values = list(sequence[0].values())

        # RISKY APPENDAGE. TO WRITE EXPORT FILENAME TO HEADER
        # NOT FOR USAGE IN SC-SCRIPT, JUST FOR HUMAN READING
        if export_filename:
            keys.append("filename")
            values.append(export_filename)
        # REMOVE IF NEEDED

        with open(directory_path + "/csv_header.txt", "w") as f:
            for key in keys[0:-1]:  # To avoid last comma
                f.write(key+",")
            f.write(str(keys[-1]))
            f.write("\n")
            for value in values[0:-1]:  # To avoid last comma
                f.write(str(value) + ",")
            f.write(str(values[-1]))
    else:
        start_idx = 0           # If no header, start idx at 0

    # If noe csv_header_order is given,
    # base header line in csv file on keys from first dictionary.
    # Keys-list decides order of values in csv-file
    if csv_header_order == None:
        keys = list(sequence[start_idx].keys())
    else:
        keys = csv_header_order

    with open(directory_path + "/csv_data.txt", "w") as f:
        for key in keys[0:-1]:        # Writing header line in csv file, avoiding last comma
            f.write(key + ",")
        f.write(str(keys[-1]))
        f.write("\n")

        for dictionary in sequence[start_idx:]:  # Start idx dependent on whether 'header' is given or not
            for key in keys[0:-1]:
                elem = str(dictionary[key])

                # Escaping newlines with backslash. Delete this part if not working properly
                if "\n" in elem:
                    elem = escape_newlines(elem)
                #

                f.write(elem + ",")

            # Escaping newlines with backslash. Delete this part if not working properly
            if "\n" in keys[-1]:
                elem = escape_newlines(str(dictionary[keys[-1]]))
            else:
                elem = str(dictionary[keys[-1]])
            f.write(elem)
            #
            #f.write(str(keys[-1]))     # Old code, decomment if deleting escape_newline function calls
            f.write("\n")   # Newline for each dictionary

    return 0


def read_csv(dir_path=None, filepath=None):
    """
    Reads a CSV-file and and translate it to a list of dictionaries.
    NB: REQUIRES A HEADER LINE
    Items in header line will function as the keys of each dictionary.
    Returns an (ordered) list of dictionaries, each containing key and value
    pairs derived from the header line.
    Can either take 'dir_path' as argument. Assumes there is a txt-file in the
    given directory with the name "/csv_data.txt". Otherwise a complete
    filepath can be specified. If both are given, filepath takes precedence.
    """

    def convert_to_num(s):
        """
        Takes a string and checks if it is convertable to an integer or float.
        Converts to the appropriate value if so.
        If not convertible it returns the given argument unmodified.
        """
        try:
            s = int(s)          # Check for int
            return s
        except ValueError:      # If not:
            try:
                s = float(s)    # Check for float
                return s
            except ValueError:  # Else: return input value unmodified
                return s

    out_sequence = []
    keys = []

    if not filepath:                            # Check if 'filepath' argument is given.
        assert dir_path, "\n\nEither filepath or dir_path must be given as arguments to function 'read_csv'\n"
        filepath = dir_path + "/csv_data.txt"   # If not, assign to default

    with open(filepath, "r") as f:
        whole_file = f.read()           # Whole file as a string
        lines = whole_file.split("\n")  # Splits file at newlines, returns a list of strings
        if str() in lines:              # If empty string in lines,
            while str() in lines:       # remove all empty rows from csv-file
                lines.remove(str())

        for idx, line in enumerate(lines):
            if line and line[-1] == ",":                      # If line is not empty, and last char is ",",
                line = line[0:-1] + line[-1].replace(",","")  # remove trailing commas
                lines[idx] = line

        for item in lines[0].split(","):    # Assuming header. Dependency on this!
            keys.append(item)               # Making a list of keys, to create dictionaries from

        for line in lines[1:]:          # Assuming header. Doesn't work properly without
            temp_dictionary = {}        # Dictionary to be appended to out_sequence
            temp_list = line.split(",") # Splits line at commas, returns a list of items.
            for idx, item in enumerate(temp_list):
                item = convert_to_num(item)
                temp_dictionary[keys[idx]] = item
            out_sequence.append(temp_dictionary)

    return out_sequence




"""
# ----- TESTING -----
now = datetime.datetime.now()
DIR = "flimmering/tmp/csv_tests/csv_test-{}-{:02d}-{:02d}__{:02d}-{:02d}-{:02d}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
READ_DIR = "flimmering/tmp/csv_tests/csv_test-2018-03-05__17-57-44"

if not os.path.exists(DIR):  # Comment out when this script not __main__
    os.makedirs(DIR)         # Only for troubleshooting/testing

# TESTING WRITING/READING

SEQ = [{'type': 'header', 'framerate': 30, 'num_events': 12, 'total_duration': 2.4666666666666663},
{'type': 'event', 'event_num': 0, 'color': 'R', 'shape': 'Circle', 'duration': 0.2},
{'type': 'event', 'event_num': 1, 'color': 'Black', 'shape': 'None', 'duration': 0.16666666666666666},
{'type': 'event', 'event_num': 2, 'color': 'G', 'shape': 'Rectangle', 'duration': 0.26666666666666666},
{'type': 'event', 'event_num': 3, 'color': 'Black', 'shape': 'None', 'duration': 0.13333333333333333},
{'type': 'event', 'event_num': 4, 'color': 'B', 'shape': 'Triangle', 'duration': 0.3},
{'type': 'event', 'event_num': 5, 'color': 'Black', 'shape': 'None', 'duration': 0.2},
{'type': 'event', 'event_num': 6, 'color': 'R', 'shape': 'Circle', 'duration': 0.2},
{'type': 'event', 'event_num': 7, 'color': 'Black', 'shape': 'None', 'duration': 0.26666666666666666},
{'type': 'event', 'event_num': 8, 'color': 'G', 'shape': 'Rectangle', 'duration': 0.1},
{'type': 'event', 'event_num': 9, 'color': 'Black', 'shape': 'None', 'duration': 0.3},
{'type': 'event', 'event_num': 10, 'color': 'B', 'shape': 'Triangle', 'duration': 0.16666666666666666},
{'type': 'event', 'event_num': 11, 'color': 'Black', 'shape': 'None', 'duration': 0.16666666666666666}]

#write_from_seq_to_csv(DIR, SEQ, None)  # Write to file
#k = read_csv(READ_DIR)                 # read csv-file



# TESTING simple_write_csv
FILEPATH = DIR + "/csv_test.txt"
HEADER = ["A", "B", "C"]
CSV_WRITE_TEST = [[1,1,1],[2,2,2],[3,3,3]]
#HEADER = ["A"]
#CSV_WRITE_TEST = [[1,1,1]]
simple_write_csv(filepath=FILEPATH, lists=CSV_WRITE_TEST, csv_header=HEADER)

csv = read_csv(dir_path=None, filepath=FILEPATH)

for d in csv:
    print(d)

"""
