from common.platforms.elos import Elos
from common.platforms.constants import BBB_LOCAL
from common.logger import logger
import pyautogui
import time

LOG_PREFIX = '[BBBLOCALSERVER]'

class BBBLocalServer(Elos):
  def __init__(self, args, round, vca=BBB_LOCAL):
    logger.debug(f'{LOG_PREFIX} Constructor')
    super().__init__(args, round, vca)
  
  def join_as_guest(self):
    logger.debug(f'{LOG_PREFIX} Join as guest')
    time.sleep(1)

  def enter_guest_data(self):
    logger.debug(f'{LOG_PREFIX} Enter guest data')
    time.sleep(2)

    pyautogui.write(self.record)
  
  def join_meeting(self):
    logger.debug(f'{LOG_PREFIX} Enter guest data')
    time.sleep(3)
    pyautogui.hotkey('enter')
  
  def join_microphone(self):
    logger.debug(f'{LOG_PREFIX} Join microphone')

    time.sleep(3)

    self.guibot_click('elos_join_microphone.png')

    self.guibot_click('bbb_confirm_audio_test.png')