#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

import os
import sys
from subprocess import check_output, STDOUT

# import RPi.GPIO as io


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


def set_printer():
    label_printer_name = "zplprinter"
    label_printer = check_output("lpstat -p | grep " + label_printer_name + "; exit 0",
                                 stderr=STDOUT, shell=True)
    if not len(label_printer) > 0:
        print("Label printer not detected! \n Exiting")
        # Cannot print labels without a label printer.
        exit_program()


def send_image_file_to_printer(label_printer):
    image_file = "cc/images/CC_120.GRF"
    print_cmd = "lpr -P " + label_printer + " -l " + image_file
    # os.system(print_cmd)
    print(print_cmd)
