# !/usr/bin/env python
# ----------------------------------------------------------------------
# qwiic_eeprom_ex4_user_options.py
#
# This example demonstrates how to record various user settings easily 
# to EEPROM.
# ----------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, July 2021
#
# This python library supports the SparkFun Electronics qwiic sensor/
# board ecosystem on a Raspberry Pi (and compatable) single board 
# computers.
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun by buying a board!
#
# ======================================================================
# Copyright (c) 2021 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# "Software"), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to 
# the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#=======================================================================
# Example 4

from __future__ import print_function
import qwiic_eeprom
import time
import sys
from collections import namedtuple

LOCATION_SETTINGS = 0

# Load the current settings from EEPROM into the settings struct
def load_user_settings(my_mem, settings):
    # Uncomment these lines to forcibly erase the EEPROM and see how the defaults are set
    # print("\nErasing EEPROM")
    # my_mem.erase()    

    # Check to see if EEPROM is blank. If the first four spots are zeros then we can assume the EEPROM is blank.
    test_read = 0
    if (my_mem.read(LOCATION_SETINGS, test_read) == 0):     # (EEPROM address to read, thing to read to)
        # At power on, settings are set to defaults within the tuple
        # So go record the tuple as it currently exists so that defaults are set
        record_user_settings(my_mem, settings)

        print("\nDefault settings applied")
    else:
        # Read current settings
        my_mem.read(LOCATION_SETTINGS, settings)

# Record the current settings into EEPROM
def recor_user_settings(my_mem, settings):
    my_mem.write(LOCATION_SETTINGS, settings)

def main_menu(my_mem, settings):
    print("""
    1) Set Baud Rate
    x) Exit
    """)
    incoming = raw_input()

    if incoming == "1":
        print("\nEnter baud rate (1200 to 115200): ")
        new_baud = raw_input()
        if int(new_baud) < 1200 or int(new_baud) > 115200:
            print("\nError: baud rate out of range")
        else:
            settings.baud_rate = new_baud
            record_user_settings(my_mem, settings)
    elif incoming == "x":
        return
    else:
        print("\nUnknown choice: " + incoming)

def run_example():

    print("\nSparkFun Qwiic EEPROM, Example 4\n")
    my_eeprom = qwiic_eeprom.QwiicEEPROM()

    if my_eeprom.begin() != 0:
        print("\nThe Qwiic EEPROM isn't connected to the syste. Please check your connection", \
            file=sys.stderr)
        return
    
    print("\nEEPROM ready!")

    # TODO: figure out if all this named tuple stuff is correct...
    Settings = namedtuple("Settings", "baud_rate log_date enable_IMU cal_value")

    # Default settings
    default_settings = Settings(115200, False, True, -5.17)    

    print("\nSize of user settings (bytes): " + str(sys.getsizeof(default_settings)))

    load_user_settings(my_eeprom, default_settings)

    print("\nBaud rate: " + str(default_settings.baud_rate))

    log_str = ""
    if default_settings.log_date == True:
        log_str = "True"
    else:
        log_str = "False"
    print("\nlogDate: " + log_str)

    print("\ncalValue: " + str(default_settings.cal_value))

    # Now we can change something
    default_settings.baud_rate = 57600

    # Save it
    record_user_settings()

    # And we never have to worry about byte alignment or EEPROM locations!
    print("\nPress any key to get menu")

    while True:
        # TODO: figure this part out...
        main_menu(my_eeprom, default_settings)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
    