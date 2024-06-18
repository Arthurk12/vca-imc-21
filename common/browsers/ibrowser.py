from typing import Protocol

class Ibrowser(Protocol):
  def set_record(self, record: int):
    pass

  def open(self) -> bool:
    pass

  def open_new_tab(self):
    pass

  def open_webrtc_internals(self):
    pass

  def close_current_tab(self):
    pass

  def refresh_tab(self):
    pass

  def switch_tab(self):
    pass

  def write_url(self):
    pass

  def collect_webrtc_data(self):
    pass

  def quit(self) -> bool:
    pass
