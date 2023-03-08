from subprocess import PIPE, Popen
import time
import pyautogui

class Chrome:

  def open(self):
    res = Popen(self.openGoogleCommand, shell=True)
    time.sleep(2)
  
  def open_webrtc_internals(self): 
    pyautogui.write('chrome://webrtc-internals')
    pyautogui.hotkey('enter')
    time.sleep(1)
  
  def switch_tab(self):
    pyautogui.hotkey('ctrl', 'tab')

  def open_new_tab(self):
    pyautogui.hotkey('ctrl', 't')
    time.sleep(1)

  def close_chrome_tab(self):
    time.sleep(0.25)
    pyautogui.hotkey('ctrl', 'w')

  def __init__(self, record, logsEnabled, fakeDevice):
    self.openGoogleCommand = 'google-chrome --check-permission'
    if fakeDevice:
      self.openGoogleCommand += ' --use-fake-ui-for-media-stream --use-fake-device-for-media-stream'
    if logsEnabled:
      self.openGoogleCommand += f' --enable-logging=stderr --vmodule=*/webrtc/*=9,*/libjingle/*=9,*=-2 --no-sandbox > {record}.log.txt 2>&1'