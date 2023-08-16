import socket
import time

HOST = ''
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  while True:
    s.listen()
    conn, addr = s.accept()
    with conn:
      print(f"connected by {addr}")
      data = conn.recv(1024)
      if not data:
        break
      message = data.decode()
      print(f"received message {message}")
      #code that downloads dump webrtc and stops screen recording
      conn.sendall(data)
  time.sleep(1)
  s.close()