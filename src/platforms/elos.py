from platforms.vca import VCA
import pyautogui
import time

class Elos(VCA):
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

  def share_camera(self):
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

    # skip to the "share" button
    for x in range(7):
      pyautogui.hotkey('tab')
      time.sleep(0.05)
    pyautogui.hotkey('enter')

  def quit_call(self):
    # hotkey for opening the three dots dropdown on the top right corner
    pyautogui.hotkey('alt', 'shift', 'O')
    for x in range(7):
      pyautogui.hotkey('down')
    pyautogui.hotkey('enter')