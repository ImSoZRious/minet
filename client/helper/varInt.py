import struct
from io import BytesIO
from socket import socket

def write(val):
  total = b''
  if val < 0:
    val = (1 << 32) + val
  while val >= 0x80:
    bits = val & 0x7F
    val >>= 7
    total += struct.pack('B', (0x80 | bits))
  bits = val & 0x7F
  total += struct.pack('B', bits)
  return total


def read(s, i):
  total = 0
  shift = 0
  cur = i
  val = 0x80
  while val & 0x80:
    val = struct.unpack('B', s[cur:cur+1])[0]
    cur += 1
    total |= ((val&0x7F)<<shift)
    shift += 7
  if total&(1<<31):
    total = total - (1<<32)
  return (total, cur - i)

def read_from_buffer(bbuff: BytesIO):
  total = 0
  shift = 0
  val = 0x80
  cur = 0
  while val&0x80:
    val = struct.unpack('B', bbuff.read(1))[0]
    total |= ((val&0x7F)<<shift)
    shift += 7
    cur += 1
  if total&(1<<31):
    total = total - (1<<32)
  return (total, cur)

def read_from_socket(sock: socket):
  total = 0
  shift = 0
  val = 0x80
  cur = 0
  while val&0x80:
    val = struct.unpack('B', sock.recv(1))[0]
    total |= ((val&0x7F)<<shift)
    shift += 7
    cur += 1
  if total&(1<<31):
    total = total - (1<<32)
  return (total, cur)
