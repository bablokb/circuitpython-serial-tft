# -------------------------------------------------------------------------
# Driver for OpenSmart 2.4" Serial-TFT: command constants
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-serial-tft
# -------------------------------------------------------------------------

TEST = b'\x00'

SET_READ_CURSOR = b'\x01'
SET_TEXTCOLOR = b'\x02'
SET_TEXTSIZE = b'\x03'
SET_ROTATION = b'\x04'
RESET = b'\x05'
SET_BACKLIGHT = b'\x06'
READ_TOUCH = b'\x07'

PRINTLN = b'\x10'
PRINT_CHAR_ARRAY = b'\x11'
PRINT_INT_8 = b'\x12'
PRINT_INT_16 = b'\x13'
PRINT_INT_32 = b'\x14'


FILL_SCREEN = b'\x20'
DRAW_PIXEL = b'\x21'
DRAW_FASTVLINE = b'\x22'
DRAW_FASTHLINE = b'\x23'
DRAW_LINE = b'\x24'
DRAW_RECT = b'\x25'
FILL_RECT = b'\x26'
DRAW_CIRCLE = b'\x27'
FILL_CIRCLE = b'\x28'
DRAW_TRIANGLE = b'\x29'
FILL_TRIANGLE = b'\x2A'
DRAW_ROUNDRECT = b'\x2B'
FILL_ROUNDRECT = b'\x2C'

DRAW_BMP = b'\x30'

WRITE_READ_BAUD = b'\x40'
READ_VERSION = b'\x41'
READ_DRIVER_ID = b'\x42'
READ_RESOLUTION = b'\x43'
