import client.helper.varInt as varInt
import json
from io import BytesIO

def format_string(data: BytesIO):
  string_size, var_size = varInt.read_from_buffer(data)
  
  return (data.read(string_size).decode('utf-8'), string_size + var_size)

def format_json(data: BytesIO):
  string_size, var_size = varInt.read_from_buffer(data)
  
  return (json.loads(data.read(string_size).decode('utf-8')), string_size + var_size)

formatter = {'s': format_string, 'j': format_json}

def unpack(_format: str, data: BytesIO):
  ret = []
  total_length = 0

  for x in _format:
    val, length = formatter[x](data)
    ret.append(val)
    total_length += length

  return (ret, total_length)