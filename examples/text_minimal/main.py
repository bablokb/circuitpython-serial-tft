# ----------------------------------------------------------------------------
# Example using the Text-API.
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
from serial_tft.colors import RED

time.sleep(5)

print("clear screen")
minidrv.clear(ser)
#print("set rotation to 0")
#minidrev.set_rotation(ser,0)
print("display initialized")

print("scaling text-size")
minidrv.textsize(ser,2)

print("sending 'Hello world'")
minidrv.text(ser,"Hello world")

pos = (0,20)
print(f"set cursor to (0,{pos}):")
minidrv.position(ser,pos[0],pos[1])

print("scaling text-size")
minidrv.textsize(ser,4)

print("sending 'Hello Blinka!'")
minidrv.textcolor(ser,RED)
minidrv.text(ser,"Hello Blinka!")

time.sleep(5)
minidrv.set_brightness(ser,0.1)
