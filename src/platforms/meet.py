from platforms.base_vca import base_VCA
from platforms.constants import MEET
from logger import logger
import pyautogui
import time

LOG_PREFIX='[MEET]'

class Meet(base_VCA):
  def __init__(self, args, round, vca=MEET):
    logger.debug(f'{LOG_PREFIX} Constructor')
    super().__init__(args, round, vca)

  def enter_guest_data(self):
    logger.debug(f'{LOG_PREFIX} Entering guest data')
    time.sleep(1)

    self.guibot_click('meet_name_input_box.png')
    pyautogui.write(self.record)
  
  def pre_join_actions(self):
    logger.debug(f'{LOG_PREFIX} Pre-join actions.')
    self.enter_guest_data()
    pass

  def join_meeting(self):
    time.sleep(2)
    pyautogui.hotkey('enter')
    time.sleep(2)
  
  def pos_join_actions(self):
    logger.debug(f'{LOG_PREFIX} Pos-join actions.')
    # self.close_camera_dialog()
    pass
  
  def join_microphone(self):
    logger.debug(f'{LOG_PREFIX} no need to join microphone explicitly. Passing.')
    pass

  def close_audio_modal(self):
    logger.debug(f'{LOG_PREFIX} no need to close audio modal. Passing.')
    pass

  def share_camera(self):
    logger.debug(f'{LOG_PREFIX} No need to share camera neither to select its quality. Passing.')
    pass

  def quit_call(self):
    logger.debug(f'{LOG_PREFIX} Quitting call')
    self.guibot_click('meet_quit_call.png')
  
  def close_camera_dialog(self):
    self.guibot_click('meet_close_camera_dialog.png')