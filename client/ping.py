import struct
from .client import client
from .helper.mstring import mstr
from .helper import varInt
from .buffer import buffer_reader as reader

def ping(ip, port):
  s = client(ip, port)
  packet_id = b'\x00'
  protocol_version = 757
  data = packet_id \
          + varInt.write(protocol_version) \
          + mstr(s.ip) \
          + struct.pack('>H', port) \
          + b'\x01'
  s.send(data)
  print(data)
  s.send(b'\x00')
  recieved_data = s.recv_data()
  reader.read(recieved_data)
