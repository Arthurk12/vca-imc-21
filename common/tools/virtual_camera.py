import subprocess
from common.logger import logger
from common.config import Config

LOG_PREFIX = '[VIRTUAL_CAMERA]'

class VirtualCamera:
	def __init__(self, card_label="My Fake Webcam", exclusive_caps=1):
		self.card_label = card_label
		self.tmux_session_name = card_label
		self.exclusive_caps = exclusive_caps
		self.load_v4l2loopback()

	def load_v4l2loopback(self):
		MODULE = "v4l2loopback"

		# Check if the module is loaded
		result = subprocess.run(['lsmod'], capture_output=True, text=True)
		if MODULE not in result.stdout:
			logger.debug(f'{LOG_PREFIX} {MODULE} is not loaded!')
			# Load the module with specific parameters
			subprocess.run(['sudo', 'modprobe', 'v4l2loopback', f'card_label={self.card_label}', f'exclusive_caps={self.exclusive_caps}'])
		else:
			logger.debug(f'{LOG_PREFIX} is already loaded! wont be loaded again.')

	def start_virtual_camera(self):
		video_file_path=Config.get_virtual_camera_video_file()
		logger.debug(f'{LOG_PREFIX} Starting virtual camera on device {Config.get_virtual_camera_dev_video()} with video file {video_file_path}')

		tmux_cmd = [
			'tmux',
			'new',
			'-d',
			'-s', self.tmux_session_name,
			f'ffmpeg -stream_loop -1 -re -i {video_file_path} -vcodec rawvideo -threads 0 -f v4l2 {Config.get_virtual_camera_dev_video()}'
		]

		result = subprocess.run(tmux_cmd, capture_output=True, text=True)#subprocess.Popen(tmux_cmd, shell=True, start_new_session=True)

		logger.debug(f'{LOG_PREFIX} started tmux session with code {result.returncode}')

	def stop_virtual_camera(self):
		logger.debug(f'{LOG_PREFIX} Stopping virtual camera. Killing tmux session {self.card_label}.')
		tmux_kill_cmd = ['tmux', 'kill-session', '-t', self.tmux_session_name]
		subprocess.run(tmux_kill_cmd)
	
	def restart_video_stream(self):
		# Restart the video stream by sending a signal to ffmpeg
		tmux_send_signal_cmd = ['tmux', 'send-keys', '-t', self.tmux_session_name, 'C-c']
		subprocess.run(tmux_send_signal_cmd)
	
	def __del__(self):
		self.stop_virtual_camera()