#!/usr/bin/python3

"""
wt.py - work week tracking tool
coded up on 2020-02-03
note: this is terribly written and not optimized at all but it does what i need it to do
"""

import os
from datetime import datetime, timedelta
from sys import argv

NAME = "user"
TARGET_DIR = os.getenv("HOME") + "/wt/"
if not os.path.isdir(TARGET_DIR):
    os.mkdir(TARGET_DIR)

try:
    LATEST = sorted(os.listdir(TARGET_DIR))[-1]
except IndexError:
    LATEST = 1

# slice newest entry's number prefix and increment if it's not the first entry
if LATEST != 1:
    # count number of underscores in filename for optimally split filenames containing underscores
    N_UNDER = 0

    for c in LATEST:
        if c == "_":
            N_UNDER += 1

    PREFIX = str(int(sorted(os.listdir(TARGET_DIR))[-1].rsplit("_", N_UNDER)[0]) + 1)
else:
    PREFIX = str(LATEST)

def df_ger(time):
    """convert datetime objects to german dd.mm.yyyy date format"""
    arr = reversed(str(time).split("-"))
    return ".".join(arr)

def df_univ(time):
    """convert datetime objects to universal yyyy-mm-dd format"""
    arr = str(time).split("-")
    return "_".join(arr)

def read(input_file):
    """read activites from file, storing them in array under the proper dictionary key"""
    days = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": []}
 
    with open(input_file, "r") as f:
        contents = f.read()

    # convert file contents to list, split by newline
    # empty strings will indicate day shift
    tmp = contents.split("\n")
    tmp_size = len(tmp)
    count = -1

    # append activities to the array of corresponding day
    for key, value in days.items():
        while count < tmp_size - 1:
            count += 1
            if tmp[count] == "":
                break

            value.append(tmp[count])

    return days

def assemble(days):
    """assemble work week summary textfile"""
    hours = 8
    days_off = 0

    # automatic week calculation based on what day it is, shoutout to stackoverflow
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    filename = PREFIX + "_" + NAME + "_" + df_univ(week_start) + ".txt"

    dept = input("department: ")

    with open(TARGET_DIR + filename, "w") as f:
        f.write("Week " + PREFIX + "\n")
        f.write(df_ger(week_start) + " - " + df_ger(week_end) + "\n")

        for key, value in days.items():
            f.write("\n")
            f.write(key + ":\n")

            if len(value) > 0:
                if value[0] == "sick":
                    days_off += 1
                    f.write("\n")
                    for i in value:
                        f.write("- " + i + "\n")
                    f.write("\n")
                    f.write("Hours: 0\n")
                    f.write("Department: /\n")
                else:
                    f.write("\n")
                    for i in value:
                        f.write("- " + i + "\n")
                    f.write("\n")
                    f.write("Hours: " + str(hours) + "\n")
                    f.write("Department: " + dept + "\n")
            else:
                days_off += 1
                f.write("\n")
                f.write("Hours: 0\n")
                f.write("Department:\n")

        total_hours = str((5 - days_off) * hours)

        f.write("\n")
        f.write("---\n")
        f.write("Week total: " + total_hours + "\n")

# print usage message on IndexError, i.e. when user forgets to pass input file
try:
    assemble(read(argv[1]))
except IndexError:
    print("usage: ./wt.py <file_to_parse>")
