from platforms.vca import VCA
from platforms.constants import MEET
import pyautogui
import time

class Meet(VCA):
  def __init__(self, args, vca=MEET):
    super().__init__(args, vca)
  
  def join_as_guest(self):
    pass
  
  def enter_guest_data(self):
    time.sleep(1)

    self.guibot_click('meet_name_input_box.png')
    pyautogui.write(self.record)

  def join_meeting(self):
    time.sleep(2)
    pyautogui.hotkey('enter')
  
  def join_microphone(self):
    print("Meet doesn't require to join microphone explicitly")
    pass

  def close_audio_modal(self):
    print("Meet doesn't require to join microphone explicitly")
    pass

  def share_camera(self, quality):
    print("Meet doesn't require camera to be explicitily share neither has a quality selector")
    pass

  def quit_call(self):
    self.guibot_click('meet_quit_call.png')