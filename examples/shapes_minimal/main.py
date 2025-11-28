# ----------------------------------------------------------------------------
# Example using the Shape-API.
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

from serial_tft.minidrv import init, clear, brightness
from serial_tft import minishapes
import serial_tft.colors as COLORS

time.sleep(5)

print("clear screen")
clear(ser)
brightness(ser,1.0)
print("display initialized")

print("centered pixel in yellow")
p = (160,120)
minishapes.pixel(ser, p, color=COLORS.YELLOW)

p = (10,10); h = 30
print(f"vertical line from {p}, height: {h})")
minishapes.vertical_line(ser, p, h, color=COLORS.BLUE)

p = (10,10); w = 30
print(f"horizontal line from {p}, width: {h})")
minishapes.horizontal_line(ser, p, w, color=COLORS.BLUE)

p0 = (10,10); p1 = (30,30);
print(f"line from {p0} to {p1}")
minishapes.line(ser, p0, p1)

p = (50,50); w = h = 30
print(f"rectangle from {p} with size: ({w},{h})")
minishapes.rectangle(ser, p, w, h, r=None, filled=False, color=COLORS.RED)

p = (p[0]+w,p[1]+h)
print(f"filled rectangle from {p} with size: ({w},{h})")
minishapes.rectangle(ser, p, w, h, r=None, filled=True, color=COLORS.CYAN)

p = (p[0]+w,p[1]+h); r = 5
print(f"rounded rectangle from {p} with size: ({w},{h})")
minishapes.rectangle(ser, p, w, h, r=r, filled=False, color=COLORS.GREEN)

p = (p[0]+w,p[1]+h); r = 5
print(f"filled rounded rectangle from {p} with size: ({w},{h})")
minishapes.rectangle(ser, p, w, h, r=r, filled=True, color=COLORS.MAGENTA)


p = (290,20); r = 20
print(f"circle at {p}, radius: {r}")
minishapes.circle(ser, p, r, filled=False, color=COLORS.WHITE)

p = (p[0]-2*r,p[1]+2*r); r = 30
print(f"filled circle at {p}, radius: {r}")
minishapes.circle(ser, p, r, filled=True, color=COLORS.GREEN)

points = [(10,230),(40,230),(25,205),]
print(f"triangle with points: {points}")
minishapes.triangle(ser, points, filled=False, color=COLORS.CYAN)

points = [(50,230),(80,230),(65,205),]
print(f"filled triangle with points: {points}")
minishapes.triangle(ser, points, filled=True, color=COLORS.MAGENTA)
