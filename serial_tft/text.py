# ----------------------------------------------------------------------------
# Driver for the OpenSmart 2.4" Serial-TFT
#
# Command subset for output of texts.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-serial-tft
# ----------------------------------------------------------------------------

""" Serial TFT driver library (text commands) """

SET_READ_CURSOR = b'\x01'
SET_TEXTSIZE = b'\x03'
PRINT_CHAR_ARRAY = b'\x11'

from .base import Transport

class Text:
  """ Text methods """

  # --- constructor   --------------------------------------------------------

  def __init__(self, uart=None, reset=True, baudrate=None, debug=False):
    """ constructor """

    self._t = Transport(uart,reset,baudrate,debug)
    self._text_scale = 2

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
    self._text_scale = scale

  # --- get text dimensions   ------------------------------------------------

  def get_textsize(self, text:int):
    """ get text dimensions (width,height) """

    # for scale==1, charsize is 5x7. Add one pixel between chars for width
    return (self._text_scale*len(text)*5 + (len(text)-1), self._text_scale*7)

  # --- print text at current position   -------------------------------------

  def print(self, text:str):
    """ print string at current position """
    self._t.command(PRINT_CHAR_ARRAY,text)
