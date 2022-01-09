def log_ping(data: list):
  print('ping response\'s: ')
  print(str(data[0]['players']['online']) + '/' + str(data[0]['players']['max']))
  print('Players: ' + ', '.join([x['name'][:-2] for x in data[0]['players']['sample']]))

log_mesasge = {b'\x00': log_ping}

def log(packet_id: bytes, data: list):
  log_mesasge[packet_id](data)