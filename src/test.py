from subprocess import PIPE, Popen
from platforms.elos import Elos
from platforms.bbb_local_server import BBBLocalServer
from platforms.constants import ELOS, BBB_LOCAL
import argparse

def infer_vca_from_url(url):
	host = url.split("//")[-1].split("/")[0].split('?')[0].split('.')[0]
	if ELOS in host:
		return ELOS
	elif BBB_LOCAL in host:
		return BBB_LOCAL
	else:
		return host

def launch(args):
	vca_type = infer_vca_from_url(args.url)
	if (vca_type == ELOS or 'live' in vca_type):
		vca = Elos(args)
	else:
		vca = BBBLocalServer(args)
	
	vca.enter_url()
	if vca_type == ELOS or vca_type == BBB_LOCAL:
		#this steps are only needed for non-api links
		vca.join_as_guest()
		vca.enter_guest_data()
		vca.join_meeting()
	vca.close_audio_modal()
	vca.share_camera()
	vca.collect_data()
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
		'-c', '--counter',
		default=None,
		action='store',
		help='Number of the experiment execution'
	)

	return parser


def execute():

	parser = build_parser()
	args = parser.parse_args()

	launch(args)


if __name__ == '__main__':
	try:
		execute()

	except Exception as error:
		print(error)
		res = Popen('killall chrome', shell=True)
		quit(-1)
	quit()
