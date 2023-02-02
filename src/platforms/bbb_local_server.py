from platforms.elos import Elos
from platforms.constants import BBB_LOCAL
import pyautogui
import time

class BBBLocalServer(Elos):
  def __init__(self, args, vca=BBB_LOCAL):
    super(Elos, self).__init__(args, vca)
  
  def join_as_guest(self):
    time.sleep(1)

  def enter_guest_data(self):
    time.sleep(2)

    pyautogui.write(self.record)
  
  def join_meeting(self):
    time.sleep(3)
    pyautogui.hotkey('enter')
  
  def join_microphone(self):
    time.sleep(3)

    self.guibot_click('elos_join_microphone.png')

    self.guibot_click('bbb_confirm_audio_test.png')