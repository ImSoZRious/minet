from io import BytesIO
import struct
import json
from .helper.mstring import mstr
from .helper import varInt
from .helper.hostname import gethostname
import socket

def ping(ip, port):
  hostname = gethostname(ip, port)
  s = socket.socket()
  s.connect((hostname, port))
  packet_id = b'\x00'
  protocol_version = 757
  data = packet_id \
          + varInt.write(protocol_version) \
          + mstr(ip) \
          + struct.pack('>H', port) \
          + b'\x01'
  s.send(varInt.write(len(data)) + data)
  s.send(b'\x01\x00')
  recieved_data = s.recv(4096)
  
  data = BytesIO(recieved_data)

  _, _ = varInt.read_from_buffer(data)
  data.read(1)
  _, _ = varInt.read_from_buffer(data)
  
  return json.loads(data.read())