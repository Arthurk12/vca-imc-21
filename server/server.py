import socket
import time
import os
import pyautogui
from subprocess import PIPE, Popen
from browsers.chrome import Chrome
from interactor import Interactor

HOST = ''
PORT = 12345
chrome = Chrome('', False, False)
interactor = Interactor()

def file_or_directory_exists(path):
  return os.path.exists(path)

def is_file_empty(file_path):
  return (not os.path.exists(file_path))

def toggle_recording():
  pyautogui.hotkey('ctrl', 'shift', 'alt', 'r')

def initial_actions():
  chrome.open()
  chrome.open_webrtc_internals()
  interactor.guibot_cliick('create_dump.png', 20)
  chrome.open_new_tab()

def start_experiment_routine():
  toggle_recording()

def end_experiment_routine(record_name):
  toggle_recording()
  chrome.switch_tab()
  time.sleep(1)
  interactor.guibot_cliick('download.png', 20)
  time.sleep(2)

  if not file_or_directory_exists(os.path.abspath(os.getcwd())+'/webrtc_server'):
    res = Popen(f'mkdir webrtc_server', shell=True)

  res = Popen(f'mv ~/Downloads/webrtc_internals_dump.txt webrtc_server/{record_name}.json', 
    shell=True)
  chrome.switch_tab()
  # To reset the webRTC dump
  chrome.refresh_tab()


initial_actions()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((HOST, PORT))
  while True:
    s.listen()
    conn, addr = s.accept()
    with conn:
      print(f"connected by {addr}")
      data = conn.recv(1024)
      if not data:
        break
      received_message = data.decode()
      print(f"received message => {received_message}")
      if 'start' in received_message:
        start_experiment_routine()
      else:
        record_name = received_message
        end_experiment_routine(record_name)
      conn.sendall(data)
  time.sleep(1)
  s.close()
