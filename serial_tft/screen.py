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

SET_TEXTSIZE = b'\x03'
PRINT_CHAR_ARRAY = b'\x11'
SET_TEXTCOLOR = b'\x02'
FILL_SCREEN = b'\x20'
SET_READ_CURSOR = b'\x01'
SET_ROTATION = b'\x04'
SET_BACKLIGHT = b'\x06'
DRAW_BMP = b'\x30'

from .base import Transport

class Screen:
  """ Screen methods """

  # --- constructor   --------------------------------------------------------

  def __init__(self, uart=None, reset=True, baudrate=None,
               fg_color=0xFFFF, bg_color=0x0000, clear=True, debug=False):
    """ constructor """

    self._t = Transport(uart,reset,baudrate,debug)
    self._text_scale = 2
    self.colors(fg_color,bg_color)

  # --- set colors   ---------------------------------------------------------

  def colors(self, fg_color=None, bg_color=None):
    """ set colors """
    if not bg_color is None:
      self._t.bg_color = [bg_color>>8, bg_color & 0xFF]
    if not fg_color is None:
      self._t.fg_color = [fg_color>>8, fg_color & 0xFF]
      self._t.command(SET_TEXTCOLOR,self._t.fg_color)

  # --- clear screen (fill with bg_color)   ----------------------------------
  
  def clear(self, color=None):
    """ clear screen """
    if color:
      self._t.bg_color = [color>>8, color & 0xFF]
    self._t.command(FILL_SCREEN, self._t.bg_color)

  # --- query/set current cursor position   ----------------------------------

  def position(self, pos=None):
    """ query or set cursor position """
    if pos:
      x, y = pos
      self._t.command(SET_READ_CURSOR,[x>>8, x&0xFF, y>>8, y&0xFF])
    else:
      (data,rc) = self._t.command(SET_READ_CURSOR)
      # data four bytes with: xH xL yH yL
      return (256*int(data[0])+int(data[1]),256*int(data[2])+int(data[3]))
                                
  # --- set rotation   -------------------------------------------------------

  def rotation(self,rot:int):
    """ set screen rotation """

    # map: 0: no rot, 1: 90, 2: 180, 3: 270
    self._t.command(SET_ROTATION,(rot+90)//90)

  # --- set brightness   -----------------------------------------------------

  def brightness(self,b:float):
    """ set screen brightness """

    # brightness is 0-1
    self._t.command(SET_BACKLIGHT,int(b*255))

  # --- set text scale   -----------------------------------------------------

  def textscale(self, scale:int):
    """ set textsize """
    self._t.command(SET_TEXTSIZE,scale)
    self._text_scale = scale

  # --- get text dimensions   ------------------------------------------------

  def textsize(self, text:int):
    """ get text dimensions (width,height) """

    # for scale==1, charsize is 5x7. Add one pixel between chars for width
    return (self._text_scale*len(text)*5 + (len(text)-1), self._text_scale*7)

  # --- set text color   ------------------------------------------------------

  def textcolor(self, color):
    """ set text color """
    self.colors(fg_color=color)

  # --- print text at current position   -------------------------------------

  def text(self, text:str):
    """ print string at current position """
    self._t.command(PRINT_CHAR_ARRAY,text)

  # --- draw image   ---------------------------------------------------------

  def draw(self, filename):
    """ draw image at current position """
    self._t.command(DRAW_BMP,filename)
