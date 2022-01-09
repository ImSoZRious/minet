from client.client import client

class player_client(client):
  def __init__(self, ip, port):
    super().__init__(ip, port)