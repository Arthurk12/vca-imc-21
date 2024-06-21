from guibot.guibot import GuiBot

PRINTS_FOLDER = '../media/'

class Interactor:
  
  def __init__(self):
    self.__guibot = GuiBot()
    self.__guibot.add_path(PRINTS_FOLDER)

  def guibot_cliick(self, filename, timeout):
    if self.__guibot.exists(filename, timeout):
      self.__guibot.click(filename)
    else:
      raise Exception('Failed to find element: ', filename)