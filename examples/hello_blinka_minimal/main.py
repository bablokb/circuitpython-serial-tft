# ----------------------------------------------------------------------------
# Mix an image and text using the minimal driver.
#
# Copy the file blinka.bmp to the SD-card and insert it into the display.
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
from serial_tft.colors import CYAN

# wait for the console to connect
time.sleep(5)

minidrv.init(ser)
print("clear screen")
minidrv.clear(ser)
minidrv.brightness(ser,1.0)
print("display initialized")

# draw blinka.bmp (size: 234x240)
pos = ((320-234)//2,0)
minidrv.position(ser,pos)
minidrv.draw(ser,"BLINKA")

# add text
minidrv.textscale(ser,3)
(w,h) = minidrv.textsize(ser,"Hello Blinka!",3)
pos = (pos[0]+4,(240//2-3*h))
minidrv.position(ser,pos)
minidrv.textcolor(ser,CYAN)
minidrv.text(ser,"Hello Blinka!")

