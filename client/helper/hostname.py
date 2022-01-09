import dnspy as dns
import dns.resolver
import socket
import re

def gethostname(ip: str, port: int):
  if re.match('^\d{0,3}.\d{0,3}.\d{0,3}.\d{0,3}$', ip):
    return ip
  hostname = ""
  try:
    hostname = socket.getaddrinfo(ip, port)[0][4][0]
    return hostname
  except:
    pass
  try:
    hostname = str(dns.resolver.resolve('_minecraft._tcp.' + ip, 'SRV')[0].target).rstrip('.')
    hostname = gethostname(hostname, port)
    return hostname
  except:
    pass
  return None