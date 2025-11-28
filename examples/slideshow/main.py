# ----------------------------------------------------------------------------
# Example using the Image-API.
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

# wait for the console to connect
if DEBUG:
  time.sleep(5)

screen = Screen(ser,reset=True,debug=DEBUG)
print("clear screen")
screen.clear()
#print("set rotation to 0")
#screen.set_rotation(0)
print("display initialized")

x = 0
for f in ["1", "2", "3", "4"]:
  screen.draw(f)
  x += 30
  screen.position((x,x))
