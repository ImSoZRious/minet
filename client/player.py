import client.client as client

class player:
  def __init__(self, player_name, ip, port):
    self.client = client.client(ip, port)
    self.player_name = player_name
    self.client.login(player_name)

  def send(self, data):
    self.client.send(data)

  def exit(self):
    self.client.close()