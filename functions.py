#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

from datetime import datetime


def exit_program():
    print("\nExiting")
    io.cleanup()
    sys.exit()


def get_day_of_year():
    day_of_year = datetime.now().timetuple().tm_yday
    return day_of_year


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


def setPrinter():
    label_printer = check_output("lpstat -p | grep zplprinter; exit 0",
                                 stderr=STDOUT, shell=True)
    if not len(label_printer) > 0:
        print("Label printer not detected! \n Exiting")
        exit_program()





