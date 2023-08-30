import socket
import time
import os
import pyautogui
from browsers.chrome import Chrome
from interactor import Interactor
from results_manager import ResultsManager

HOST = ''
PORT = 12345
chrome = Chrome('', False, False)
interactor = Interactor()
has_started = False

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

def elos_setup():
  time.sleep(3)
  #confirm page reload
  pyautogui.hotkey('enter')
  #wait for the page to load
  time.sleep(10)
  #close audio modal
  interactor.guibot_cliick('close_audio_modal.png', 20)
  #open camera modal
  interactor.guibot_cliick('elos_camera_open_modal.png', 20)
  #wait for the modal to load
  time.sleep(5)
  #9 tabs til "share camera" is selected
  for i in range(9):
    pyautogui.hotkey('tab')
    time.sleep(0.05)
  #click "share camera"
  pyautogui.hotkey('enter')

def meet_setup():
  #wait for the page to load
  time.sleep(10)
  #mute microphone
  interactor.guibot_cliick('meet_mute_mic.png', 20)
  #click to join
  interactor.guibot_cliick('meet_join_now.png', 20)

def start_round_routine(conference_link):
  global has_started
  if has_started:
    print('Received experiment start message when experiment has already started!')
    pass

  has_started = True
  # To reset the webRTC dump
  chrome.refresh_tab()
  if 'live' in conference_link or 'elos' in conference_link:
    elos_setup()
  elif 'meet' in conference_link:
    meet_setup()
  else:
    print(f'Unknown VCA: {conference_link}')

  toggle_recording()

def end_round_routine(experiment_name, record_name):
  global has_started
  if not has_started:
    print('Received experiment end message when experiment has already ended!')
    pass

  has_started = False
  toggle_recording()
  chrome.switch_tab()
  time.sleep(1)
  interactor.guibot_cliick('download.png', 20)
  time.sleep(2)

  results_manager = ResultsManager(experiment_name+'_server')
  results_manager.move_webrtc_dump(record_name)
  results_manager.move_video(record_name)

  chrome.switch_tab()


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
      arguments = received_message.split('#')
      if arguments[0] == 'start':
        conference_link = arguments[1]
        start_round_routine(conference_link)
      elif arguments[0] == 'end':
        experiment_name = arguments[1]
        record_name = arguments[2]
        end_round_routine(experiment_name, record_name)
      else:
        print('received unknown message')
      conn.sendall(data)
  time.sleep(1)
  s.close()
