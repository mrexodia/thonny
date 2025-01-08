# SPDX-FileCopyrightText: 2024 Justin Myers
#
# SPDX-License-Identifier: MIT
"""
Board stub for CP Sapling M0
 - port: atmel-samd
 - board_id: cp_sapling_m0_revb
 - NVM size: 256
 - Included modules: analogio, array, board, builtins, busio, busio.SPI, busio.UART, collections, digitalio, math, microcontroller, neopixel_write, nvm, os, pwmio, rainbowio, random, rotaryio, rtc, storage, struct, supervisor, sys, time, touchio, usb_cdc, usb_hid, usb_midi
 - Frozen libraries: 
"""

# Imports
import busio
import microcontroller


# Board Info:
board_id: str


# Pins:
D4: microcontroller.Pin  # PA19
A4: microcontroller.Pin  # PA19
SCK: microcontroller.Pin  # PA19
D5: microcontroller.Pin  # PA18
A5: microcontroller.Pin  # PA18
MOSI: microcontroller.Pin  # PA18
D6: microcontroller.Pin  # PA17
A6: microcontroller.Pin  # PA17
MISO: microcontroller.Pin  # PA17
D7: microcontroller.Pin  # PA07
A7: microcontroller.Pin  # PA07
D8: microcontroller.Pin  # PA00
A8: microcontroller.Pin  # PA00
RX: microcontroller.Pin  # PA00
D9: microcontroller.Pin  # PA01
A9: microcontroller.Pin  # PA01
TX: microcontroller.Pin  # PA01
D10: microcontroller.Pin  # PA02
A10: microcontroller.Pin  # PA02
D11: microcontroller.Pin  # PA03
A11: microcontroller.Pin  # PA03
D12: microcontroller.Pin  # PA03
A12: microcontroller.Pin  # PA03
D13: microcontroller.Pin  # PA03
A13: microcontroller.Pin  # PA03
D14: microcontroller.Pin  # PA09
A14: microcontroller.Pin  # PA09
SCL: microcontroller.Pin  # PA09
D15: microcontroller.Pin  # PA08
A15: microcontroller.Pin  # PA08
SDA: microcontroller.Pin  # PA08
NEOPIXEL: microcontroller.Pin  # PA15


# Members:
def I2C() -> busio.I2C:
    """Returns the `busio.I2C` object for the board's designated I2C bus(es).
    The object created is a singleton, and uses the default parameter values for `busio.I2C`.
    """

def STEMMA_I2C() -> busio.I2C:
    """Returns the `busio.I2C` object for the board's designated I2C bus(es).
    The object created is a singleton, and uses the default parameter values for `busio.I2C`.
    """

def SPI() -> busio.SPI:
    """Returns the `busio.SPI` object for the board's designated SPI bus(es).
    The object created is a singleton, and uses the default parameter values for `busio.SPI`.
    """

def UART() -> busio.UART:
    """Returns the `busio.UART` object for the board's designated UART bus(es).
    The object created is a singleton, and uses the default parameter values for `busio.UART`.
    """


# Unmapped:
#   none
