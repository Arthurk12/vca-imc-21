import sys
import csv
import subprocess
import time
import socket
import argparse
from common.logger import logger

LOG_PREFIX = '[LIMITER]'

HOST = ''
PORT = 6666

last_applied_constraint = None
seconds_counter = 0
args = None

def apply_bandwidth_constraint(constraint_in_bits_per_second):
  global last_applied_constraint
  if constraint_in_bits_per_second != last_applied_constraint:
    logger.debug(f'{LOG_PREFIX} Applying constraint: {constraint_in_bits_per_second} bits per second')
    apply_constraint_command = f'sudo ./netspeed.sh -l {constraint_in_bits_per_second}bit'
    subprocess.run(apply_constraint_command, shell=True)

    last_applied_constraint = constraint_in_bits_per_second

def clear_bandwidth_constraints():
  logger.debug(f'{LOG_PREFIX} Clearing bandwidth constraints')
  clear_constraints_command = f'sudo ./netspeed.sh -s'
  subprocess.run(clear_constraints_command, shell=True)

def start_shaping(max_seconds):
  global seconds_counter
  logger.debug(f'{LOG_PREFIX} Called start_shaping()')
  # Abre o arquivo CSV
  with open(args.csv_trace, "r") as csvfile:
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

def build_parser():
  logger.debug(f'{LOG_PREFIX} Parsing arguments')
  parser = argparse.ArgumentParser(
		description='Limit bandwith')

  parser.add_argument(
		'csv_trace',
		help='CSV file with the bandwidth shaping pattern to be applied'
	)
  logger.debug(f'{LOG_PREFIX} Arguments parsed!')
  return parser

def startup():
  global args
  parser = build_parser()
  args = parser.parse_args()

def start():
  clear_bandwidth_constraints()
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    logger.debug(f'{LOG_PREFIX} Listening socket on {HOST}:{PORT}')
    while True:
      s.listen()
      conn, addr = s.accept()
      with conn:
        logger.debug(f'{LOG_PREFIX} Connected by {addr}')
        data = conn.recv(1024)
        if not data:
          break
        received_message = data.decode()
        logger.debug(f'{LOG_PREFIX} Received message => {received_message}')
        arguments = received_message.split('#')
        command = arguments[0]
        duration = int(float(arguments[1]))
        logger.debug(f'{LOG_PREFIX} Identified arguments are command: {command} and duration: {duration}')
        if command == 'start':
          conn.sendall(data)
          start_shaping(duration)
        else:
          logger.error(f'{LOG_PREFIX} Received unknown message!')
    time.sleep(1)
    s.close()

if __name__ == '__main__':
  try:
    startup()
    start()
  except Exception as error:
    logger.error(error)
    quit(-1)
  quit()

