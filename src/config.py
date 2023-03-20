import yaml

class Config:
  selector = 'python'
  configs = 0
  
  @staticmethod
  def init(settings):
    Config.configs = settings[Config.selector]

  def get_mtr_enabled():
    return Config.configs['mtr']['enabled']

  def get_mtr_endpoint():
    return Config.configs['mtr']['endpoint']

  def get_receiver_wait_enabled():
    return Config.configs['receiverWait']['enabled']

  def get_receiver_wait_time():
    return Config.configs['receiverWait']['time']

  def get_video_quality():
    return Config.configs['videoQuality']