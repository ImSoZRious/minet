import client.helper.varInt as varInt

def mstr(s: str):
  return varInt.write(len(s)) + s.encode()