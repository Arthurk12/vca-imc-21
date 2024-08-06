from subprocess import Popen
from common.platforms.base_vca import base_VCA
from common.platforms.constants import ELOS
from common.config import Config
from common.logger import logger
import pyautogui
import time

LOW_QUALITY = "Low"
MEDIUM_QUALITY = "Medium"
HIGH_QUALITY = "High"
ULTRA_HIGH_QUALITY = "High Definition"

DEFAULT_QUALITY = ULTRA_HIGH_QUALITY

LOG_PREFIX = '[ELOS]'

class Elos(base_VCA):
  def __init__(self, args, round, vca=ELOS):
    logger.debug(f'{LOG_PREFIX} Constructor')
    super().__init__(args, round, vca)
    self.is_api = 'api' in self.url
    self.is_elos = vca == ELOS

  def pre_join_actions(self):
    if not self.is_api:    
      logger.debug(f'{LOG_PREFIX} Is not API. Pre-join actions')
      self.exit_previous_user_data()
      self.join_as_guest()
      self.enter_guest_data()
    else:
      logger.debug(f'{LOG_PREFIX} Is API. No pre-join actions. Passing.')

  def join_meeting(self):
    logger.debug(f'{LOG_PREFIX} Pre-join actions')
    if not self.is_api:
      time.sleep(3)
      pyautogui.hotkey('enter')
    time.sleep(4)
      # self.guibot_click('elos_join_meeting.png')
  
  def pos_join_actions(self):
    logger.debug(f'{LOG_PREFIX} Pos-join actions')
  
  def share_camera(self):
    logger.debug(f'{LOG_PREFIX} Sharing camera with quality: {Config.get_elos_video_quality()}')
    self._share_camera(Config.get_elos_video_quality())
  
  def exit_previous_user_data(self):
    try:
      logger.debug(f'{LOG_PREFIX} Exit previous user data')
      self.guibot_click('elos_wrong_person.png')
    except Exception as e:
      logger.debug(f'{LOG_PREFIX} Apparently there is no previous user data {e}')

  def join_as_guest(self):
    logger.debug(f'{LOG_PREFIX} Joining as guest')
    time.sleep(2)

    self.guibot_click('elos_sign_in_as_guest.png')

  def enter_guest_data(self):
    logger.debug(f'{LOG_PREFIX} Entering guest data')
    time.sleep(2)

    pyautogui.write(self.record)
    pyautogui.hotkey('enter')

    pyautogui.hotkey('tab')
    pyautogui.write(self.record+'@test.com')

    time.sleep(2)

    pyautogui.hotkey('enter')

  def join_microphone(self):
    logger.debug(f'{LOG_PREFIX} Joining microphone')
    time.sleep(3)

    self.guibot_click('elos_join_microphone.png')

    self.guibot_click('elos_activate_audio_echo_test.png')
  
  def close_audio_modal(self):
    logger.debug(f'{LOG_PREFIX} Closing audio modal')
    time.sleep(3)

    self.guibot_click('close_audio_modal.png')
  
  def low_quality():
    logger.debug(f'{LOG_PREFIX} Selecting low quality camera profile')
    pyautogui.hotkey('enter')
    pyautogui.hotkey('up')
    pyautogui.hotkey('enter')
    time.sleep(3)

  def medium_quaity():
    logger.debug(f'{LOG_PREFIX} Selecting medium quality camera profile')
    pass
  
  def high_quality():
    logger.debug(f'{LOG_PREFIX} Selecting high quality camera profile')
    pyautogui.hotkey('enter')
    pyautogui.hotkey('down')
    pyautogui.hotkey('enter')
    time.sleep(3)
  
  def ultra_high_quality():
    logger.debug(f'{LOG_PREFIX} Selecting ultra high quality camera profile')
    pyautogui.hotkey('enter')
    for i in range(2):
      pyautogui.hotkey('down')
      time.sleep(0.05)
    pyautogui.hotkey('enter')
    time.sleep(3)

  def _share_camera(self, quality = DEFAULT_QUALITY):
    time.sleep(2)

    self.guibot_click('elos_camera_open_modal.png')
    time.sleep(5)

    # select fake cam from dropdown
    for x in range(3):
      pyautogui.hotkey('tab')
      time.sleep(0.05)
    pyautogui.hotkey('enter')
    pyautogui.hotkey('down')
    pyautogui.hotkey('enter')
    pyautogui.hotkey('tab')

    if (quality == LOW_QUALITY):
      Elos.low_quality()
    elif(quality == MEDIUM_QUALITY):
      Elos.medium_quaity()
    elif(quality == HIGH_QUALITY):
      Elos.high_quality()
    elif(quality == ULTRA_HIGH_QUALITY):
      Elos.ultra_high_quality()
    else:
      Elos.medium_quaity()

    # skip to the "share" button
    for x in range(4):
      pyautogui.hotkey('tab')
      time.sleep(0.05)
    pyautogui.hotkey('enter')

  def collect_data(self):
    logger.debug(f'{LOG_PREFIX} Starting data collection')
    if self.is_elos and Config.get_elos_mtr_enabled():
      self.mtr()
    
    super().collect_data()

  def mtr(self):
    logger.debug(f'{LOG_PREFIX} Starting mtr test to endpoint {Config.get_elos_mtr_endpoint()}')

    filename = self.results_manager.get_mtr_path_file('{self.vca}-{self.record}')
    
    cmd = f'mtr -w -o"LDRSNBAWVGJMXI" -C -c{str(self.duration)} {Config.get_elos_mtr_endpoint()} > {filename}'
    _ = Popen(cmd, shell=True)

  def open_right_corner_three_dots(self) -> bool:
    # hotkey for opening the three dots dropdown on the top right corner
    pyautogui.hotkey('alt', 'shift', 'O')

  def quit_call(self):
    logger.debug(f'{LOG_PREFIX} Quitting call')
    self.open_right_corner_three_dots()
    for x in range(7):
      pyautogui.hotkey('down')
    pyautogui.hotkey('enter')
