class Config:
  selector = 'app'
  configs = 0
  
  @staticmethod
  def init(settings):
    Config.configs = settings[Config.selector]
  
  def get_log_level():
    return Config.confis['logging']['level']

  def get_receiver_wait_enabled():
    return Config.configs['receiverWait']['enabled']

  def get_receiver_wait_time():
    return Config.configs['receiverWait']['time']
  
  def get_notify_enabled():
    return Config.configs['notify']['enabled']

  def get_notify_destination():
    return Config.configs['notify']['destination']

  def get_virtual_camera_video_file():
    return Config.configs['tools']['virtualCamera']['videoFile']

  def get_virtual_camera_dev_video():
    return Config.configs['tools']['virtualCamera']['devVideo']
  
  def get_shaper_machine_endpoint():
    return Config.configs['shaper']['endpoint']

  def get_shaper_machine_port():
    return Config.configs['shaper']['port']
  
  def get_notify_port():
    return Config.configs['notify']['port']
  
  def get_browsers_configs():
    return Config.configs['browsers']

  def get_chrome_fake_device():
    return Config.get_browsers_configs()['chrome']['fakeDevice']
  
  def get_chrome_internal_logs():
    return Config.get_browsers_configs()['chrome']['internalLogs']
  
  def get_platforms_configs():
    return Config.configs['platforms']

  def get_elos_mtr_enabled():
    return Config.get_platforms_configs()['elos']['mtr']['enabled']

  def get_elos_mtr_endpoint():
    return Config.get_platforms_configs()['elos']['mtr']['endpoint']

  def get_elos_video_quality():
    return Config.get_platforms_configs()['elos']['videoQuality']

  def get_elos_join_microphone():
    return Config.get_platforms_configs()['elos']['joinMicrophone']