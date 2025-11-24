# ----------------------------------------------------------------------------
# Minimal driver implementation for OpenSmart 2.4" Serial-TFT
#
# A simplistic version for memory constrained systems.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-serial-tft
# ----------------------------------------------------------------------------

""" Serial TFT driver library, minimal version """

import time

# --- read response   --------------------------------------------------------

def _read(uart,timeout):
  """ read result """
  start = time.monotonic()
  while time.monotonic() - start < timeout and not uart.in_waiting:
    pass
  if not uart.in_waiting:
    raise RuntimeError("timeout")

  b = uart.read(1)
  if b != b'\x7E':
    raise RuntimeError("ill. response")
  data_len = ord(uart.read(1))
  buf = bytearray(data_len)
  if uart.readinto(buf) != data_len:
    raise RuntimeError("ill. response")
  if buf[-1:] != b'\xEF':
    raise RuntimeError(f"illegal response with last byte {buf[-1:]}")
  # return response without start-byte, length-byte, end-byte
  return buf[0:-1]

# --- send cmd   -------------------------------------------------------------

def _send(uart, cmd, timeout=5):
  """ send command and return result """

  uart.reset_input_buffer()
  #print(f"command: {cmd.hex()}")
  uart.write(cmd)
    
  # read response data/code: either (None,code) or (data,code)
  resp = _read(uart, timeout)
  if cmd == b'\x01' and data is None:    # SET_READ_CURSOR
    while resp == b'ok':
      resp = _read(uart, timeout)
    return (resp[1:], _read(uart, timeout))
  elif resp in [b'ok', b'e1', b'e2']:       # response without data
    return (None, resp)
  else:
    rc = _read(uart, timeout)
    if rc != b'ok':
      raise RuntimeError("failed")
    else:
      # strip first byte (i.e. cmd byte from data)
      return (resp[1:], rc)

# --- send cmd + string   ----------------------------------------------------

def _send_str(uart, c, s):
  """ send given command with string argument """
  cmd = bytearray(b'\x7e\xFF'+c)
  cmd[1] = len(s)+2
  cb = [ord(ch) for ch in s]
  cmd.extend(cb)                 # small builds don't support s.encode('utf8')
  cmd.append(0xef)
  _send(uart,cmd)

# --- initialize display   ---------------------------------------------------

def init(uart):
  """ initialize display """

  # on POR, wait for the display
  while True:
    _, resp = _send(uart, b'\x7e\x02\x00\xef')
    if resp == b'ok':
      break

  # reset display
  _, resp = _send(uart, b'\x7e\x02\x05\xef')
  if resp not in [b'ok', b'e1']:
    raise RuntimeError("failed")

# --- clear screen   ---------------------------------------------------------

def clear(uart):
  """ clear display """
  _send(uart,b'\x7e\x04\x20\x00\x00\xef')

# --- set brightness   -----------------------------------------------------

def set_brightness(uart,b:float):
  """ set screen brightness """

  # brightness is 0-1
  cmd = bytearray(b'\x7e\x03\x06\xFF\xef')
  cmd[3] = int(b*255)
  _send(uart,cmd)

# --- draw image   -----------------------------------------------------------

def draw(uart, filename):
  """ draw image at current position. """
  _send_str(uart, b'\x30', filename)

# --- print text   -----------------------------------------------------------

def text(uart, text):
  """ print text at given position """
  _send_str(uart, b'\x11', text)

# --- set text size   ---------------------------------------------------------

def textsize(uart, scale):
  """ set textsize """
  cmd = bytearray(b'\x7e\x03\x03\xFF\xef')
  cmd[3] = scale
  _send(uart,cmd)

# --- set text size   ---------------------------------------------------------

def textcolor(uart, color):
  """ set textsize """
  cmd = bytearray(b'\x7e\x04\x02\xFF\xFF\xef')
  cmd[3] = color >> 8
  cmd[4] = color & 0xFF
  _send(uart,cmd)

# --- set cursor position   --------------------------------------------------

def position(uart, x:int, y:int):
  """ set cursor position """
  cmd = bytearray(b'\x7e\x06\x01')
  cmd.extend([x>>8, x&0xFF, y>>8, y&0xFF])
  cmd.append(0xef)
  _send(uart,cmd)
