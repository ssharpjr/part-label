#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
###############################################################################

# IMPORTS
import os
from datetime import datetime
from time import sleep

import RPi.GPIO as io

from functions import get_press_id, set_printer, exit_program,\
                      send_image_file_to_printer
from iqapi_test import press_api_request_pn_only
from serialnumber import get_full_serial_number, increment_sn, print_sn_file

###############################################################################

# VARIABLES
DEBUG = 1

label_template_file_name = "label_template.zpl"
label_file = "/tmp/label_file.zpl"
sn_log_file = "log/serial_numbers.log"

###############################################################################
# SETUP Raspberry Pi

# Assign GPIO pins
btn_pin = 25  # PLC Input

# Setup GPIO
io.setmode(io.BCM)

# Pulling Resistors 101: Pull-Up vs Pull-Down.
# btn_pin is PULLED-DOWN to 0V (False by default).
# btn_pin is connected to a button/relay.
# The other end of the button is connected to 3V3.
# When the button is pushed, btn_pin RISES HIGH to 3V3 (becomes True).
io.setup(btn_pin, io.IN, pull_up_down=io.PUD_DOWN)
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


def log_serial_number(part_number, serial_number):
    # Log serial numbers in a CSV file.
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    log_entry = now + "," + part_number + "," + serial_number + "\n"
    with open(sn_log_file, 'a') as f:
        f.write(log_entry)


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

    # TODO: Set Printer (TOGGLE this on!)
    # label_printer = set_printer()
    label_printer = "zplprinter"

    # COMPLETE: Send image file to printer just in case
    send_image_file_to_printer(label_printer)

    while True:
        try:
            # TODO: Wait for PLC trigger (button)
            # TODO: Need to test with RPI
            sleep(1)  # Add small delay before reading button
            btn_state = io.input(btn_pin)
            if btn_state == 1:  # Button is pushed
                # Halt the program until button is released
                if DEBUG:
                    print("Waiting for button release.")
                # Wait for FALLING edge (pin moving from 3V3 to 0V)
                io.wait_for_edge(btn_pin, io.FALLING, bouncetime=300)
                if DEBUG:
                    print("Button released, continuing...")
            if btn_state == 0:  # Button is not pushed
                # Halt the program until button is pressed
                if DEBUG:
                    print("Waiting for button press.")
                # Wait for RISING edge (pin moving from 0V to 3V3)
                io.wait_for_edge(btn_pin, io.RISING, bouncetime=300)
                if DEBUG:
                    print("Button pressed, continuing...")

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

            # COMPLETE: Log printed Serial Number
            log_serial_number(part_number, serial_number)

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

    # Log printed Serial Number
    log_serial_number(part_number, serial_number)

    # Increment Serial Number
    increment_sn()

    print_sn_file()


if __name__ == '__main__':
    test_run()
