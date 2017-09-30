#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
###############################################################################

# IMPORTS
import os

# import RPi.GPIO as io

from functions import get_press_id, set_printer, exit_program,\
                      send_image_file_to_printer
from iqapi_test import press_api_request_pn_only
from serialnumber import get_full_serial_number, increment_sn, print_sn_file

###############################################################################

# VARIABLES
DEBUG = 1

label_template_file_name = "label_template.zpl"
label_file = "/tmp/label_file.zpl"

###############################################################################
# SETUP Raspberry Pi

# Assign GPIO pins
btn_pin = 16  # PLC Input

# Setup GPIO, pull-down resistors from 3V3 (False by default)
# io.setmode(io.BCM)
# io.setup(btn_pin, io.IN, pull_up_down=io.PUD_DOWN)
###############################################################################


def set_part_number(press_id):
    # Get Part Number from IQ API
    itemno = press_api_request_pn_only(press_id)
    # Must be 15-digits.  Pad with zeros as needed.
    itemno = str(itemno)
    itemno = itemno.rjust(15, '0')
    return itemno


def build_label(pn, sn):
    with open(label_template_file_name, 'r') as f:
        label_data = f.read()
    label = label_data.format(pn=pn, sn=sn)

    with open(label_file, 'w') as f:
        f.write(label)
        f.truncate()


def print_label(label_printer):
    print_cmd = "lpr -P " + label_printer + " -l " + label_file
    # os.system(print_cmd)
    print(print_cmd)
    cmd = "cat " + label_file
    os.system(cmd)


###############################################################################
# Main

def main():
    # Startup checks and sets
    # COMPLETE: Set Press ID
    press_id = get_press_id()

    # COMPLETE: Set Printer
    # label_printer = set_printer()
    label_printer = "zplprinter"

    # COMPLETE: Send image file to printer just in case
    send_image_file_to_printer(label_printer)

    while True:
        try:
            # COMPLETE: Wait for PLC trigger (button)
            # TODO: Need to test with RPI
            if DEBUG:
                print("Waiting for PLC")
            # Halt the program; wait for the trigger.
            io.wait_for_edge(btn_pin, io.BOTH, bouncetime=200)
            if DEBUG:
                print("PLC trigger detected")

            # COMPLETE: Get Part Number from IQ API
            part_number = set_part_number(press_id)
            if DEBUG:
                print("Part Number: " + str(part_number))

            # COMPLETE: Generate Serial Number
            serial_number = get_full_serial_number()
            if DEBUG:
                print("Serial Number: " + serial_number)

            # COMPLETE: Build label file
            build_label(part_number, serial_number)

            # COMPLETE: Print label
            # TODO: Need to test printing from RPI
            print_label(label_printer)

            # COMPLETE: Increment Serial Number
            increment_sn()

        except KeyboardInterrupt:
            io.cleanup()
            exit_program()

###############################################################################


def test_run():
    # Startup checks and sets
    # COMPLETE: Set Press ID
    press_id = get_press_id()

    # COMPLETE: Set Printer
    # label_printer = set_printer()
    label_printer = "zplprinter"

    # COMPLETE: Send image file to printer just in case
    send_image_file_to_printer(label_printer)

    # COMPLETE: Get Part Number from IQ API
    part_number = set_part_number(press_id)
    if DEBUG:
        print("Part Number: " + str(part_number))

    # Generate Serial Number
    serial_number = get_full_serial_number()
    if DEBUG:
        print("Serial Number: " + serial_number)

    # Build label file
    build_label(part_number, serial_number)

    # Print label
    print_label(label_printer)

    # Increment Serial Number
    increment_sn()

    print_sn_file()


if __name__ == '__main__':
    test_run()
