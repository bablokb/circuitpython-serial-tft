# ----------------------------------------------------------------------------
# Driver for the OpenSmart 2.4" Serial-TFT
#
# Command subset for displaying images.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-serial-tft
# ----------------------------------------------------------------------------

""" Serial TFT driver library (image commands) """

DRAW_BMP = b'\x30'

from .base import Transport

class Image:
  """ Image methods """

  # --- constructor   --------------------------------------------------------

  def __init__(self, uart=None, reset=True, baudrate=None, debug=False):
    """ constructor """

    self._t = Transport(uart,reset,baudrate,debug)

  # --- draw image   ---------------------------------------------------------

  def draw(self, filename):
    """ draw image at current position """
    self._t.command(DRAW_BMP,filename)
