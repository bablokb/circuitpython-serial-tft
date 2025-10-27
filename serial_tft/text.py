# ----------------------------------------------------------------------------
# Command Subset for Texts for the OpenSmart 2.4" Serial-TFT
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-serial-tft
# ----------------------------------------------------------------------------

""" Serial TFT driver library (text commands) """

from .commands import SET_READ_CURSOR, SET_TEXTSIZE, PRINT_CHAR_ARRAY
from .base import Transport

class Text:
  """ Text methods """

  # --- constructor   --------------------------------------------------------

  def __init__(self, uart=None, reset=True, baudrate=None,
               fg_color=0xFFFF, bg_color=0x0000, clear=True, debug=False):
    """ constructor """

    self._t = Transport(uart,reset,baudrate,fg_color,bg_color,clear,debug)

  # --- set colors   ---------------------------------------------------------

  def set_colors(self, fg_color=0xFFFF, bg_color=0x0000):
    """ set colors """
    self._t.set_colors(fg_color, bg_color)

  # --- query current cursor position   --------------------------------------

  def get_cursor(self):
    """ query cursor """
    (data,rc) = self._t.command(SET_READ_CURSOR)
    # data four bytes with: xH xL yH yL
    return (256*int(data[0])+int(data[1]),256*int(data[2])+int(data[3]))
                                
  # --- set cursor position   ------------------------------------------------

  def set_cursor(self, x:int, y:int):
    """ set cursor position """
    self._t.command(SET_READ_CURSOR,[x>>8, x&0xFF, y>>8, y&0xFF])

  # --- set text size   ------------------------------------------------------

  def set_textsize(self, scale:int):
    """ set textsize """
    self._t.command(SET_TEXTSIZE,scale)

  # --- print text at current position   -------------------------------------

  def print(self, text:str):
    """ print string at current position """
    self._t.command(PRINT_CHAR_ARRAY,text)
