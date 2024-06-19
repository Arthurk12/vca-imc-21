from subprocess import PIPE, Popen
import argparse
import time
import yaml
from beepy import beep
from common.platforms.vca_factory import Factory_vca
from common.browsers.chrome import Chrome
from common.config import Config
from common.coordinator import Coordinator
from common.tools.virtual_camera import VirtualCamera
from common.logger import logger


CONFIG_YML = 'config/config.yml'
LOG_PREFIX = '[MAIN]'


def run(args, round):
	logger.debug(f'{LOG_PREFIX} -------- Round {round} --------')
	ivca = Factory_vca.create_vca(args, round)
	ivca.set_browser(Chrome())

	ivca.start_browser()
	
	logger.debug(f'{LOG_PREFIX} Calling enter_url()')
	ivca.enter_url()

	if Config.get_notify_enabled():
		logger.debug(f'{LOG_PREFIX} Creating Coordinator to notify start of round')
		coordinator = Coordinator(Config.get_notify_destination(), Config.get_notify_port())
		coordinator.notify('#'.join(['start', args.url]))

	logger.debug(f'{LOG_PREFIX} Calling pre_join_actions()')
	ivca.pre_join_actions()

	logger.debug(f'{LOG_PREFIX} Calling join_meeting()')
	ivca.join_meeting()
	
	logger.debug(f'{LOG_PREFIX} Calling pos_join_actions()')
	ivca.pos_join_actions()

	logger.debug(f'{LOG_PREFIX} Calling share_camera()')
	ivca.share_camera()

  # Send command to shaper machine to start shaping network
	logger.debug(f'{LOG_PREFIX} Creating Coordinator to notify start of round')
	coordinator = Coordinator(Config.get_shaper_machine_endpoint(), Config.get_shaper_machine_port())
	coordinator.notify('#'.join(['start', args.duration]))
	
	logger.debug(f'{LOG_PREFIX} Calling collect_data()')
	ivca.collect_data()

	if Config.get_receiver_wait_enabled():
		logger.debug(f'{LOG_PREFIX} Waiting for receiver for {Config.get_receiver_wait_time()} ms')
		time.sleep(Config.get_receiver_wait_time())
	elif Config.get_notify_enabled():
		logger.debug(f'{LOG_PREFIX} Creating Coordinator to notify end of round')
		coordinator = Coordinator(Config.get_notify_destination(), Config.get_notify_port())
		coordinator.notify('#'.join(['end', args.experiment, ivca.create_webrtc_filename()]))

	ivca.quit_call()

	del ivca


def build_parser():

	parser = argparse.ArgumentParser(
		description='Initiate and capture video call')

	parser.add_argument(
		'-u', '--url',
		help='Url to join the conference'
	)

	parser.add_argument(
		'duration',
		help='Length of each call'
	)

	parser.add_argument(
		'-i', '--interface',
		default=None,
		action='store',
		help='Interface to capture network traffic'
	)
	
	parser.add_argument(
		'-e', '--experiment',
		default=None,
		action='store',
		help='Name of the experiment'
	)

	parser.add_argument(
		'-r', '--rounds',
		default=1,
		action='store',
		help='Number of rounds of the experiment. It means the expermient will repet x rounds.'
	)

	return parser


def load_configs():
	logger.debug(f'{LOG_PREFIX} Loading configs')
	with open(CONFIG_YML, 'r') as f:
			data = yaml.load(f, Loader=yaml.FullLoader)
			Config.init(data)
	logger.debug(f'{LOG_PREFIX} Configs loaded!')


def execute():
	logger.debug(f'{LOG_PREFIX} Parsing arguments')
	parser = build_parser()
	args = parser.parse_args()
	logger.debug(f'{LOG_PREFIX} Arguments parsed!')

	logger.debug(f'{LOG_PREFIX} ********** Starting experiment: {args.experiment} with {int(float(args.rounds))} rounds **********')
	total_rounds = int(float(args.rounds)) + 1
	for round in range(1, total_rounds, 1):
		virtual_camera = VirtualCamera()
		virtual_camera.start_virtual_camera()
		run(args, round)
		virtual_camera.stop_virtual_camera()
		time.sleep(1)

def play_sound(number):
	if Config.get_sounds_enabled():
		beep(sound=number)


if __name__ == '__main__':
	try:
		logger.debug(f'{LOG_PREFIX} Script startup')
		load_configs()
		execute()
		play_sound(6)

	except Exception as error:
		play_sound(3)
		logger.error(error)
		Chrome.quit()
		quit(-1)
	quit()
