from subprocess import Popen
import time
import pyautogui
from common.interactor import Interactor
from common.config import Config
from common.logger import logger

LOG_PREFIX = '[CHROME]'

class Chrome:
  def __init__(self):
    logger.debug(f'{LOG_PREFIX} Constructor')
    self.timeout = 20
    self.interactor = Interactor()
    self.openGoogleCommand = 'google-chrome --check-permission --auto-accept-camera-and-microphone-capture'
    if Config.get_chrome_fake_device():
      self.openGoogleCommand += ' --use-fake-ui-for-media-stream --use-fake-device-for-media-stream'

  def open(self) -> bool:
    logger.debug(f'{LOG_PREFIX} Opening')
    # TODO: return boolean according to the return of Popen
    res = Popen(self.openGoogleCommand, shell=True)
    time.sleep(2)
    return True

  def set_record(self, record: str):
    logger.debug(f'{LOG_PREFIX} Setting record {record}')
    self.record = record
    if Config.get_chrome_internal_logs():
      self.openGoogleCommand += f' --enable-logging=stderr --vmodule=*/webrtc/*=9,*/libjingle/*=9,*=-2 --no-sandbox > {record}.log.txt 2>&1'
    else:
      self.openGoogleCommand += ' > /dev/null 2>&1'

  def open_webrtc_internals(self): 
    logger.debug(f'{LOG_PREFIX} Opening webrtc internals page')
    pyautogui.write('chrome://webrtc-internals')
    pyautogui.hotkey('enter')
    time.sleep(1)
  
  def switch_tab(self):
    logger.debug(f'{LOG_PREFIX} Switching tab')
    pyautogui.hotkey('ctrl', 'tab')

  def open_new_tab(self):
    logger.debug(f'{LOG_PREFIX} Opening new tab')
    pyautogui.hotkey('ctrl', 't')
    time.sleep(1)

  def close_current_tab(self):
    logger.debug(f'{LOG_PREFIX} Closing current tab')
    time.sleep(0.25)
    pyautogui.hotkey('ctrl', 'w')

  def refresh_tab(self):
    logger.debug(f'{LOG_PREFIX} Refreshing tab')
    time.sleep(0.25)
    pyautogui.hotkey('f5')
  
  def collect_webrtc_data(self):
    logger.debug(f'{LOG_PREFIX} Collecting WebRTC data')
    self.interactor.guibot_cliick('create_dump.png', self.timeout)
    self.interactor.guibot_cliick('download.png', self.timeout)
  
  def quit() -> bool:
    logger.debug(f'{LOG_PREFIX} Quitting')
    # TODO: return boolean according to the return of Popen
    res = Popen('killall chrome', shell=True)
    return True

