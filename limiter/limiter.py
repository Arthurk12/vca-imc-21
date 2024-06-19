## TODO: add readme to this folder explaining how to configure it(shaped interface, scripts)
import sys
import csv
import subprocess
import time
import socket
from common.logger import logger

LOG_PREFIX = '[LIMITER]'

HOST = ''
PORT = 6666

last_applied_constraint = None
seconds_counter = 0

if len(sys.argv) < 2 or sys.argv[1] == '-h':
  sys.stdout.write("Usage: %s <trace.csv> \n"%sys.argv[0])
  sys.exit(0)

csv_trace = sys.argv[1]

def apply_bandwidth_constraint(constraint_in_bytes_per_second):
  global last_applied_constraint
  if constraint_in_bytes_per_second != last_applied_constraint:
    logger.debug(f'{LOG_PREFIX} Applying constraint: {constraint_in_bytes_per_second} bytes per second')
    apply_constraint_command = f'sudo ./netspeed.sh -l {constraint_in_bytes_per_second}bps'
    subprocess.run(apply_constraint_command, shell=True)

    last_applied_constraint = constraint_in_bytes_per_second

def clear_bandwidth_constraints():
  logger.debug(f'{LOG_PREFIX} Clearing bandwidth constraints')
  clear_constraints_command = f'sudo ./netspeed.sh -s'
  subprocess.run(clear_constraints_command, shell=True)

def start_shaping(max_seconds):
  global seconds_counter
  logger.debug(f'{LOG_PREFIX} Called start_shaping()')
  # Abre o arquivo CSV
  with open(csv_trace, "r") as csvfile:
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

clear_bandwidth_constraints()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((HOST, PORT))
  logger.debug(f'{LOG_PREFIX} Listening on {HOST} port {PORT}')
  while True:
    s.listen()
    conn, addr = s.accept()
    with conn:
      logger.debug(f'{LOG_PREFIX}connected by {addr}')
      data = conn.recv(1024)
      if not data:
        break
      received_message = data.decode()
      logger.debug(f'{LOG_PREFIX}received message => {received_message}')
      arguments = received_message.split('#')
      command = arguments[0]
      duration = int(float(arguments[1]))
      logger.debug(f'{LOG_PREFIX} Identified arguments are command: {command} and duration: {duration}')
      if command == 'start':
        conn.sendall(data)
        start_shaping(duration)
      else:
        logger.error(f'{LOG_PREFIX} received unknown message!')
  time.sleep(1)
  s.close()
