#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
###############################################################################

# Imports
import os
import sys
from subprocess import check_output, STDOUT

from time import time, strftime, sleep
from datetime import datetime

# import RPi.GPIO as io

from iqapi_test import press_api_request

###############################################################################


# VARIABLES
label_printer_name = "zplprinter"


###############################################################################
# SETUP RPI GPIO

# Assign GPIO pins
btn_pin = 16  # PLC Input

# Setup GPIO, pull-down resistors from 3V3 (False by default)
# io.setmode(io.BCM)
# io.setup(btn_pin, io.IN, pull_up_down=io.PUD_DOWN)
###############################################################################


def exit_program():
    print("\nExiting")
    io.cleanup()
    sys.exit()


def get_press_id():
    # Get PRESS_ID from /boot/PRESS_ID file
    # Close the program if no PRESS_ID is found
    press_id_file = "/boot/PRESS_ID"
    try:
        with open(press_id_file) as f:
            PRESS_ID = f.read().replace('\n', '')
            if len(PRESS_ID) >= 3:
                return PRESS_ID
            else:
                raise ValueError("PRESS_ID is Not Assigned!\nExiting")
                sys.exit()
    except IOError:
        print(press_id_file + " Not Found!\nExiting")
        sys.exit()
    except BaseException as e:
        print(e)
        sys.exit()


def set_part_number(PRESS_ID):
    # Get Part Number from IQ API
    press_id = PRESS_ID
    itemno = press_api_request(press_id)
    return itemno


def set_printer():
    check_output_string = "lpstat -p | grep " + label_printer_name + "; exit 0"
    check_label_printer = check_output(check_output_string, stderr=STDOUT,
                                       shell=True)
    if not len(check_label_printer) > 0:
        print("Label printer not detected! \n Exiting")
        exit_program()
    else:
        label_printer = label_printer_name
    return label_printer


def get_day_of_year():
    day_of_year = datetime.now().timetuple().tm_yday
    return day_of_year


###############################################################################
# Main

def main():
    # TODO: Set Press ID
    PRESS_ID = get_press_id()
    print(PRESS_ID)

    # TODO: Set Printer
    # label_printer = set_printer()

    # TODO: Wait for PLC trigger (button)

    # TODO: Get Part Number from IQ API
    part_number = set_part_number(PRESS_ID)
    print(part_number)

    # TODO: Build label file

    # TODO: Print label


###############################################################################


if __name__ == '__main__':
    main()
