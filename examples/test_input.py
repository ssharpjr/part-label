#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

from time import sleep
import RPi.GPIO as io

btn_pin = 25
io.setmode(io.BCM)
io.setup(btn_pin, io.IN, pull_up_down=io.PUD_DOWN)

while True:
    sleep(1)
    btn_state = io.input(btn_pin)
    if btn_state == 1:
        # Button is pushed.  Wait for release.
        print("waiting on release.")
        io.wait_for_edge(btn_pin, io.FALLING, bouncetime=300)
        print("button released.")
    if btn_state == 0:
        print("waiting on push.")
        io.wait_for_edge(btn_pin, io.RISING, bouncetime=300)
        print("button pushed.")

