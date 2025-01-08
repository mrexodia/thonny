# SPDX-FileCopyrightText: 2024 Justin Myers
#
# SPDX-License-Identifier: MIT
"""
Board stub for Arduino Nano ESP32
 - port: espressif
 - board_id: arduino_nano_esp32s3_inverted_statusled
 - NVM size: 8192
 - Included modules: _asyncio, _bleio, _eve, _pixelmap, adafruit_bus_device, adafruit_pixelbuf, aesio, alarm, analogbufio, analogio, array, atexit, audiobusio, audiocore, audiomixer, audiomp3, binascii, bitbangio, bitmapfilter, bitmaptools, board, builtins, builtins.pow3, busdisplay, busio, busio.SPI, busio.UART, canio, codeop, collections, countio, digitalio, displayio, dualbank, epaperdisplay, errno, espidf, espnow, espulp, fontio, fourwire, framebufferio, frequencyio, getpass, gifio, hashlib, i2cdisplaybus, io, ipaddress, jpegio, json, keypad, keypad.KeyMatrix, keypad.Keys, keypad.ShiftRegisterKeys, keypad_demux, keypad_demux.DemuxKeyMatrix, locale, math, max3421e, mdns, memorymap, microcontroller, msgpack, neopixel_write, nvm, onewireio, os, os.getenv, paralleldisplaybus, ps2io, pulseio, pwmio, rainbowio, random, re, rgbmatrix, rotaryio, rtc, sdcardio, sdioio, select, sharpdisplay, socketpool, socketpool.socketpool.AF_INET6, ssl, storage, struct, supervisor, synthio, sys, terminalio, time, touchio, traceback, ulab, usb, usb_cdc, usb_hid, usb_midi, vectorio, warnings, watchdog, wifi, zlib
 - Frozen libraries: 
"""

# Imports
import busio
import microcontroller


# Board Info:
board_id: str


# Pins:
B0: microcontroller.Pin  # GPIO46
B1: microcontroller.Pin  # GPIO0
D0: microcontroller.Pin  # GPIO44
D1: microcontroller.Pin  # GPIO43
D2: microcontroller.Pin  # GPIO5
D3: microcontroller.Pin  # GPIO6
D4: microcontroller.Pin  # GPIO7
D5: microcontroller.Pin  # GPIO8
D6: microcontroller.Pin  # GPIO9
D7: microcontroller.Pin  # GPIO10
D8: microcontroller.Pin  # GPIO17
D9: microcontroller.Pin  # GPIO18
D10: microcontroller.Pin  # GPIO21
D11: microcontroller.Pin  # GPIO38
MOSI: microcontroller.Pin  # GPIO38
D12: microcontroller.Pin  # GPIO47
MISO: microcontroller.Pin  # GPIO47
D13: microcontroller.Pin  # GPIO48
SCK: microcontroller.Pin  # GPIO48
LED: microcontroller.Pin  # GPIO48
A0: microcontroller.Pin  # GPIO1
D17: microcontroller.Pin  # GPIO1
A1: microcontroller.Pin  # GPIO2
D18: microcontroller.Pin  # GPIO2
A2: microcontroller.Pin  # GPIO3
D19: microcontroller.Pin  # GPIO3
A3: microcontroller.Pin  # GPIO4
D20: microcontroller.Pin  # GPIO4
A4: microcontroller.Pin  # GPIO11
D21: microcontroller.Pin  # GPIO11
SDA: microcontroller.Pin  # GPIO11
A5: microcontroller.Pin  # GPIO12
D22: microcontroller.Pin  # GPIO12
SCL: microcontroller.Pin  # GPIO12
A6: microcontroller.Pin  # GPIO13
D23: microcontroller.Pin  # GPIO13
A7: microcontroller.Pin  # GPIO14
D24: microcontroller.Pin  # GPIO14
LED_R: microcontroller.Pin  # GPIO46
LED_G: microcontroller.Pin  # GPIO45
LED_B: microcontroller.Pin  # GPIO0


# Members:
def I2C() -> busio.I2C:
    """Returns the `busio.I2C` object for the board's designated I2C bus(es).
    The object created is a singleton, and uses the default parameter values for `busio.I2C`.
    """

def SPI() -> busio.SPI:
    """Returns the `busio.SPI` object for the board's designated SPI bus(es).
    The object created is a singleton, and uses the default parameter values for `busio.SPI`.
    """


# Unmapped:
#   none
