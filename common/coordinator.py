import socket
from common.logger import logger

LOG_PREFIX = '[COORDINATOR]'

class Coordinator:
  def __init__(self, destination, port):
    self._destination = destination
    self._port = port
  
  def notify(self, message, waitForResponse = True):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      logger.debug(f'{LOG_PREFIX} Connecting to {self._destination} on port {self._port}')
      s.connect((self._destination, self._port))
      logger.debug(f'{LOG_PREFIX} Sending message {message}')
      s.sendall(message.encode())
      if (waitForResponse):
        logger.debug(f'{LOG_PREFIX} Waiting for response message')
        data = s.recv(1024)
        logger.debug(f'{LOG_PREFIX} Received message {data.decode()}')

      s.close()