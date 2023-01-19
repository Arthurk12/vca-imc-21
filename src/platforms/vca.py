from interactor import Interactor
from browsers.chrome import Chrome
from subprocess import PIPE, Popen
import time
import os

class VCA:

  DEFAULT_TIMEOUT = 20

  def create_record(self, args):
    return f'{args.download}-{args.upload}';

  def guibot_click(self, filename):
    self.interactor.guibot_cliick(filename, self.timeout)

  def get_time(self):
    self.ts = int(time.time())

  def file_or_directory_exists(path):
    return os.path.exists(path)

  def is_file_empty(file_path):
    return (not os.path.exists(file_path))
  
  def capture_traffic(self):
    if not VCA.file_or_directory_exists(os.path.abspath(os.getcwd())+'/captures'):
      _ = Popen(f'mkdir captures', shell=True)

    filename = f'captures/{self.ts}-{self.vca}-{self.record}.pcap'

    cmd = f'tshark -i {self.interface} -w {filename} -a duration:{str(self.duration)}'
    res = Popen(cmd, shell=True)
    res.wait()
  
  def collect_webrtc_dump(self):
    self.guibot_click('create_dump.png')
    self.guibot_click('download.png')

    time.sleep(2)

    if not VCA.file_or_directory_exists(os.path.abspath(os.getcwd())+'../../webrtc'):
      res = Popen(f'mkdir ../../webrtc', shell=True)

    res = Popen(f'mv ~/Downloads/webrtc_internals_dump.txt ../../webrtc/{self.vca}-{self.record}[{self.counter}].json', 
      shell=True)

    printheader = VCA.is_file_empty(os.path.abspath(os.getcwd())+'/stats.log')

    with open('stats.log', 'a') as f:
      if printheader:
        f.write(f'\n[time]-[vca]-[browser]-[name_of_test]')
      f.write(f'\n{self.ts}-{self.vca}-{self.record}')

    return
  
  def collect_data(self):
    self.get_time()
    self.capture_traffic()
    Chrome.switch_tab()
    self.collect_webrtc_dump()
    Chrome.switch_tab()
  
  def __init__(self, args):
    self.record = self.create_record(args)
    self.interface = args.interface
    self.counter = args.counter
    self.url = args.url
    self.vca = args.vca
    self.duration = args.duration
    self.timeout = (3-float(args.download))*VCA.DEFAULT_TIMEOUT
    self.interactor = Interactor()
    Chrome.open()
    Chrome.open_webrtc_internals()
    Chrome.open_new_tab()
  
  def __del__(self):
    # closes vca tab
    Chrome.close_chrome_tab()
    # closes webrtc internals tab
    Chrome.close_chrome_tab()
