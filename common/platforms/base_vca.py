from common.interactor import Interactor
from common.browsers.ibrowser import Ibrowser
from subprocess import Popen
from common.results_manager import ResultsManager
from common.logger import logger
import time
import os
import pyautogui

LOG_PREFIX='[BASE_VCA]'

class base_VCA:

  DEFAULT_TIMEOUT = 20

  def __init__(self, args, round, vca):
    logger.debug(f'{LOG_PREFIX} Constructor')
    self.interface = args.interface
    self.round = round
    self.url = args.url
    self.vca = vca
    self.duration = args.duration
    self.record = self.create_record(args, round)
    self.timeout = base_VCA.calculate_timeout(0)
    self.results_manager = ResultsManager(args.experiment)
    self.interactor = Interactor()
    self.is_screen_recording = False
    
    logger.debug(f'{LOG_PREFIX} Toggling screen capture. It should be starting now.')
    self.toggle_screen_recording()
  
  def toggle_screen_recording(self):
    logger.debug(f'{LOG_PREFIX} toggling screeen recording')
    time.sleep(1)
    # TODO: move record actions to an specific class
    pyautogui.hotkey('ctrl', 'shift', 'alt', 'r')
    time.sleep(1)
    self.is_screen_recording = not self.is_screen_recording
  
  def sync_screen_recording(self):
    if self.is_screen_recording:
      logger.debug(f'{LOG_PREFIX} screen recording is out of sync. Fixing it')
      self.toggle_screen_recording()

  def set_browser(self, browser: Ibrowser):
    logger.debug(f'{LOG_PREFIX} Setting browser')
    self.browser = browser
    self.browser.set_record(self.record)
  
  def start_browser(self):
    logger.debug(f'{LOG_PREFIX} Starting browser')
    self.browser.open()
    self.browser.open_webrtc_internals()
    self.browser.open_new_tab()

  def enter_url(self):
    logger.debug(f'{LOG_PREFIX} Entering URL')
    pyautogui.write(self.url)
    pyautogui.hotkey('enter')

  def create_record(self, args, round):
    logger.debug(f'{LOG_PREFIX} Creating record: {self.vca}-{args.experiment}-round{round}')
    return f'{self.vca}-{args.experiment}-round{round}'

  def create_webrtc_filename(self) -> str:
    logger.debug(f'{LOG_PREFIX} Creating webrtc filename: {self.record.split("-round")[0]}[{self.round}]')
    return f'{self.record.split("-round")[0]}[{self.round}]'

  def guibot_click(self, filename):
    self.interactor.guibot_cliick(filename, self.timeout)

  def get_time(self):
    self.ts = int(time.time())

  def is_file_empty(file_path):
    return (not os.path.exists(file_path))
  
  def capture_traffic(self):
    logger.debug(f'{LOG_PREFIX} Starting traffic capture')

    filename = self.results_manager.get_captures_path_file(f'{self.ts}-{self.vca}-{self.record}')
    cmd = f'tshark -i {self.interface} -w {filename} -a duration:{str(self.duration)}'
    res = Popen(cmd, shell=True)
    res.wait()
  
  def collect_webrtc_dump(self):
    logger.debug(f'{LOG_PREFIX} Collecting WebRTC dump')
    logger.debug(f'{LOG_PREFIX} Toggling screen capture. It should be stopping now.')
    self.toggle_screen_recording()

    self.browser.collect_webrtc_data()

    time.sleep(2)

    self.results_manager.move_webrtc_dump(self.create_webrtc_filename())

    self.results_manager.move_video(self.create_webrtc_filename())

    printheader = base_VCA.is_file_empty(os.path.abspath(os.getcwd())+'/stats.log')

    with open('stats.log', 'a') as f:
      if printheader:
        f.write(f'\n[time]-[vca]-[browser]-[name_of_test]')
      f.write(f'\n{self.ts}-{self.vca}-{self.record}')

    return
  
  def collect_data(self):
    logger.debug(f'{LOG_PREFIX} Collecting data')
    self.get_time()
    self.capture_traffic()
    self.browser.switch_tab()
    self.collect_webrtc_dump()
    self.browser.switch_tab()

  def calculate_timeout(download):
    if(download == 0):
      logger.debug(f'{LOG_PREFIX} Calculating timeout. Returning default timeout of {base_VCA.DEFAULT_TIMEOUT}')
      return base_VCA.DEFAULT_TIMEOUT
    
    timeout = ((3000-float(download))/1000)*base_VCA.DEFAULT_TIMEOUT
    logger.debug(f'{LOG_PREFIX} Calculating timeout. Returning timeout of {timeout}')
    return timeout
  
  def __del__(self):
    logger.debug(f'{LOG_PREFIX} Deleting')
    # closes vca tab
    self.browser.close_current_tab()
    # closes webrtc internals tab
    self.browser.close_current_tab()
    self.sync_screen_recording()
