#-----------------------------------------------------------------------------
# qwiic_eeprom.py
#
# Python library for the SparkFun Qwiic EEPROM Breakout - 512Kbit.
#   https://www.sparkfun.com/products/18355
#
#------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, June 2021
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem 
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#==================================================================================
# Copyright (c) 2020 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================

"""
qwiic_eeprom
============
Python module for the SparkFun Qwiic EEPROM Breakout - 512Kbit.

This package is a port of the exisiting [SparkFun External EEPROM Arduino Library](https://github.com/sparkfun/SparkFun_External_EEPROM_Arduino_Library).

This package can be used in conjuction with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py).

New to qwiic? Take a look at the entire [SparkFun Qwiic Ecosystem](https://www.sparkfun.com/qwiic).
"""
# ---------------------------------------------------------------------------------

import math
import time
import qwiic_i2c

_DEFAULT_NAME = "Qwiic EEPROM"

_AVAILABLE_I2C_ADDRESS = [0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57]

class QwiicEEPROM(object):
    """
    Qwiic EEPROM

        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :param i2c_driver: An existing i2c driver object. If not provided a
                        a driver object is created.
        :return: The GPIo device object.
        :rtype: Object
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Variables
    
    memory_size_bytes = 512000 / 8
    page_size_bytes = 64
    page_write_time_ms = 5
    poll_for_write_complete = True

    I2C_BUFFER_LENGTH = 32

    # Constructor
    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        self.address = address if address != None else self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver == None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c == None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

    # ----------------------------------------------------------------------------
    # is_connected(i2c_address)
    #
    # Is an actual board connected to our system?
    def is_connected(self, i2c_address = 255):
        """
            Determine if a Qwiic EEPROM device is connected to the system

            :param i2c_address: I2C address of EEPROM. Larger EEPROMs have two addresses.
            :return: True if the device is connected, false otherwise.
            :rtype: bool
        """
        # DEBUG: Not really sure what the point of the 255 is yet... but I'm just gonna copy it from the lib
        if i2c_address == 255:
            i2c_address = self.address       
        return qwiic_i2c.isDeviceConnected(i2c_address)
    
    # ----------------------------------------------------------------------------
    # begin()
    #
    # Initialize the system and validate the board.
    def begin(self):
        """
            Initialize the operation of the Qwiic EEPROM.
            Run is_connected().

            :return: Returns true if the initialization was successful, false otherwise.
            :rtype: bool
        """
        if self.is_connected() == True:
            return True
        return False

    # ----------------------------------------------------------------------------
    # erase(to_write)
    #
    # Erase entire EEPROM
    def erase(self, to_write = 0x00):
        """
            Erase entire EEPROM.
            
            :param to_write: byte to write into each spot of EEPROM 
            :return: Nothing
            :rtype: void
        """
        temp_buffer = []

        for x in range(0, page_size_bytes):
            temp_buffer[x] = to_write
        
        for addr in range(0, self.length(), page_size_bytes):
            self.write(addr, temp_buffer, page_size_bytes)
    
    # DEBUG: Why do we have two functions that DO EXACTLY THE SAME THING?!
    # Same as get_memory_size()
    # ----------------------------------------------------------------------------
    # length()
    #
    # Returns the memory size of the EEPROM
    def length(self):
        """
            Returns the memory size of the EEPROM

            :return: memory_size_bytes
            :rtype: int
        """
        return self.memory_size_bytes
    
    # ----------------------------------------------------------------------------
    # is_busy(i2c_address)
    #
    # Returns true if the device is not answering (currently writing).
    def is_busy(self, i2c_address = 255):
        """
            Returns true if the device is not answering (currently writing).

            :param i2c_address: I2C address of EEPROM. Larger EEPROMs have two addresses.
            :return: True if the IC is busy, false otherwise
            :rtype: bool
        """
        if i2c_address == 255:
            i2c_address = self.address

        # DEBUG: what the heck is this?!
        if self.is_connected(i2c_address):
            return False
        return True

    # ----------------------------------------------------------------------------
    # set_memory_size(mem_size)
    #
    # Set the size of memory in bytes
    def set_memory_size(self, mem_size):
        """
            Set the size of memory in bytes

            :param mem_size: memory size in bytes
            :return: Nothing
            :rtype: void
        """
        self.memory_size_bytes = mem_size

    # ----------------------------------------------------------------------------
    # get_memory_size()
    #
    # Return the size of EEPROM
    def get_memory_size(self):
        """
            Return the size of EEPROM

            :return: memory_size_bytes
            :rtype: int
        """
        return self.memory_size_bytes
    
    # ----------------------------------------------------------------------------
    # set_page_size(page_size)
    #
    # Set the size of the page we can write at a time
    def set_page_size(self, page_size):
        """
            Set the size of the page we can write at a time

            :param page_size: new page size in bytes
            :return: Nothing
            :rtype: void
        """
        self.page_size_bytes = page_size
    
    # ----------------------------------------------------------------------------
    # get_page_size()
    #
    # Return the current page size of EEPROM in bytes
    def get_page_size(self):
        """
            Get the page size

            :return: Current page size off EEPROM in bytes
            :rtype: int
        """
        return self.page_size_bytes
    
    # ----------------------------------------------------------------------------
    # set_page_write_time(write_time_ms)
    #
    # Set the number of ms required per page write
    def set_page_write_time(self, write_time_ms):
        """
            Set the number of ms required per page write

            :param write_time_ms: write time in ms
            :return: Nothing
            :rtype: Void
        """
        self.page_write_time_ms = write_time_ms
    
    # ----------------------------------------------------------------------------
    # get_page_write_time()
    #
    # Get the current time required per page write
    def get_page_write_time(self):
        """
            Get the current time required per page write

            :return: Time required per page write
            :rtype: int
        """
        return self.page_write_time_ms
    
    # ---------------------------------------------------------------------------
    # enable_poll_for_write_complete()
    #
    # Most EEPROMs allow I2C polling of when a write has completed
    def enable_poll_for_write_complete(self):
        """
            Enable I2C polling of when a write has completed

            :return: Nothing
            :rtype: Void
        """
        self.poll_for_write_complete = True

    # --------------------------------------------------------------------------
    # disable_poll_for_write_complete()
    #
    # Disable polling of when a write has completed
    def disable_poll_for_write_complete(self):
        """
            Disable polling of when a write has completed

            :return: Nothing
            :rtype: Void
        """
        self.poll_for_write_complete = False

    # --------------------------------------------------------------------------
    # get_I2C_buffer_size()
    #
    # Return the size of the TX buffer
    def get_I2C_buffer_size(self):
        """
            Return the size of the TX buffer

            :return: I2C_BUFFER_LENGTH_TX
            :rtype: int
        """
        return self.I2C_BUFFER_LENGTH
    
    # --------------------------------------------------------------------------
    # read_byte(eeprom_location)
    #
    # Read a byte from a given location
    def read_byte(self, eeprom_location):
        """
            Read a byte from a given location

            :param eeprom_location: location of EEPROM to read byte from
            :return: byte read
            :rtype: int
        """
        temp_byte = 0
        self.read(eeprom_location, temp_byte, 1)
        return temp_byte
    
    # -------------------------------------------------------------------------
    # read(eeprom_location, buff, bufer_size)
    #
    # Bulk reads from EEPROM 
    # Handles breaking up read amt into 32 byte chunks (can be overridden with set_I2C_buffer_size)
    # Hangles a read that straddles the 512kbit barrier
    def read(self, eeprom_location, buff, buffer_size):
        """
            Bulk reads from EEPROM
            Handles breaking up read amt into 32 byte chunks (can be overridden 
            with set_I2C_buffer_size)
            Handles a read that straddles the 512kbit barrier
            
            :param eeprom_location: location in EEPROM to start reading from 
            :param buff: buffer which holds the bytes that have been read
            :param buffer_size: number of bytes to be read from EEPROM
            :return: Nothing
            :rtype: Void
        """
        received = 0

        while received < buffer_size:

            # Limit the amount to write to a page size
            amt_to_read = buffer_size - received

            # TODO: not sure about this part
            # What is the rasppi I2C buffer size limit?
            if amt_to_read > self.I2C_BUFFER_LENGTH:
                amt_to_read = self.I2C_BUFFER_LENGTH
            
            # Check if we are dealing with large (>512kbit) EEPROMs
            i2c_address = self.address
            
            if self.memory_size_bytes > 0xFFFF:
                # Figure out if we are going to cross the barrier with this read
                if eeprom_location + received < 0xFFFF:
                    if 0xFF - (eeprom_location + received) < amt_to_read:
                        amt_to_read = 0xFFFF - (eeprom_location + received)
                    
                # Figure out if we are accessing the lower half or the upper half
                if eeprom_location + received > 0xFFFF:
                    i2c_address |= 0b100    # Set the block bit to 1
                
            # See if EEPROM is available or still writing to a previous request
            # TODO: need to figure out what the RaspPi equivalent function is to isBusy()
            while self.poll_for_write_complete & isBusy(i2c_address) == True:
                time.sleep(0.1) # This shortens the amount of time waiting between writes but hammers the I2C bus
            
            self._i2c.writeByte((eeprom_location + received) >> 8)  # MSB
            self._i2c.writeByte((eeprom_location + received) & 0xFF)    # LSB

            # TODO: not sure if this is right
            buff = self._i2c.readBloc(self.address, 0, amt_to_read)
            
            received += amt_to_read

    # -------------------------------------------------------------------------------------------
    # write_byte(eeprom_location, data_to_write)
    #
    # Write a byte to a given EEPROM location
    def write_byte(self, eeprom_location, data_to_write):
        """
            Write a byte to a given EEPROM location

            :param eeprom_location: location in EEPROM to write byte to 
            :param data_to_write: the byte to be written to EEPROM
            :return: Nothing
            :rtype: Void
        """
        if self.read(eeprom_location) != data_to_write: # Update only if data is new
            self.write(eeprom_location, data_to_write, 1)
    
    # -------------------------------------------------------------------------------------------
    # write(eeprom_location, data_to_write, buffer_size)
    #
    # Write large bulk amounts
    # Limits writes to the I2C buffer size (default is 32 bytes)
    def read(self, eeprom_location, data_to_write, buffer_size):
        """
            Write large bulk amounts of data
            Limits writes to the I2C buffer size (default is 32 bytes)

            :param eeprom_location: location in EEPROM to write data to 
            :param data_to_write: list of bytes to be written to EEPROM
            :param buffer_size: length of the data_to_write list
            :return: Nothing
            :rtype: Void
        """
        # Error check
        if eeprom_location + buffer_size >= self.memory_size_bytes:
            buffer_size = self.memory_size_bytes - eeprom_location
        
        max_write_size = self.page_size_bytes
        if max_write_size > self.I2C_BUFFER_LENGTH - 2:
            max_write_size = self.I2C_BUFFER_LENGTH - 2 # TODO: need to find out the I2C transaction limit of rasp pi
        
        # Break the buffer into page sized chunks
        recorded = 0
        while recorded < buffer_size:
            # Limit the amount to write to either the page size or the Rasp Pi limit of #TODO: what?
            amt_to_write = buffer_size - recorded
            if amt_to_write > max_write_size:
                amt_to_write = max_write_size
            
            if amt_to_write > 1:
                # check for crossing of a page line. Writes cannot cross a page line.
                page_number_1 = (eeprom_location + recorded) / self.page_size_bytes
                page_number_2 = (eeprom_location + recorded + amt_to_write - 1) / self.page_size_bytes
                if page_number_2 > page_number_1:
                    amt_to_write = (page_number_2 * self.page_size_bytes) - (eeprom_location + recorded) # Limit the read amt to go right up to edge of page barrier

            i2c_address = self.address
            # Check if we are dealing with large (>512kbit) EEPROMs
            if self.memory_size_bytes > 0xFFFF:
                # Figure out if we are accessing the lower half or the upper half
                if eeprom_location + recorded > 0xFFFF:
                    i2c_address |= 0b100    # Set the block bit to 1
            
            # See if EEPROM is available or still writing a previous request
            while self.poll_for_write_complete & isBusy(i2c_address) == True:   # Poll device
                time.sleep(0.1) # This shortens the amountof time waiting between writes but hammers the I2C bus
            
            self._i2c.writeByte((eeprom_location + recorded) >> 8)  # MSB
            self._i2c.writeByte((eeprom_location + recorded) & 0xFF)    # LSB
            for x in range(0, amt_to_write):
                self._i2c.writeByte(data_to_write[recorded + x])
            
            recorded += amt_to_write

            if self.poll_for_write_complete == False:
                # TODO: need to fix this delay call!
                time.sleep(self.page_write_time_ms) # Delay the amount of time to record a page
