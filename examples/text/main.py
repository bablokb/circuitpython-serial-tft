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

from serial_tft.screen import Screen
from serial_tft.colors import RED

# wait for the console to connect
if DEBUG:
  time.sleep(5)

screen = Screen(ser,reset=True,debug=DEBUG)
print("clear screen")
screen.clear()
print("set rotation to 0")
screen.rotation(0)
print("display initialized")
print(f"current position: {screen.position()}")

print("sending 'Hello world'")
screen.text("Hello world")

print("query cursor: ", end="")
pos = screen.position()
print(f"{pos}")

tsize = screen.textsize("Hello world")
print(f"size of 'Hello world': ({tsize[0]},{tsize[1]})")
print(f"set cursor to (0,{pos[1]+tsize[1]+1}):")
screen.position((0,pos[1]+tsize[1]+1))
pos = screen.position()
print(f"current position: {pos}")

print("scaling text-size")
screen.textscale(4)

print("sending 'Hello world' in red")
screen.textcolor(RED)
screen.text("Hello world")

print("query cursor: ", end="")
pos = screen.position()
print(f"{pos}")

time.sleep(5)
screen.brightness(0.1)
