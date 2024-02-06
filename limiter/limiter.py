## TODO: add readme to this folder explaining how to configure it(shaped interface, scripts)
import csv
import subprocess
import time
import socket

CSV_TRACE = ''
HOST = ''
PORT = 12345

last_applied_constraint = None
seconds_counter = 0

def apply_bandwidth_constraint(constraint_in_bytes_per_second):
  global last_applied_constraint
  if constraint_in_bytes_per_second != last_applied_constraint:
    print(f'Applying constraint: {constraint_in_bytes_per_second} bytes per second')
    apply_constraint_command = f'sudo ./netspeed.sh -l {constraint_in_bytes_per_second}bps'
    subprocess.run(apply_constraint_command, shell=True)

    last_applied_constraint = constraint_in_bytes_per_second

def clear_bandwidth_constraints():
  print('Clearing bandwidth constraints')
  clear_constraints_command = f'sudo ./netspeed.sh -s'
  subprocess.run(clear_constraints_command, shell=True)

def startShaping(max_seconds):
  # Abre o arquivo CSV
  with open(CSV_TRACE, "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    next(reader)

    # Itera sobre as linhas do arquivo
    for row in reader:
      # Obtém o valor da largura de banda
      bandwidth = round(float(row[0]))

      apply_bandwidth_constraint(bandwidth)

      # Aguarda 1 segundo
      time.sleep(1)
      seconds_counter+=1
      if max_seconds and seconds_counter >= max_seconds:
        seconds_counter = 0
        clear_bandwidth_constraints()
        break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((HOST, PORT))
  while True:
    s.listen()
    conn, addr = s.accept()
    with conn:
      print(f'connected by {addr}')
      data = conn.recv(1024)
      if not data:
        break
      received_message = data.decode()
      print(f'received message => {received_message}')
      arguments = received_message.split('#')
      command = arguments[0]
      duration = arguments[1]
      if command == 'start':
        startShaping(duration)
      else:
        print('received unknown message')
      conn.sendall(data)
  time.sleep(1)
  s.close()
