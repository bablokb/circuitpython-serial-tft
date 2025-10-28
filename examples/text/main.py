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

# wait for the console to connect
if DEBUG:
  time.sleep(5)

tft = Text(ser,reset=True,debug=DEBUG)
print("display initialized")
print(f"current position: {tft.get_cursor()}")

print("sending 'Hello world'")
tft.print("Hello world")

print("query cursor:")
pos = tft.get_cursor()
print(f"current position: {pos}")

print("set cursor to (0,pos[1]+10):")
tft.set_cursor(0,pos[1]+20)
pos = tft.get_cursor()
print(f"current position: {pos}")

print("scaling text-size")
tft.set_textsize(4)

print("sending 'Hello world'")
tft.print("Hello world")

print("query cursor:")
pos = tft.get_cursor()
print(f"current position: {pos}")
