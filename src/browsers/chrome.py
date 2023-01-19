from subprocess import PIPE, Popen
import time
import pyautogui

class Chrome:

  def open():
    res = Popen('google-chrome', shell=True)
    time.sleep(2)
  
  def open_webrtc_internals(): 
    pyautogui.write('chrome://webrtc-internals')
    pyautogui.hotkey('enter')
    time.sleep(1)
  
  def switch_tab():
    pyautogui.hotkey('ctrl', 'tab')

  def open_new_tab():
    pyautogui.hotkey('ctrl', 't')
    time.sleep(1)

  def close_chrome_tab():
    time.sleep(0.25)
    pyautogui.hotkey('ctrl', 'w')

  def __init__(self):
    Chrome.open()