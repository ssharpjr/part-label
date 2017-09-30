#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
###############################################################################

import os
import sys
from datetime import datetime


# Date file exists. If not, create it.
# Serial number file exists. If not, create it.
# Current date is captured and compared to the date file.
# If the current date is greater than the date file,
# - then a new day has started.
# - The serial number file is reset to 0.
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
    current_date = get_date()
    with open(date_file, 'w') as f:
        f.write(current_date)


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


def reset_sn():
    # Reset the serial number counter to 0.
    sn = 0
    return sn


def pad_sn(sn):
    # Serial number must be 4-digits.  Pad with zeros if too short.
    sn = str(sn)
    sn = sn.rjust(4, '0')
    return sn


def write_sn_file(sn):
    sn = str(sn)
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
        sn = reset_sn()
        write_sn_file(sn)
    except BaseException as e:
        print(e)
        sys.exit()


def increment_sn():
    sn = read_sn_file()
    sn = int(sn)

    # Must be 4-digits.  Reset if 9999 is reached.
    if sn >= 9999:
        # Reset serial number
        sn = reset_sn()

    sn = sn + 1
    sn = str(sn)
    write_sn_file(sn)


def get_serial_number():
    # Compare the current date and saved date.
    current_date = get_date()
    saved_date = read_date_file()
    if current_date > saved_date or current_date < saved_date:
        # It's a new day (or a wrong date), update date file
        write_date_file()

        # Reset serial number and
        # save serial number to sn_file
        sn = reset_sn()
        write_sn_file(sn)
        sn = read_sn_file()
        sn = pad_sn(sn)
        return sn

    else:
        # If it is the same day, get the serial number
        # from sn_file.
        sn = read_sn_file()
        return sn


def get_full_serial_number():
    current_date = get_date()
    sn = get_serial_number()
    return current_date + sn


def test_serial_number_generation():
    date = get_date()
    sn = get_serial_number()
    for i in range(1, 20000):
        print(date + sn)
        increment_sn()


def print_sn_file():
    cmd = "cat " + sn_file
    print()
    os.system(cmd)
    print()
