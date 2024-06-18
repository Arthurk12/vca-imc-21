from typing import Protocol

from common.browsers.ibrowser import Ibrowser

class Ivca(Protocol):
  
  def set_browser(self, browser: Ibrowser):
    pass

  def start_browser(self):
    pass

  def enter_url(self):
    pass

  def pre_join_actions(self):
    pass

  def join_meeting(self):
    pass

  def pos_join_actions(self):
    pass

  def share_camera(self):
    pass

  def create_webrtc_filename(self) -> str:
    pass

  def collect_data(self):
    pass

  # def sync_screen_recording(self):
  #   pass

  def quit_call(self):
    pass
