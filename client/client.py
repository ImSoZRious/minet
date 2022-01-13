from hashlib import new
from io import BytesIO
import socket
import threading
import struct
import client.buffer.buffer_reader as reader
import client.helper.varInt as varInt
import client.helper.hostname as hostname
from client.helper.mstring import mstr

class client:
  def __init__(self, ip, port, handler = {}):
    self.ip = ip
    self.hostname = hostname.gethostname(ip, port)
    self.addr = (self.hostname, port)
    self.socket = socket.socket()
    try:
      self.socket.connect(self.addr)
    except Exception as e:
      raise e
    self.open = True
    self.listener = threading.Thread(target=self.listen)

    self.handler = handler

    self.compress = False
    self.max_packet_size = None
  
  def ifalive(func):
    def wrapper(self):
      if not self.open:
        return
      func(self)
    return wrapper

  def close(self):
    if self.open:
      self.open = False
      self.socket.close()
      print('socket close')

  def send(self, byte_message):
    vi = varInt.write(len(byte_message))
    # print(vi + byte_message)
    self.socket.send(vi + byte_message)

  def listen(self):
    while self.open:
      try:
        packet_size, _ = varInt.read_from_socket(self.socket)
      except:
        self.close()
        return

      data = BytesIO()
      length = 0

      while self.open and length < packet_size:
        remaining = packet_size - length
        try:
          new_byte = self.socket.recv(remaining)
          length += len(new_byte)
          data.write(new_byte)
        except:
          self.close()
          return

      data.seek(0)
      ret = reader.read(data, self.compress)
      self.handle(ret)

  def handle(self, result):
    if not result['type'] in self.handler:
      return
    self.handler[result['type']](result)
  
  def login(self, player_name: str):
    # handshake
    packet_id = b'\x00'
    protocol_version = 757
    handshake_data = packet_id \
            + varInt.write(protocol_version) \
            + mstr(self.ip) \
            + struct.pack('>H', self.addr[1]) \
            + b'\x02'
    self.send(handshake_data)

    # login start
    self.send(b'\x00' + mstr(player_name))

    # set compression
    data = BytesIO(self.socket.recv(4096))
    packet_size, _ = varInt.read_from_buffer(data)
    packet_id = data.read(1)
    print(data.getvalue())
    if packet_id == '\x03':
      self.compress = True
      self.max_packet_size = varInt.read_from_buffer(data)

    # login success with compression  
      data = self.socket.recv(4096)
      print(data)
    else:
      # login success without compression
      data = self.socket.recv(4096)
      print(data)
    
    self.listener.start()