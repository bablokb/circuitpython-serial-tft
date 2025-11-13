# ----------------------------------------------------------------------------
# Example using the Text-API.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-serial-tft
# ----------------------------------------------------------------------------

DEBUG=True

import time
try:
  # test native CPython
  import serial
  import sys
  if len(sys.argv) < 2:
    port = "/dev/ttyUSB0"
  else:
    port = sys.argv[1]
  ser = serial.Serial(port,9600)
except:
  # assume native CircuitPython
  import busio
  import board
  try:
    ser = busio.UART(board.TX, board.RX, baudrate=9600)
  except:
    # assume Pico
    ser = busio.UART(board.GP0, board.GP1, baudrate=9600)

from serial_tft.text import Text
from serial_tft.screen import Screen
from serial_tft.colors import RED

# wait for the console to connect
if DEBUG:
  time.sleep(5)

texts = Text(ser,reset=True,debug=DEBUG)
screen = Screen()
print("clear screen")
screen.clear()
print("set rotation to 0")
screen.set_rotation(0)
print("display initialized")
print(f"current position: {texts.get_cursor()}")

print("sending 'Hello world'")
texts.print("Hello world")

print("query cursor: ", end="")
pos = texts.get_cursor()
print(f"{pos}")

tsize = texts.get_textsize("Hello world")
print(f"size of 'Hello world': ({tsize[0]},{tsize[1]})")
print(f"set cursor to (0,{pos[1]+tsize[1]+1}):")
texts.set_cursor(0,pos[1]+tsize[1]+1)
pos = texts.get_cursor()
print(f"current position: {pos}")

print("scaling text-size")
texts.set_textsize(4)

print("sending 'Hello world' in red")
screen.set_colors(fg_color=RED)
texts.print("Hello world")

print("query cursor: ", end="")
pos = texts.get_cursor()
print(f"{pos}")

time.sleep(5)
screen.set_brightness(0.1)
