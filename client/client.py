import socket
import client.helper.varInt as varInt
import client.buffer as reader
import struct
import client.helper.hostname as hostname
from client.helper.mstring import mstr

class client:
  def __init__(self, ip, port):
    self.ip = ip
    self.hostname = hostname.gethostname(ip, port)
    self.addr = (self.hostname, port)
    self.socket = socket.socket()
    try:
      self.socket.connect(self.addr)
    except Exception as e:
      raise e
    self.status = 'opened'
  
  def ifalive(func):
    def wrapper(self):
      if self.status == 'closed':
        self.close(self)
        return
      func(self)
    return wrapper

  def close(self):
    self.status = 'closed'
    self.socket.close()
    print('socket close')

  def send(self, byte_message):
    vi = varInt.write(len(byte_message))
    # print(vi + byte_message)
    self.socket.send(vi + byte_message)
  
  def recv_data(self):
    first_data = self.socket.recv(4096)
    if not first_data:
      return None
    packet_size, var_size = varInt.read(first_data, 0)
    packet_data = first_data[var_size:]
    
    while len(packet_data) < packet_size:
      data = self.socket.recv(4096)
      packet_data += data
    return packet_data