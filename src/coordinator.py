import socket

class Coordinator:
  def __init__(self, destination, port):
    self._destination = destination
    self._port = port
  
  def notify(self, message, waitForResponse = True):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      print(f"Connecting to {self._destination} on port {self._port}")
      s.connect((self._destination, self._port))
      s.sendall(message.encode())
      if (waitForResponse):
        data = s.recv(1024)
        print(f"Received message {data.decode()}")

      s.close()