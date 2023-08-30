from subprocess import PIPE, Popen
import glob
import os

ROOT_OUTPUT_FOLDER = 'output'
VIDEO_FILE_PREFIX = 'Screencast'

class ResultsManager:

  def __init__(self, experiment_name):
    self.experiment_name = experiment_name
    if not self.file_or_directory_exists(os.path.abspath(os.getcwd())+f'/{ROOT_OUTPUT_FOLDER}'):
      self.create_directory(ROOT_OUTPUT_FOLDER)
    if not self.file_or_directory_exists(os.path.abspath(os.getcwd())+f'/{ROOT_OUTPUT_FOLDER}/{experiment_name}'):
      self.create_directory(f'{ROOT_OUTPUT_FOLDER}/{experiment_name}')

  def file_or_directory_exists(self, path):
    return os.path.exists(path)

  def create_directory(self, path):
    return Popen(f'mkdir {path}', shell=True)

  def move_file(self, org, dest):
    return Popen(f'mv {org} {dest}', shell=True)
  
  def move_webrtc_dump(self, dest_filename):
    if not self.file_or_directory_exists(os.path.abspath(os.getcwd())+f'/{ROOT_OUTPUT_FOLDER}/{self.experiment_name}/webrtc'):
      self.create_directory(f'{ROOT_OUTPUT_FOLDER}/{self.experiment_name}/webrtc')
    return self.move_file('~/Downloads/webrtc_internals_dump.txt', f'{ROOT_OUTPUT_FOLDER}/{self.experiment_name}/webrtc/{dest_filename}.json')
  
  def get_latest_video_file(self):
    absolute_path_home_folder = os.path.expanduser('~')
    list_of_files = glob.glob(f'{absolute_path_home_folder}/Videos/{VIDEO_FILE_PREFIX}*.webm')
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file
  
  def move_video(self, dest_filename):
    if not self.file_or_directory_exists(os.path.abspath(os.getcwd())+f'/{ROOT_OUTPUT_FOLDER}/{self.experiment_name}/videos'):
      self.create_directory(f'{ROOT_OUTPUT_FOLDER}/{self.experiment_name}/videos')
    return self.move_file(f'"{self.get_latest_video_file()}"', f'{ROOT_OUTPUT_FOLDER}/{self.experiment_name}/videos/{dest_filename}.webm')
  
  def get_mtr_path_file(self, dest_filename):
    if not self.file_or_directory_exists(os.path.abspath(os.getcwd())+f'/{ROOT_OUTPUT_FOLDER}/{self.experiment_name}/mtr'):
      self.create_directory(f'{ROOT_OUTPUT_FOLDER}/{self.experiment_name}/mtr')
    return f'{ROOT_OUTPUT_FOLDER}/{self.experiment_name}/mtr/{dest_filename}.mtr'
  
  def get_captures_path_file(self, dest_filename):
    if not self.file_or_directory_exists(os.path.abspath(os.getcwd())+f'/{ROOT_OUTPUT_FOLDER}/{self.experiment_name}/captures'):
      self.create_directory(f'{ROOT_OUTPUT_FOLDER}/{self.experiment_name}/captures')
    return f'{ROOT_OUTPUT_FOLDER}/{self.experiment_name}/captures/{dest_filename}.pcap'

