from platforms.vca import VCA
from platforms.constants import ELOS
import pyautogui
import time

LOW_QUALITY, MEDIUM_QUALITY, HIGH_QUALITY, ULTRA_HIGH_QUALITY = range(4)

DEFAULT_QUALITY = ULTRA_HIGH_QUALITY

class Elos(VCA):
  def __init__(self, args, vca=ELOS):
    super().__init__(args, vca)

  def enter_url(self):
    pyautogui.write(self.url)
    pyautogui.hotkey('enter')

  def join_as_guest(self):
    self.guibot_click('elos_sign_in_as_guest.png')

  def enter_guest_data(self):
    time.sleep(2)

    pyautogui.write(self.record)
    pyautogui.hotkey('enter')

    pyautogui.hotkey('tab')
    pyautogui.write(self.record+'@test.com')

    pyautogui.hotkey('enter')
  
  def join_meeting(self):
    time.sleep(3)
    pyautogui.hotkey('enter')
  
  def join_microphone(self):
    time.sleep(3)

    self.guibot_click('elos_join_microphone.png')

    self.guibot_click('elos_activate_audio_echo_test.png')
  
  def low_quality():
    pyautogui.hotkey('enter')
    pyautogui.hotkey('up')
    pyautogui.hotkey('enter')
    time.sleep(3)

  def medium_quaity():
    # Do nothing
    # Put a time sleep here, just because a function can't be empty in python
    time.sleep(0.01)
  
  def high_quality():
    pyautogui.hotkey('enter')
    pyautogui.hotkey('down')
    pyautogui.hotkey('enter')
    time.sleep(3)
  
  def ultra_high_quality():
    pyautogui.hotkey('enter')
    for i in range(2):
      pyautogui.hotkey('down')
      time.sleep(0.05)
    pyautogui.hotkey('enter')
    time.sleep(3)

  def share_camera(self, quality = DEFAULT_QUALITY):
    time.sleep(2)

    self.guibot_click('elos_camera_open_modal.png')
    time.sleep(5)

    # select fake cam from dropdown
    for x in range(2):
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
    for x in range(6):
      pyautogui.hotkey('tab')
      time.sleep(0.05)
    pyautogui.hotkey('enter')

  def quit_call(self):
    # hotkey for opening the three dots dropdown on the top right corner
    pyautogui.hotkey('alt', 'shift', 'O')
    for x in range(7):
      pyautogui.hotkey('down')
    pyautogui.hotkey('enter')