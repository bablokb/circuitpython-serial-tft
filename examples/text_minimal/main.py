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
from serial_tft.colors import RED, BLACK, WHITE

time.sleep(5)

print("init")
minidrv.init(ser,0)          # rotation: 0
print("clear screen")
minidrv.clear(ser,WHITE)
print("display initialized")

print("scaling text-size")
minidrv.textscale(ser,2)
minidrv.textcolor(ser,BLACK)

print("sending 'Hello world'")
minidrv.text(ser,"Hello world")

(tw,th) = minidrv.textsize(ser,"Hello world",2)
pos = minidrv.position(ser)        # current pos is at top of current line!
pos = (0,pos[1]+th+1)              # move down by text-height+1
print(f"set cursor to {pos}:")
minidrv.position(ser,pos)

print("scaling text-size")
minidrv.textscale(ser,4)

print("sending 'Hello Blinka!'")
minidrv.textcolor(ser,RED)
minidrv.text(ser,"Hello Blinka!")

time.sleep(5)
minidrv.brightness(ser,0.1)
