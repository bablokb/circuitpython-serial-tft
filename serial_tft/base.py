# ----------------------------------------------------------------------------
# Transport implementation for OpenSmart 2.4" Serial-TFT
#
# Don't use this driver directly.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-serial-tft
# ----------------------------------------------------------------------------

""" Serial TFT driver library """

TEST = b'\x00'
RESET = b'\x05'
WRITE_READ_BAUD = b'\x40'
SET_READ_CURSOR = b'\x01'
_START_BYTE = b'\x7E'
_END_BYTE = b'\xEF'
_BAUD = [9600, 19200, 38400, 57600, 115200]

import time

class Transport:
  """ Serial-TFT driver """

  _transport = None

  # --- constructor   --------------------------------------------------------

  def __new__(cls, uart, reset, baudrate, debug):
    if Transport._transport:
      return Transport._transport
    return super(Transport,cls).__new__(cls)

  def __init__(self, uart, reset, baudrate, debug):
    """ constructor """
    if Transport._transport:
      return
    else:
      Transport._transport = self
    self._uart = uart

    if debug:
      self._debug = lambda msg: print(msg)
    else:
      self._debug = lambda msg: None

    # on POR, wait for the display
    while True:
      _, resp = self.command(TEST)
      if resp == b'ok':
        break

    if reset:
      _, resp = self.command(RESET)
      if resp not in [b'ok', b'e1']:
        raise RuntimeError("could not reset TFT")

    if baudrate:
      self.baudrate = baudrate

  # --- convert arguments to bytes   -----------------------------------------

  def _to_bytes(self,arg):
    """ convert argument to bytes """
    if isinstance(arg,str):
      return arg.encode('utf8')
    elif isinstance(arg,bytes):
      return arg
    elif isinstance(arg,int):
      return arg.to_bytes(arg//256+1,'little')
    else:
      raise ValueError(f"unsupported type: {type(arg)}")

  # --- read response   ------------------------------------------------------

  def _read_response(self, timeout):
    """ return response """

    start = time.monotonic()
    while time.monotonic() - start < timeout and not self._uart.in_waiting:
      pass
    self._debug(f"duration: {time.monotonic()-start}")
    if not self._uart.in_waiting:
      raise RuntimeError(f"no response from TFT within {timeout}s")

    b = self._uart.read(1)
    if b != _START_BYTE:
      raise RuntimeError(f"illegal response with first byte {b}")
    data_len = ord(self._uart.read(1))
    buf = bytearray(data_len)
    if self._uart.readinto(buf) != data_len:
      raise RuntimeError(f"illegal response: could not read {data_len} bytes")
    if buf[-1:] != _END_BYTE:
      raise RuntimeError(f"illegal response with last byte {buf[-1:]}")
    # return response without start-byte, length-byte, end-byte
    return buf[0:-1]

  # --- set baudrate   -------------------------------------------------------

  @property
  def baudrate(self):
    """ return current baudrate """
    return self._uart.baudrate

  @baudrate.setter
  def baudrate(self, value: int) -> None:
    """ set (temporary) baudrate of display and UART """

    self.command(WRITE_READ_BAUD,_BAUD.index(value))
    self._uart.baudrate = value

  # --- send command to TFT   ------------------------------------------------

  def command(self, cmd, data=None, timeout=5):
    """ send command to the TFT """

    time.sleep(0.1)
    # convert data to bytes
    if isinstance(data,list):
      data = bytearray(b''.join([self._to_bytes(x) for x in data]))
    elif data:
      data = self._to_bytes(data)
    data_len = len(data) + 2 if data else 2

    # create complete command-sequence
    com_bytes = bytearray(_START_BYTE) 
    com_bytes.extend(self._to_bytes(data_len))
    com_bytes.extend(cmd)
    if data:
      com_bytes.extend(data)
    com_bytes.extend(_END_BYTE)

    # send command
    self._debug(f"command: {com_bytes.hex()}")
    self._uart.reset_input_buffer()
    self._uart.write(com_bytes)
    
    # read response data/code: either (None,code) or (data,code)
    resp = self._read_response(timeout)
    self._debug(f"resp: {resp}")
    if cmd == SET_READ_CURSOR and data is None:
      while resp == b'ok':
        resp = self._read_response(timeout)
      return (resp[1:], self._read_response(timeout))
    elif resp in [b'ok', b'e1', b'e2']:       # response without data
      return (None, resp)
    else:
      rc = self._read_response(timeout)
      if rc != b'ok':
        raise RuntimeError("command failed")
      else:
        # strip first byte (i.e. cmd byte from data)
        return (resp[1:], rc)


