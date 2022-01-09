import client.helper.varInt as varInt
import json

def format_string(data: bytes, index: int):
  string_size, var_size = varInt.read(data, index)
  print(string_size, var_size)
  return (data[index + var_size: index + var_size + string_size].decode('utf-8'), string_size + var_size)

def format_json(data: bytes, index: int):
  string_size, var_size = varInt.read(data, index)
  
  return (json.loads(data[index + var_size: index + var_size + string_size].decode('utf-8')), string_size + var_size)

formatter = {'s': format_string, 'j': format_json}

def unpack(_format: str, data: bytes, index: int):
  cur = index
  total_length = 0
  result = []
  for x in _format:
    (val, length) = formatter[x](data, cur)
    result.append(val)
    total_length += length
  return (result, total_length)