import client.buffer.buffer_unpack as unpacker
import client.buffer.buffer_logger as log

status_packet_format = {b'\x00': 'j'}

def read(data: bytes):
  cur = 0
  # l = len(data)
  # while cur < l:
  result = unpacker.unpack(status_packet_format[data[cur: cur + 1]], data, cur + 1)[0]
  log.log(data[cur: cur + 1], result)
  # cur += packet_length