from subprocess import PIPE, Popen
from guibot.guibot import GuiBot
from pathlib import Path
import time
import os
import pyautogui
import argparse

ELOS = 'elos'

def file_or_directory_exists(path):
	return os.path.exists(path)

def is_file_empty(file_path):
	return (not os.path.exists(file_path)) # or os.stat(file_path).st_size == 0

def guibot_click(guibot, filename, timeout):
	if guibot.exists(filename, timeout):
		guibot.click(filename)
	else:
		raise Exception('Failed to find element: ', filename)

def open_chrome():
	res = Popen('google-chrome', shell=True)
	time.sleep(2)

def open_webrtc_internals():
	pyautogui.write('chrome://webrtc-internals')
	pyautogui.hotkey('enter')
	time.sleep(1)

def open_new_tab():
	pyautogui.hotkey('ctrl', 't')
	time.sleep(1)

def maximize_window(guibot):
	if guibot.exists('maximize.png', timeout=5):
		guibot.click('maximize.png')
	elif guibot.exists('firefox-maximize.png', timeout=5):
		guibot.click('firefox-maximize.png')

def enter_url(args):
	pyautogui.write(args.id)
	pyautogui.hotkey('enter')

def enter_name(args):
	print('Trying to find field and enter name')
	time.sleep(2)
	
	pyautogui.write(args.record)
	pyautogui.hotkey('enter')

def share_camera(guibot):
	print('Trying to share camera')
	time.sleep(2)
	guibot_click(guibot, 'elos_camera_open_modal.png', 20)
	time.sleep(5)
	for x in range(2):
		pyautogui.hotkey('tab')
		time.sleep(0.05)
	pyautogui.hotkey('enter')
	pyautogui.hotkey('down')
	pyautogui.hotkey('enter')

	for x in range(7):
		pyautogui.hotkey('tab')
		time.sleep(0.05)
	pyautogui.hotkey('enter')

def quit_call():
	pyautogui.hotkey('alt', 'shift', 'O')
	for x in range(7):
		pyautogui.hotkey('down')
	pyautogui.hotkey('enter')

def collect_webrtc(args, ts):

	guibot = GuiBot()
	guibot.add_path('media')

	if guibot.exists('create_dump.png', timeout=3):
		guibot.click('create_dump.png')

	if guibot.exists('download.png', timeout=3):
		guibot.click('download.png')

	time.sleep(2)

	if not file_or_directory_exists(os.path.abspath(os.getcwd())+'/webrtc'):
		res = Popen(f'mkdir webrtc', shell=True)

	res = Popen(f'mv ~/Downloads/webrtc_internals_dump.txt webrtc/{args.vca}-{args.record}[{args.counter}].json', 
		shell=True)

	printheader = is_file_empty(os.path.abspath(os.getcwd())+'/stats.log')
	print(printheader)
	with open('stats.log', 'a') as f:
		if printheader:
			f.write(f'\n[time]-[vca]-[browser]-[name_of_test]')
		f.write(f'\n{ts}-{args.vca}-{args.record}')

	return

def capture_traffic(args, ts):

	if not file_or_directory_exists(os.path.abspath(os.getcwd())+'/captures'):
		_ = Popen(f'mkdir captures', shell=True)

	filename = f'captures/{ts}-{args.vca}-{args.record}.pcap'

	cmd = f'tshark -i {args.interface} -w {filename} -a duration:{str(args.time)}'
	res = Popen(cmd, shell=True)
	res.wait()

	return

def launch_elos(args):

	open_chrome()

	open_webrtc_internals()

	open_new_tab()

	enter_url(args)

	guibot = GuiBot()
	guibot.add_path('media')

	guibot_click(guibot, 'elos_sign_in_as_guest.png', 20)
	
	enter_name(args)

	pyautogui.hotkey('tab')
	pyautogui.write(args.record+'@test.com')
	#submit name and email
	pyautogui.hotkey('enter')

	time.sleep(3)
	#Join meeting
	pyautogui.hotkey('enter')
	
	time.sleep(3)

	guibot_click(guibot, 'elos_join_microphone.png', 20)

	guibot_click(guibot, 'elos_activate_audio_echo_test.png', 20)

	share_camera(guibot)

	ts = int(time.time())

	capture_traffic(args, ts)

	pyautogui.hotkey('ctrl', 'tab')
	
	collect_webrtc(args, ts)

	pyautogui.hotkey('ctrl', 'tab')

	quit_call()
	time.sleep(0.25)
	pyautogui.hotkey('ctrl', 'w')
	time.sleep(0.05)
	pyautogui.hotkey('ctrl', 'w')

	return

def launch(args):
		launch_elos(args)

def build_parser():

	parser = argparse.ArgumentParser(
		description='Initiate and capture video call')

	parser.add_argument(
		'vca',
		help="VCA to use"
	)

	parser.add_argument(
		'time',
		help='Length of call'
	)

	parser.add_argument(
		'-b', '--browser',
		default=False,
		action='store_true',
		help='Launch call in browser (as opposed to client)'
	)

	parser.add_argument(
		'-id', '--id',
		default=None,
		action='store',
		help='Meeting ID'
	)

	parser.add_argument(
		'-r', '--record',
		default=None,
		action='store',
		help='Name of test to log'
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
