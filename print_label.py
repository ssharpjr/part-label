#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
###############################################################################

# IMPORTS
import os
import sys
from datetime import datetime
from time import sleep
from subprocess import check_output, STDOUT

import RPi.GPIO as io

from iqapi import press_api_request_pn_only
from serialnumber import get_full_serial_number, increment_sn

###############################################################################

# VARIABLES
DEBUG = 1

press_id_file = "/boot/PRESS_ID"
label_template_file_name = "label_template.zpl"
label_file = "label_file.zpl"
sn_log_file = "log/serial_numbers.log"

###############################################################################
# SETUP Raspberry Pi

# Assign GPIO pins
btn_pin = 26  # PLC Input

# Setup GPIO
io.setmode(io.BCM)

# Pulling Resistors 101: Pull-Up vs Pull-Down.
# btn_pin is PULLED-DOWN to 0V (False by default).
# btn_pin is connected to a button/relay.
# The other end of the button is connected to 3V3.
# When the button is pushed, btn_pin RISES HIGH to 3V3 (becomes True).
io.setup(btn_pin, io.IN, pull_up_down=io.PUD_DOWN)
###############################################################################


def exit_program():
    print("\nExiting")
    io.cleanup()
    sys.exit()


def get_press_id():
    # Get PRESS_ID from /boot/PRESS_ID file
    # Close the program if no PRESS_ID is found
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
    label_printer = "zplprinter"
    check_label_printer = check_output("lpstat -p | grep " + label_printer +
                                       "; exit 0",
                                       stderr=STDOUT, shell=True)
    if not len(check_label_printer) > 0:
        print("Label printer not detected! \n Exiting")
        # Cannot print labels without a label printer.
        exit_program()
    # Setup printer options
    # TODO: Set Printer Time?
    set_default_printer_cmd = "lpoptions -d " + label_printer +\
                              "> /dev/null 2>&1"
    set_cups_cmd = "lpadmin -p " + label_printer +\
                   " -o usb-no-reattach-default=false > /dev/null 2>&1"
    restart_cups_cmd = "sudo /etc/init.d/cups restart > /dev/null 2>&1"
    os.system(set_default_printer_cmd)
    os.system(set_cups_cmd)
    os.system(restart_cups_cmd)
    return label_printer


def send_image_file_to_printer(label_printer):
    image_file = "cc/images/CC_120.GRF"
    print_cmd = "lpr -P " + label_printer + " -l " + image_file
    os.system(print_cmd)
    # print(print_cmd)


def set_part_number(press_id, pad=False):
    # Get Part Number from IQ API
    itemno = press_api_request_pn_only(press_id)
    # Must be 15-digits.  Pad with zeros as needed.
    itemno = str(itemno)
    if pad:
        itemno = itemno.rjust(15, '0')
    return itemno


def build_label(pn, padpn, sn):
    with open(label_template_file_name, 'r') as f:
        label_data = f.read()
    label = label_data.format(pn=pn, padpn=padpn, sn=sn) + "\n"

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
    os.system(print_cmd)


###############################################################################
# Main

def main():
    # Startup checks and sets
    # Set Press ID
    press_id = get_press_id()

    # Set Printer
    label_printer = set_printer()

    # Send image file to printer just in case
    send_image_file_to_printer(label_printer)

    while True:
        try:
            # Wait for PLC trigger (button)
            # Wait for RISING edge (pin RISING from 0V to 3V3)
            # PLC sends a 0.2 second signal
            if DEBUG:
                print("Waiting on PLC trigger...")
            try:
                io.wait_for_edge(btn_pin, io.RISING, bouncetime=300)
                if DEBUG:
                    print("Button pressed, continuing...")
            except KeyboardInterrupt:
                # Only works if a keyboard CTRL-C is pressed.
                exit_program()

            # Get Part Number from IQ API
            part_number = set_part_number(press_id)
            part_number_padded = set_part_number(press_id, True)
            if DEBUG:
                print("Part Number: " + str(part_number))
                print("Part Number (padded) " + part_number_padded)

            # Generate Serial Number
            serial_number = get_full_serial_number()
            if DEBUG:
                print("Serial Number: " + serial_number)

            # Build label file
            build_label(part_number, part_number_padded, serial_number)

            # Print label
            print_label(label_printer)

            # COMPLETE: Log printed Serial Number
            log_serial_number(part_number, serial_number)

            # COMPLETE: Increment Serial Number
            increment_sn()

            # Pause before next run
            sleep(1)

        except KeyboardInterrupt:
            io.cleanup()
            exit_program()

###############################################################################


def test_run():
    # Nothing to see here.  Move along. :)
    pass


if __name__ == '__main__':
    main()
