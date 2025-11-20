# ----------------------------------------------------------------------------
# Driver for the OpenSmart 2.4" Serial-TFT
#
# Command subset for displaying shapes.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-serial-tft
# ----------------------------------------------------------------------------

""" Serial TFT driver library (shapes commands) """

DRAW_PIXEL = b'\x21'
DRAW_FASTVLINE = b'\x22'
DRAW_FASTHLINE = b'\x23'
DRAW_LINE = b'\x24'
DRAW_RECT = b'\x25'
FILL_RECT = b'\x26'
DRAW_CIRCLE = b'\x27'
FILL_CIRCLE = b'\x28'
DRAW_TRIANGLE = b'\x29'
FILL_TRIANGLE = b'\x2A'
DRAW_ROUNDRECT = b'\x2B'
FILL_ROUNDRECT = b'\x2C'

from .base import Transport

class Shapes:
  """ Shape methods """

  # --- constructor   --------------------------------------------------------

  def __init__(self, uart=None, reset=True, baudrate=None, debug=False):
    """ constructor """

    self._t = Transport(uart,reset,baudrate,debug)

  # --- draw pixel   ---------------------------------------------------------

  def pixel(self, p, color=None):
    """ draw pixel at the given position """
    if color:
      color = [color>>8, color&0xFF]
    else:
      color = self._t.fg_color
    x,y = p
    self._t.command(DRAW_PIXEL,[x>>8, x&0xFF, y>>8, y&0xFF, *color])

  # --- draw vertical line   -------------------------------------------------

  def vertical_line(self, p, h, color=None):
    """ draw a vertical line starting at the given position with given height"""
    if color:
      color = [color>>8, color&0xFF]
    else:
      color = self._t.fg_color
    x,y = p
    self._t.command(DRAW_FASTVLINE,
                    [x>>8, x&0xFF, y>>8, y&0xFF, h>>8, h&0xFF, *color])

  # --- draw horizontal line   -----------------------------------------------

  def horizontal_line(self, p, w, color=None):
    """ draw a horizontal line starting at the given position with given width"""
    if color:
      color = [color>>8, color&0xFF]
    else:
      color = self._t.fg_color
    x,y = p
    self._t.command(DRAW_FASTHLINE,
                    [x>>8, x&0xFF, y>>8, y&0xFF, w>>8, w&0xFF, *color])

  # --- draw line   ----------------------------------------------------------

  def line(self, p0, p1, color=None):
    """ draw a line from (x0,y0) to (x1,y1) """
    if color:
      color = [color>>8, color&0xFF]
    else:
      color = self._t.fg_color
    x0,y0 = p0
    x1,y1 = p1
    self._t.command(DRAW_LINE,
                    [x0>>8, x0&0xFF, y0>>8, y0&0xFF,
                     x1>>8, x1&0xFF, y1>>8, y1&0xFF,
                     *color])

  # --- draw rectangle   -----------------------------------------------------

  def rectangle(self, p, w, h, r=None, filled=False, color=None):
    """ draw a rectangle at (x,y) with given width, height and rounding """
    if color:
      color = [color>>8, color&0xFF]
    else:
      color = self._t.fg_color
    if filled and not r:
      cmd = FILL_RECT
    elif filled and r:
      cmd = FILL_ROUNDRECT
    elif not filled and not r:
      cmd = DRAW_RECT
    elif not filled and r:
      cmd = DRAW_ROUNDRECT
    x,y = p
    args = [x>>8, x&0xFF, y>>8, y&0xFF, w>>8, w&0xFF, h>>8, h&0xFF]
    if r:
      args.extend([r>>8, r&0xFF])
    args.extend(color)
    self._t.command(cmd, args)

  # --- draw circle   --------------------------------------------------------

  def circle(self, p, r, filled=False, color=None):
    """ draw a circle at (x,y) with given radius """
    if color:
      color = [color>>8, color&0xFF]
    else:
      color = self._t.fg_color
    if filled:
      cmd = FILL_CIRCLE
    else:
      cmd = DRAW_CIRCLE
    x,y = p
    self._t.command(cmd, [x>>8, x&0xFF, y>>8, y&0xFF, r>>8, r&0xFF, *color])

  # --- draw triangle   ------------------------------------------------------

  def triangle(self, points, filled=False, color=None):
    """ draw a triangle between given points """
    if color:
      color = [color>>8, color&0xFF]
    else:
      color = self._t.fg_color
    if filled:
      cmd = FILL_TRIANGLE
    else:
      cmd = DRAW_TRIANGLE
    args = []
    for p in points:
      args.extend([p[0]>>8, p[0]&0xFF, p[1]>>8, p[1]&0xFF])
    args.extend(color)
    self._t.command(cmd, args)
