from subprocess import PIPE, Popen
from platforms.elos import Elos
from platforms.bbb_local_server import BBBLocalServer
from platforms.meet import Meet
from platforms.constants import ELOS, BBB_LOCAL, MEET
from config import Config
from coordinator import Coordinator
import argparse
import time
import yaml

def infer_vca_from_url(url):
	host = url.split("//")[-1].split("/")[0].split('?')[0].split('.')[0]
	if ELOS in host:
		return ELOS
	elif BBB_LOCAL in host:
		return BBB_LOCAL
	elif MEET in host:
		return MEET
	else:
		return host
	
def is_api(url):
	return 'api' in url

def launch(args):
	vca_type = infer_vca_from_url(args.url)
	if (vca_type == ELOS or 'live' in vca_type):
		vca = Elos(args)
	elif (vca_type == MEET):
		vca = Meet(args)
	else:
		vca = BBBLocalServer(args)
	
	vca.enter_url()
	if Config.get_notify_enabled():
		coordinator = Coordinator(Config.get_notify_destination(), Config.get_notify_port())
		coordinator.notify('#'.join(['start', args.url]))
	if not is_api(args.url):
		#this steps are only needed for non-api links
		vca.join_as_guest()
		vca.enter_guest_data()
		vca.join_meeting()
	vca.close_audio_modal()
	vca.share_camera(Config.get_video_quality())
	vca.collect_data()
	if Config.get_receiver_wait_enabled():
		time.sleep(Config.get_receiver_wait_time())
	elif Config.get_notify_enabled():
		coordinator = Coordinator(Config.get_notify_destination(), Config.get_notify_port())
		coordinator.notify('#'.join(['end',args.experiment,vca.create_webrtc_filename()]))
	vca.quit_call()

	del vca


def build_parser():

	parser = argparse.ArgumentParser(
		description='Initiate and capture video call')

	parser.add_argument(
		'-u', '--url',
		help='Url to join the conference'
	)

	parser.add_argument(
		'duration',
		help='Length of call'
	)

	parser.add_argument(
		'-d', '--download',
		default=None,
		action='store',
		help='Download bandwidth'
	)
	
	parser.add_argument(
		'-p', '--upload',
		default=None,
		action='store',
		help='Upload bandwidth'
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
		'-c', '--counter',
		default=None,
		action='store',
		help='Number of the experiment execution'
	)

	return parser


def load_configs():

	with open('config/config.yml', 'r') as f:
			data = yaml.load(f, Loader=yaml.FullLoader)
			print("settings data: ", data['python'])
			Config.init(data)

def execute():

	parser = build_parser()
	args = parser.parse_args()

	launch(args)


if __name__ == '__main__':
	try:
		load_configs()
		execute()

	except Exception as error:
		print(error)
		res = Popen('killall chrome', shell=True)
		quit(-1)
	quit()
