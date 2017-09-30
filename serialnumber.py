#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime


# Date file exists.
# Serial number file exists.
# Current date is captured and compared to the date file.
# If the current date is greater than the date file,
# - then a new day has started.
# - The serial number file is reset to 1.
# - The current date is saved to the date file.
# The Serial number is assigned from the serial number file.
# The current date was assigned when captured.
#
# For each run, the comparisons are made.
# The date and serial number are used to generate the code.
# The serial number is incremented after each run.


date_file = "/tmp/date_file.txt"
sn_file = "/tmp/sn_file.txt"


def get_day_of_year():
    day_of_year = datetime.now().strftime("%j")
    return day_of_year


def get_year():
    year = datetime.now().strftime("%y")
    return year


def get_date():
    year = datetime.now().strftime("%y")
    day = datetime.now().strftime("%j")
    return year + day


def write_date_file():
    date = get_date()
    with open(date_file, 'w') as f:
        f.write(date)


def read_date_file():
    try:
        with open(date_file) as f:
            saved_date = f.read().replace('\n', '')
            return saved_date
    except IOError:
        print(date_file + " Not Found.\nCreating it.")
        write_date_file()
    except BaseException as e:
        print(e)
        sys.exit()


def pad_sn(sn):
    sn = str(sn)
    sn = sn.rjust(4, '0')
    return sn


def write_sn_file(sn):
    sn = pad_sn(sn)
    with open(sn_file, 'w') as f:
        f.write(sn)
        f.truncate()


def read_sn_file():
    try:
        with open(sn_file) as f:
            sn = f.read().replace('\n', '')
        sn = str(sn)
        return sn
    except IOError:
        print(sn_file + " Not Found.\nCreating it.")
        # If sn_file is missing, reset sn and create file.
        sn = 1
        write_sn_file(sn)
    except BaseException as e:
        print(e)
        sys.exit()


def increment_sn(sn):
    sn = int(sn)
    sn = sn + 1
    sn = pad_sn(sn)
    return sn


def get_serial_number():
    # Compare the current date and saved date.
    current_date = get_date()
    saved_date = read_date_file()
    if current_date > saved_date:
        # It's a new day, update date file
        write_date_file()

        # Reset serial number and
        # save serial number to sn_file
        sn = 1
        write_sn_file(sn)
        sn = read_sn_file()
        sn = pad_sn(sn)
        return sn

    else:
        # If it is the same day, get the serial number
        # from sn_file.
        sn = read_sn_file()
        return sn


date = get_date()
sn = get_serial_number()
for i in range(1, 10):
    print(date + sn)
    sn = increment_sn(sn)

