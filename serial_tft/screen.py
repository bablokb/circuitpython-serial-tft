# ----------------------------------------------------------------------------
# Driver for the OpenSmart 2.4" Serial-TFT
#
# Command subset for generic screen manipulation.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-serial-tft
# ----------------------------------------------------------------------------

""" Serial TFT driver library (screen commands) """

SET_TEXTCOLOR = b'\x02'
FILL_SCREEN = b'\x20'
SET_ROTATION = b'\x04'
SET_BACKLIGHT = b'\x06'

from .base import Transport

class Screen:
  """ Screen methods """

  # --- constructor   --------------------------------------------------------

  def __init__(self, uart=None, reset=True, baudrate=None,
               fg_color=0xFFFF, bg_color=0x0000, clear=True, debug=False):
    """ constructor """

    self._t = Transport(uart,reset,baudrate,debug)
    self.set_colors(fg_color,bg_color)

  # --- set colors   ---------------------------------------------------------

  def set_colors(self, fg_color=0xFFFF, bg_color=0x0000):
    """ set colors """
    self.fg_color = [fg_color>>8, fg_color & 0xFF]
    self.bg_color = [bg_color>>8, bg_color & 0xFF]
    self._t.command(SET_TEXTCOLOR,self.fg_color)

  # --- clear screen (fill with bg_color)   ----------------------------------
  
  def clear(self):
    """ clear screen """
    self._t.command(FILL_SCREEN,self.bg_color)

  # --- set rotation   -------------------------------------------------------

  def set_rotation(self,rot:int):
    """ set screen rotation """

    # map: 0: no rot, 1: 90, 2: 180, 3: 270
    self._t.command(SET_ROTATION,(rot+90)//90)

  # --- set brightness   -----------------------------------------------------

  def set_brightness(self,b:float):
    """ set screen brightness """

    # brightness is 0-1
    self._t.command(SET_BACKLIGHT,int(b*255))
