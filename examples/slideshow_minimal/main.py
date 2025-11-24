# ----------------------------------------------------------------------------
# Example slideshow using the minimal driver.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-serial-tft
# ----------------------------------------------------------------------------

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

from serial_tft import minidrv

# wait for the console to connect
time.sleep(5)

minidrv.init(ser)
print("clear screen")
minidrv.clear(ser)
print("display initialized")

x = 0
for f in ["1", "2", "3", "4"]:
  minidrv.draw(ser,f)
  x += 30
  minidrv.position(ser,(x,x))
