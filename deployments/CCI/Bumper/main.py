#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
###############################################################################

# IMPORTS
import os
import sys
from datetime import datetime
from time import sleep

import RPi.GPIO as io
import serial
from iqapi import press_api_request_pn_only

from program_template.serialnumber import get_full_serial_number, increment_sn, \
    date_file, sn_file

###############################################################################

# VARIABLES
DEBUG = 1

serial_port = '/dev/ttyUSB0'

part_number_file = "PART_NUMBERS.TXT"
label_template_file_name = "label_template.zpl"
label_file = "label_file.zpl"  # Generated on the fly.
sn_log_file = "log/serial_numbers.log"

# From serialnumber.py (date_file, sn_file)

# List of files required to be present at the start
file_list = [date_file, sn_file, sn_log_file]

###############################################################################
# SETUP Raspberry Pi

# Assign GPIO pins
btn_pin = 25        # PLC Input
switch_pin_1 = 24   # Part Selector Switch Input

# Setup GPIO
io.setmode(io.BCM)

# Pulling Resistors 101: Pull-Up vs Pull-Down.
# btn_pin is PULLED-DOWN to 0V (False by default).
# btn_pin is connected to a button/relay.
# The other end of the button is connected to 3V3.
# When the button is pushed, btn_pin RISES HIGH to 3V3 (becomes True).
io.setup(btn_pin, io.IN, pull_up_down=io.PUD_DOWN)
###############################################################################


def reboot_system():
    io.cleanup()
    os.system('sudo reboot')


def run_or_exit_program(status):
    if status == 'run':
        restart_program()
    elif status == 'exit':
        print("\nExiting")
        io.cleanup()
        sys.exit()


def restart_program():
    print("\nRestarting program")
    # sleep(1)
    io.cleanup()
    os.execv(__file__, sys.argv)


def get_part_numbers():
    # TODO: Test
    if DEBUG:
        print("Getting Part Numbers...")
    try:
        with open(part_number_file, 'r') as f:
            part_number_list = f.read().split('\n')
            if DEBUG:
                print("Part Numbers: " + str(part_number_list))
            return part_number_list
    except IOError:
        print(part_number_file + " not found!\nExiting")
        sys.exit()


def set_part_number(part_number_list):
    # TODO: Test
    # Set the part number based on the Part Selector Switch Position
    if DEBUG:
        print("Setting Part Number")
    if io.input(switch_pin_1) == 1:
        part_number = part_number_list[0]
    else:
        part_number = part_number_list[1]
    return part_number


def check_serial_port():
    # Check if the serial port exists
    if DEBUG:
        print("\nChecking serial port...")
    serial_check = serial.Serial(serial_port, timeout=1)
    try:
        is_port = serial_check.read()
        sleep(0.1)
        serial_check.close()
    except serial.SerialException as e:
        print(e)
        run_or_exit_program('exit')


def send_serial(file):
    # Setup Serial Port
    ser = serial.Serial(serial_port, baudrate=9600, bytesize=8, parity='N',
                        stopbits=1, xonxoff=0, timeout=5)
    if DEBUG:
        print("(Sending " + file + ")")
    with open(file) as f:
        label = f.read()
    try:
        ser.write(label.encode())
        ser.close()
    except serial.SerialException as e:
        if DEBUG:
            print("Error: " + e)
        run_or_exit_program('exit')


def send_image_file_to_printer():
    if DEBUG:
        print("\nSending images to printer...")
    image_file = "cc/images/CC_120.GRF"
    send_serial(image_file)


def check_for_files(f_list):
    # Check for needed files
    if DEBUG:
        print("\nChecking files...")
    for file in f_list:
        if not os.path.isfile(file):
            if DEBUG:
                print(file + " is missing")
            run_or_exit_program('exit')


def pad_part_number(part_number):
    part_number = str(part_number)
    part_number = part_number.rjust(15, '0')
    return part_number


def build_label(pn, padpn, sn):
    if DEBUG:
        print("\nBuilding ZPL label file")
    with open(label_template_file_name, 'r') as f:
        label_data = f.read()
    label = label_data.format(pn=pn, padpn=padpn, sn=sn) + "\n"

    with open(label_file, 'w') as f:
        f.write(label)
        f.truncate()


def log_serial_number(part_number, serial_number):
    if DEBUG:
        print("\nWriting log entry")
    # Log serial numbers in a CSV file.
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    log_entry = now + "," + part_number + "," + serial_number + "\n"
    if DEBUG:
        print(log_entry)
    with open(sn_log_file, 'a') as f:
        f.write(log_entry)


def print_label():
    if DEBUG:
        print("Printing label")
    send_serial(label_file)


def delete_label():
    # Delete the label file after it is printed to prevent duplicates.
    if DEBUG:
        print("\nDeleting " + label_file)
    os.remove(label_file)


###############################################################################
# Main

def main():
    if DEBUG:
        os.system('clear')
        print()
        print("========================")
        print("| Part Labeling System |")
        print("========================")
        print()

    # Startup checks and sets
    # TODO: Set Part Number

    # Check Serial Port
    check_serial_port()

    # Check for needed files
    check_for_files(file_list)

    # Send image file to printer just in case
    send_image_file_to_printer()

    if DEBUG:
        print()
        print("----------------")
        print("Startup complete")
        print("----------------")
        print()

    while True:
        try:
            # Wait for PLC trigger (button)
            # Wait for RISING edge (pin RISING from 0V to 3V3)
            # PLC sends a 0.2 second signal
            if DEBUG:
                print("\nWaiting on PLC/Button trigger...")
            try:
                io.wait_for_edge(btn_pin, io.RISING, bouncetime=300)
                if DEBUG:
                    print("Button pressed, continuing...\n")
            except KeyboardInterrupt:
                # Only works if a keyboard CTRL-C is pressed.
                run_or_exit_program('exit')

            # Get Part Number from IQ API
            part_number = set_part_number(press_id)
            part_number_padded = pad_part_number(part_number)
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
            print_label()

            # Log printed Serial Number
            log_serial_number(part_number, serial_number)

            # Delete label file to prevent duplicates
            delete_label()

            # Increment Serial Number
            increment_sn()

            # Pause before next run
            sleep(1)

        except KeyboardInterrupt:
            io.cleanup()
            run_or_exit_program('exit')

###############################################################################


def test_run():
    pass


if __name__ == '__main__':
    test_run()
