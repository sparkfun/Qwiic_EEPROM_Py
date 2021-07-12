# !/usr/bin/env python
# ----------------------------------------------------------------------
# qwiic_eeprom_ex5_interface_test.py
#
# This example demonstrates how to read and write various variables to memory
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
# Example 5

from __future__ import print_function
import qwiic_eeprom
import time
import sys

def run_example():

    print("\nSparkFun Qwiic EEPROM, Example 5\n")
    my_eeprom = qwiic.eeprom.QwiicEEPROM()

    if my_eeprom.begin() != 0:
        print("\nThe Qwiic EEPROM isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    print("\nEEPROM ready!")

    my_eeprom.set_memory_size(51200 / 8)    # Qwiic EEPROM is 24512C (512kbit)
    # my_eeprom.set_page_size(128)
    # my_eeprom.disable_poll_for_write_complete()

    all_tests_passed = True

    print("\nMem size in bytes: " + str(my_eeprom.length()))

    # Erase test
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    start_time = time.time()
    my_eeprom.erase()
    end_time = time.time()
    print("\nTime to erase all EEPROM: " + str(end_time * 1000 - start_time * 1000) + "ms")

    # Byte sequential test
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    print("\n")
    print("\n8 bit tests")
    my_value1 = 200
    my_value2 = 23
    random_location = random(0, my_eeprom.length())

    start_time = time.time()
    my_eeprom.write_byte(random_location, my_value1)   # (location, data)
    end_time = time.time()
    my_eeprom.write(random_location + 1, my_value2)
    print("\nTime to record byte: " + str(end_time - start_time) + " s")

    start_time = time.time()
    my_eeprom.write_byte(random_location, my_value1)    # (location, data)
    end_time = time.time()
    print("\nTime to write identical byte to same location (should be ~0s): " + str(end_time - start_time) + " s")

    start_time = time.time()
    response1 = my_eeprom.read_byte(random_location)
    end_time = time.time()
    print("\nTime to read byte: " + str(end_time - start_time) + " s")

    response2 = my_eeprom.read_byte(random_location + 1)
    print("\nLocation " + str(random_location) + " should be " + str(my_value1) + ": " + str(response1))
    print("\nLocation " + str(random_location + 1) + " should be " + str(my_value2) + ": " + str(response2))
    
    if my_value1 != response1:
        all_tests_passed = False
    if my_value2 != response2:
        all_tests_passed = False
    
    # 16 bit test
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    print("\n")
    print("\n16 bit tests")

    my_value3 = 3411
    my_value4 = -366
    random_location = random(0, my_eeprom.lenghth())

    start_time = time.time()
    my_eeprom.write(random_location, my_value3)
    end_time = time.time()
    print("\nTime to record 16 bits: " str(end_time - start_time) + " s")

    my_eeprom.write(random_location + 2, my_value4)

    response3 = 0
    response4 = 0

    start_time = time.time()
    my_eeprom.read(random_location, response3)
    end_time = time.time()
    print("\nTime to read 16 bits: " + str(end_time - start_time) + " s")

    my_eeprom.read(random_location + 2, response4)
    print("\nLocation " + str(random_location) + " should be " + str(my_value3) + ": " + str(response3))
    print("\nLocation " + str(random_location + 2) + " should be " + str(my_value4) + ": " + str(response4))

    if my_value3 != response3:
        all_tests_passed = False
    if my_value4 != response4:
        all_tests_passed = False
    
    # 32 bit test
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    print("\n")
    print("\n32 bit tests")

    my_value5 = -245000
    my_value6 = 400123
    random_location = random(0, my_eeprom.length())

    start_time = time.time()
    my_eeprom.write(random_location, my_value5)
    end_time = time.time()
    print("\nTime to record int32: " + str(end_time - start_time) + " s")
    my_eeprom.write(random_location + 4, my_value6)

    response5 = 0
    response6 = 0

    start_time = time.time()
    my_eeprom.read(random_location, response5)
    end_time = time.time()
    print("\nTime to read 32 bits: " + str(end_time - start_time) + " s")

    my_eeprom.read(random_location + 4, response6)
    print("\nLocation " + str(random_location) + " should be " + str(my_value5) + ": " + str(response5))
    print("\nLocation " + str(random_location + 4) + " should be " + str(my_value6) + ": " + str(response6))

    if my_value5 != response5:
        all_tests_passed = False
    if my_value6 != response6:
        all_tests_passed = False
    
    # 32 bit sequential test
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    my_value7 = -341002
    my_value8 = 241544
    random_location = random(0, my_eeprom.length())

    my_eeprom.write(random_location, my_value7)
    my_eepomr.write(random_location + 4, my_value8)

    response7 = 0
    response8 = 0

    start_time = time.time()
    my_eeprom.read(random_location, response7)
    end_time = time.time()
    print("\nTime to read 32 bits: " + str(end_time - start_time) + " s")

    my_eeprom.read(random_location + 4, response8)
    print("\nLocation " + str(random_location) + " should be " + str(my_value7) + ": " + str(response7))
    print("\nLocation " + str(random_location + 4) + " should be " + str(my_value8) + ": " + str(response8))

    if my_value7 != response7:
        all_tests_passed = False
    if my_value8 != response8:
        all_tests_passed = False
    
    # Float sequential test
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    my_value9 = -7.35
    my_value10 = 5.22
    random_location = random(0, my_eeprom.length())

    my_eeprom.write(random_location, my_value9)
    my_eeprom.write(random_location + 4, my_value10)

    response9 = 0
    response10 = 0

    start_time = time.time()
    my_eeprom.read(random_location, response9)
    end_time = time.time()
    print("\nTime to read float: " + str(end_time - start_time) + " s")

    my_eeprom.read(random_location + 4, response10)
    print("\nLocation " + str(random_location) + " should be " + str(my_value9) + ": " + str(response9))
    print("\nLocation " + str(random_location + 4) + " should be " + str(my_value10) + ": " + str(response10))

    if my_value9 != response9:
        all_tests_passed = False
    if my_value10 != response10:
        all_tests_passed = False
    
    # 64 bits sequential test
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    print("\n")
    print("\n64 bit tests")

    my_value11 = -290.3485723409857
    my_value12 = 384.957
    my_value13 = 917.14159
    my_value14 = 254.8877
    random_location = random(0, my_eeprom.length())

    start_time = time.time()
    my_eeprom.write(random_location, my_value11)
    end_time = time.time()
    print("\nTime to record 64 bits: " + str(end_time - start_time) + " s")

    my_eeprom.write(random_location + 8, my_value12)
    # TODO: not sure if this is the right way to get the size of something...
    my_eeprom.write(my_eeprom.length() - sys.getsizeof(my_value13), my_value13) # Test end of EEPROM space

    response11 = 0
    response12 = 0
    response13 = 0

    start_time = time.time()
    my_eeprom.read(random_location, response11)
    end_time = time.time()
    print("\nTime to read 64 bits: " + str(end_time - start_time) + " s")

    my_eeprom.read(random_location + 8, response12)
    my_eeprom.read(my_eeprom.length() - sys.getsizeof(my_value13), response13)
    print("\nLocation " + str(random_location) + " should be " + str(my_value11) + ": " + str(response11))
    print("\nLocation " + str(random_location + 8) + " should be " + str(my_value12) + ": " + str(response12))
    print("\nEdge of EEPROM " + str(my_eeprom.lenght() - sys.getsizeof(my_value13)) + " should be " + str(my_value13) + ": " + str(response13))

    response14 = 0
    my_eeprom.write(my_eeprom.length() - sys.getsizeof(my_value14), my_value14) # Test the re-write of a spot
    my_eeprom.read(my_eeprom.length() - sys.getsizeof(my_value14), response14)
    print("\nRewrite of " + str(my_eeprom.length() - sys.getsizeof(my_value14)) + " should be " + str(my_value14) + ": " + str(response14))

    if my_value11 != response11:
        all_tests_passed = False
    if my_value12 != response12:
        all_tests_passed = False
    if my_value13 != response13:
        all_tests_passed = False
    if my_value14 != response14:
        all_tests_passed = False
    
    # Buffer write test
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    print("\n")
    print("\nBuffer write test")
    
    # TODO: will this work?!
    my_chars = []
    my_chars = "Lorem ipsum dolor sit amet, has in verterem accusamus. Nulla viderer inciderint eum at."
    random_location = random(0, my_eeprom.length())

    est_time = sys.getsizeof(my_chars) / my_eeprom.get_page_size() * my_eeprom.get_page_write_time()
    print("\nCalculated time to record array of " + str(sys.getsizeof(my_chars)) + " characters: ~" + str(est_time) + " ms")

    start_time = time.time()
    my_eeprom.write(random_location, my_chars)
    end_time = time.time()
    print("\nTime to record array: " + str(end_time - start_time) + " s")

    read_my = []

    start_time = time.time()
    my_eeprom.read(random_location, read_my)
    end_time = time.time()
    print("\nTime to read array: " + str(end_time - start_time) + " s")

    print("\nLocation " + str(random_location) + " string should read: " + my_chars)
    print("\n" + read_my)

    if my_chars != read_my:
        print("\nString compare failed")
        all_tests_passed = False

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    print("\n")
    print("\nMemory Contents: ")

    for x in range(0, 32 * 4):
        if x % 16 == 0:
            print("\n")
        print("\n0x" + str(my_eeprom.read(x)))
    
    if all_tests_passed == True:
        print("\nAll tests PASSED!")
    else:
        print("\nOne or more tests failed. See output")

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)