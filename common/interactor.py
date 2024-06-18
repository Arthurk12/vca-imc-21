from guibot.guibot import GuiBot

class Interactor:
  prints_folder = 'media'
  
  def __init__(self):
    self.__guibot = GuiBot()
    self.__guibot.add_path(self.prints_folder)

  def guibot_cliick(self, filename, timeout):
    if self.__guibot.exists(filename, timeout):
      self.__guibot.click(filename)
    else:
      raise Exception('Failed to find element: ', filename)