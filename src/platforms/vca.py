from interactor import Interactor
from browsers.chrome import Chrome
from subprocess import PIPE, Popen
from platforms.constants import ELOS
from results_manager import ResultsManager
from config import Config
import time
import os
import pyautogui

class VCA:

  DEFAULT_TIMEOUT = 20

  def enter_url(self):
    pyautogui.write(self.url)
    pyautogui.hotkey('enter')

  def create_record(self, args):
    return f'{args.download}-{args.upload}r{args.counter}';

  def create_webrtc_filename(self):
    return f'{self.vca}-{self.record.split("r")[0]}[{self.counter}]'

  def guibot_click(self, filename):
    self.interactor.guibot_cliick(filename, self.timeout)

  def get_time(self):
    self.ts = int(time.time())

  def is_file_empty(file_path):
    return (not os.path.exists(file_path))
  
  def capture_traffic(self):
    # if not VCA.file_or_directory_exists(os.path.abspath(os.getcwd())+'/captures'):
    #   _ = Popen(f'mkdir captures', shell=True)

    filename = self.results_manager.get_captures_path_file(f'{self.ts}-{self.vca}-{self.record}')
    if Config.get_mtr_enabled():
      self.mtr()
    cmd = f'tshark -i {self.interface} -w {filename} -a duration:{str(self.duration)}'
    res = Popen(cmd, shell=True)
    res.wait()
  
  def mtr(self):
    if ELOS not in self.vca:
      return

    filename = self.results_manager.get_mtr_path_file('{self.vca}-{self.record}')
    
    cmd = f'mtr -w -o"LDRSNBAWVGJMXI" -C -c{str(self.duration)} {Config.get_mtr_endpoint()} > {filename}'
    _ = Popen(cmd, shell=True)
  
  def collect_webrtc_dump(self):
    pyautogui.hotkey('ctrl', 'shift', 'alt', 'r')
    self.guibot_click('create_dump.png')
    self.guibot_click('download.png')

    time.sleep(2)

    self.results_manager.move_webrtc_dump(self.create_webrtc_filename())

    # if not VCA.file_or_directory_exists():
    #   res = Popen(f'mkdir webrtc', shell=True)

    # res = Popen(f'mv ~/Downloads/webrtc_internals_dump.txt webrtc/{self.vca}-{self.record.split("r")[0]}[{self.counter}].json', 
    #   shell=True)

    self.results_manager.move_video(self.create_webrtc_filename())

    # if not VCA.file_or_directory_exists(os.path.abspath(os.getcwd())+'/videos'):
    #   res = Popen(f'mkdir videos', shell=True)

    # res = Popen(f'mv ~/Videos/*.webm videos/{self.vca}-{self.record.split("r")[0]}[{self.counter}].webm', 
    #   shell=True)

    printheader = VCA.is_file_empty(os.path.abspath(os.getcwd())+'/stats.log')

    with open('stats.log', 'a') as f:
      if printheader:
        f.write(f'\n[time]-[vca]-[browser]-[name_of_test]')
      f.write(f'\n{self.ts}-{self.vca}-{self.record}')

    return
  
  def collect_data(self):
    self.get_time()
    self.capture_traffic()
    self.browser.switch_tab()
    self.collect_webrtc_dump()
    self.browser.switch_tab()

  def calculate_timeout(download):
    if(download == 0):
      return VCA.DEFAULT_TIMEOUT
    return ((3000-float(download))/1000)*VCA.DEFAULT_TIMEOUT
  
  def __init__(self, args, vca):
    self.record = self.create_record(args)
    self.interface = args.interface
    self.counter = args.counter
    self.url = args.url
    self.vca = vca
    self.duration = args.duration
    self.timeout = VCA.calculate_timeout(args.download)
    self.results_manager = ResultsManager(args.experiment)
    self.interactor = Interactor()
    self.browser = Chrome(self.record, False, False)
    self.browser.open()
    self.browser.open_webrtc_internals()
    self.browser.open_new_tab()
    pyautogui.hotkey('ctrl', 'shift', 'alt', 'r')
  
  def __del__(self):
    # closes vca tab
    self.browser.close_chrome_tab()
    # closes webrtc internals tab
    self.browser.close_chrome_tab()
