import socket
import time
import os
import pyautogui
import yaml
from common.config import Config
from common.browsers.chrome import Chrome
from common.interactor import Interactor
from common.results_manager import ResultsManager
from common.tools.virtual_camera import VirtualCamera
from common.logger import logger

CONFIG_YML = '../config/config.yml'
LOG_PREFIX = '[SERVER]'

HOST = ''
PORT = 12345
chrome = None
interactor = None
has_started = False
virtual_camera = None

def toggle_recording():
  logger.debug(f'{LOG_PREFIX} Called toggle_reccording()')
  pyautogui.hotkey('ctrl', 'shift', 'alt', 'r')

def load_configs():
  logger.debug(f'{LOG_PREFIX} Loading configs')
  with open(CONFIG_YML, 'r') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    Config.init(data)
    logger.debug(f'{LOG_PREFIX} Configs loaded!')

def startup():
  global virtual_camera
  global chrome
  global interactor
  logger.debug(f'{LOG_PREFIX} Script startup')
  load_configs()

  virtual_camera = VirtualCamera()
  virtual_camera.start_virtual_camera()


  chrome = Chrome()
  interactor = Interactor()
  chrome.open()
  chrome.open_webrtc_internals()
  interactor.guibot_cliick('create_dump.png', 20)
  chrome.open_new_tab()

def elos_setup():
  logger.info(f'{LOG_PREFIX} Called elos_setup()')
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
  for i in range(8):
    pyautogui.hotkey('tab')
    time.sleep(0.05)
  #click "share camera"
  pyautogui.hotkey('enter')

def meet_setup():
  logger.info(f'{LOG_PREFIX} Called meet_setup()')
  #wait for the page to load
  time.sleep(10)
  #mute microphone
  interactor.guibot_cliick('meet_mute_mic.png', 20)
  #click to join
  interactor.guibot_cliick('meet_join_now.png', 20)

def start_round_routine(conference_link):
  global has_started
  global chrome
  logger.debug(f'{LOG_PREFIX} Called start_round_routine()')
  if has_started:
    logger.warn(f'{LOG_PREFIX} Received experiment start message when experiment has already started!')
    pass

  time.sleep(1)

  has_started = True
  # To reset the webRTC dump
  chrome.refresh_tab()
  if 'live' in conference_link or 'elos' in conference_link:
    elos_setup()
  elif 'meet' in conference_link:
    meet_setup()
  else:
    logger.error(f'{LOG_PREFIX} Unknown VCA: {conference_link}')

  toggle_recording()

def end_round_routine(experiment_name, record_name):
  global has_started
  global chrome
  logger.debug(f'{LOG_PREFIX} Called end_round_routine()')
  if not has_started:
    logger.warn(f'{LOG_PREFIX} Received experiment end message when experiment has already ended!')
    pass

  has_started = False
  toggle_recording()
  chrome.switch_tab()
  time.sleep(1)
  interactor.guibot_cliick('download.png', 20)
  time.sleep(2)

  results_manager = ResultsManager(experiment_name+'_client#2')
  results_manager.move_webrtc_dump(record_name)
  results_manager.move_video(record_name)

  chrome.switch_tab()
  virtual_camera.stop_virtual_camera()


def execute():
  logger.debug(f'{LOG_PREFIX} Called execute()')
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    logger.debug(f'{LOG_PREFIX} Listening socket on {HOST}:{PORT} waiting for conference link')
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
        if arguments[0] == 'start':
          conference_link = arguments[1]
          logger.debug(f'{LOG_PREFIX} Identified START message with conference link: {conference_link}')
          start_round_routine(conference_link)
        elif arguments[0] == 'end':
          experiment_name = arguments[1]
          record_name = arguments[2]
          logger.debug(f'{LOG_PREFIX} Identified END message with experiment name: {experiment_name} and record name: {record_name}')
          end_round_routine(experiment_name, record_name)
        else:
          logger.warn(f'{LOG_PREFIX} Received unknown message!')
        conn.sendall(data)
    time.sleep(1)
    s.close()

if __name__ == '__main__':
  try:
    startup()
    execute()
  except Exception as error:
    logger.error(error)
    Chrome.quit()
    quit(-1)
  quit()