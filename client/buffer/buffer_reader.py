import zlib
import client.helper.varInt as varInt
from struct import unpack
import client.buffer.buffer_unpack as unpacker
from io import BytesIO

packet_format = {b'\x00': {'name': 'ping', 'format': 'j'}}

def read(data: BytesIO, compressed: bool = False):
  if compressed:
    data_length, _ = varInt.read_from_buffer(data)
    data = BytesIO(zlib.decompress(data.read()))
  packet_id = data.read(1)
  
  result = unpacker.unpack(packet_format[packet_id]['format'], data)

  return {'type': packet_format[packet_id]['name'], 'data': result}