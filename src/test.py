from subprocess import PIPE, Popen
from platforms.elos import Elos
import argparse

def launch(args):
	vca = Elos(args)
	vca.enter_url()
	vca.join_as_guest()
	vca.enter_guest_data()
	vca.join_meeting()
	vca.join_microphone()
	vca.share_camera()
	vca.collect_data()
	vca.quit_call()

	del vca


def build_parser():

	parser = argparse.ArgumentParser(
		description='Initiate and capture video call')

	parser.add_argument(
		'vca',
		help="VCA to use"
	)

	parser.add_argument(
		'duration',
		help='Length of call'
	)

	parser.add_argument(
		'-u', '--url',
		default=None,
		action='store',
		help='Meeting ID'
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
