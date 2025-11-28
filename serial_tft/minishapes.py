# ----------------------------------------------------------------------------
# Minimal driver implementation for OpenSmart 2.4" Serial-TFT
#
# Shapes-API for memory constrained systems.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-serial-tft
# ----------------------------------------------------------------------------

""" Serial TFT driver library, Shapes-API, minimal version """

from .minidrv import _send, _read

# --- draw pixel   ---------------------------------------------------------

def pixel(uart, p, color=0xFFFF):
  """ draw pixel at the given position """
  cmd = bytearray(b'\x7e\x08\x21')
  cmd.extend([p[0]>>8, p[0]&0xFF, p[1]>>8, p[1]&0xFF,
             color>>8, color&0xFF])
  cmd.append(0xef)
  _send(uart,cmd)

# --- draw vertical line   -------------------------------------------------

def vertical_line(uart, p, h, color=0xFFFF):
  """ draw a vertical line starting at the given position with given height"""
  cmd = bytearray(b'\x7e\x0A\x22')
  cmd.extend([p[0]>>8, p[0]&0xFF, p[1]>>8, p[1]&0xFF,
              h>>8, h&0xFF, color>>8, color&0xFF])
  cmd.append(0xef)
  _send(uart,cmd)

# --- draw horizontal line   -----------------------------------------------

def horizontal_line(uart, p, w, color=0xFFFF):
  """ draw a horizontal line starting at the given position with given width"""
  cmd = bytearray(b'\x7e\x0A\x23')
  cmd.extend([p[0]>>8, p[0]&0xFF, p[1]>>8, p[1]&0xFF,
              w>>8, w&0xFF, color>>8, color&0xFF])
  cmd.append(0xef)
  _send(uart,cmd)

# --- draw line   ----------------------------------------------------------

def line(uart, p0, p1, color=0xFFFF):
  """ draw a line from (x0,y0) to (x1,y1) """
  cmd = bytearray(b'\x7e\x0C\x24')
  cmd.extend([p0[0]>>8, p0[0]&0xFF, p0[1]>>8, p0[1]&0xFF,
              p1[0]>>8, p1[0]&0xFF, p1[1]>>8, p1[1]&0xFF,
              color>>8, color&0xFF])
  cmd.append(0xef)
  _send(uart,cmd)

# --- draw rectangle   -----------------------------------------------------

def rectangle(uart, p, w, h, r=None, filled=False, color=0xFFFF):
  """ draw a rectangle at (x,y) with given width, height and rounding """
  if filled and not r:
    cmd = bytearray(b'\x7e\x0C\x26')
  elif filled and r:
    cmd = bytearray(b'\x7e\x0E\x2C')
  elif not filled and not r:
    cmd = bytearray(b'\x7e\x0C\x25')
  elif not filled and r:
    cmd = bytearray(b'\x7e\x0E\x2B')
  x,y = p
  cmd.extend([x>>8, x&0xFF, y>>8, y&0xFF, w>>8, w&0xFF, h>>8, h&0xFF])
  if r:
    cmd.extend([r>>8, r&0xFF])
  cmd.extend([color>>8, color&0xFF])
  cmd.append(0xef)
  _send(uart,cmd)

# --- draw circle   --------------------------------------------------------

def circle(uart, p, r, filled=False, color=0xFFFF):
  """ draw a circle at (x,y) with given radius """
  if filled:
    cmd = bytearray(b'\x7e\x0A\x28')
  else:
    cmd = bytearray(b'\x7e\x0A\x27')
  x,y = p
  cmd.extend([x>>8, x&0xFF, y>>8, y&0xFF, r>>8, r&0xFF,
              color>>8, color&0xFF])
  cmd.append(0xef)
  _send(uart,cmd)

# --- draw triangle   ------------------------------------------------------

def triangle(uart, points, filled=False, color=0xFFFF):
  """ draw a triangle between given points """
  if filled:
    cmd = bytearray(b'\x7e\x10\x29')
  else:
    cmd = bytearray(b'\x7e\x10\x2A')
  for p in points:
    cmd.extend([p[0]>>8, p[0]&0xFF, p[1]>>8, p[1]&0xFF])
  cmd.extend([color>>8, color&0xFF])
  cmd.append(0xef)
  _send(uart,cmd)
