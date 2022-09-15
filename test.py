from subprocess import PIPE, Popen
from guibot.guibot import GuiBot
from pathlib import Path
import time
import sys
import os
import pyautogui
import argparse

MEET = 'meet'
TEAMS = 'teams'
TEAMS_APP = 'teams-app'
ZOOM = 'zoom'
ZOOM_APP = 'zoom-app'
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

def maximize_window(guibot, vca):
	print('Trying to maximize window!')
	#window is already fullscreen
	if guibot.exists('maximized.png', timeout=5):
		return
	if vca == TEAMS_APP:
		if guibot.exists('teams_maximize.png', timeout=5):
			guibot.click('teams_maximize.png')
	# elif vca == ZOOM_APP:
	else:
		if guibot.exists('maximize.png', timeout=5):
			guibot.click('maximize.png')
		elif guibot.exists('firefox-maximize.png', timeout=5):
			guibot.click('firefox-maximize.png')

def enter_url(args):
	pyautogui.write(args.id)
	pyautogui.hotkey('enter')

def enter_name(args, guibot, vca):
	print('Trying to find field and enter name')
	if vca == MEET:
		time.sleep(2)
	# 	if guibot.exists('meet_enter_name.png', timeout=3):
	# 		guibot.click('meet_enter_name.png')
	elif vca == ELOS:
		time.sleep(2)
	
	pyautogui.write(args.record)
	pyautogui.hotkey('enter')

def share_camera(guibot, vca):
	print('Trying to share camera')
	time.sleep(2)
	if vca == ELOS:
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

def quit_call(guibot, vca):
	if vca == MEET:
		print('aoreuch')
		#
	elif vca == ELOS:
		# guibot_click(guibot, 'elos_three_dots', 20)
		pyautogui.hotkey('alt', 'shift', 'O')
		for x in range(6):
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

	res = Popen(f'mv ~/Downloads/webrtc_internals_dump.txt webrtc/{ts}-{args.vca}-{args.record}.json', 
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

	# maximize_window(guibot, ELOS)

	guibot_click(guibot, 'elos_sign_in_as_guest.png', 20)
	
	enter_name(args, guibot, ELOS)

	pyautogui.hotkey('tab')
	pyautogui.write(args.record+'@test.com')
	#submit name and email
	pyautogui.hotkey('enter')

	time.sleep(1)
	#Join meeting
	pyautogui.hotkey('enter')
	
	time.sleep(3)

	guibot_click(guibot, 'elos_join_microphone.png', 20)

	guibot_click(guibot, 'elos_activate_audio_echo_test.png', 20)

	share_camera(guibot, ELOS)

	ts = int(time.time())

	capture_traffic(args, ts)

	pyautogui.hotkey('ctrl', 'tab')
	
	collect_webrtc(args, ts)

	pyautogui.hotkey('ctrl', 'tab')

	quit_call(guibot, ELOS)
	time.sleep(0.25)
	pyautogui.hotkey('ctrl', 'w')
	time.sleep(0.05)
	pyautogui.hotkey('ctrl', 'w')

	return

def launch_meet(args):

	open_chrome()

	open_webrtc_internals()

	open_new_tab()

	enter_url()

	guibot = GuiBot()
	guibot.add_path('media')

	maximize_window(guibot, MEET)

	enter_name(args, guibot, MEET)

	if guibot.exists('meet_join_now.png', timeout=20):
		guibot.click('meet_join_now.png')

	ts = int(time.time())

	capture_traffic(args, ts)

	time.sleep(1)
	pyautogui.hotkey('ctrl', 'tab')

	
	collect_webrtc(args, ts)

	pyautogui.hotkey('ctrl', 'w')

	if guibot.exists('meet_end_call.png', timeout=5):
		guibot.click('meet_end_call.png')

	if guibot.exists('meet_leave_call.png', timeout=5):
		guibot.click('meet_leave_call.png')

	pyautogui.hotkey('ctrl', 'w')

	return 

def launch_zoom(args):
	guibot = GuiBot()
	guibot.add_path('media')

	open_chrome()

	pyautogui.write(args.id)
	pyautogui.hotkey('enter')


	if args.browser:

		maximize_window(guibot, ZOOM)

		if guibot.exists('zoom_cancel.png', timeout=10):
			guibot.click('zoom_cancel.png')
		
		if guibot.exists('zoom_launch_meeting.png', timeout=10):
			guibot.click('zoom_launch_meeting.png')

		if guibot.exists('zoom_cancel.png', timeout=10):
			guibot.click('zoom_cancel.png')

		if guibot.exists('zoom_join_from_browser.png', timeout=10):
			guibot.click('zoom_join_from_browser.png')

		if guibot.exists('zoom_browser_join.png', timeout=10):
			guibot.click('zoom_browser_join.png')

		time.sleep(15)

		ts = int(time.time())

		capture_traffic(args, ts)

		pyautogui.moveTo(1200, 850, duration=2)

		if guibot.exists('zoom_browser_leave.png', timeout=5):
			guibot.click('zoom_browser_leave.png')

		time.sleep(1)

		pyautogui.hotkey('enter')

		time.sleep(1)

		pyautogui.hotkey('ctrl', 'w')

		with open('stats.log', 'a') as f:
			f.write(f'\n{ts}-{args.vca}-{args.browser}-{args.record}')

		res = Popen('killall "Google Chrome"', shell=True)

	else:

		if guibot.exists('zoom_open_client.png', timeout=10):
			guibot.click('zoom_open_client.png')

		if guibot.exists('zoom_join_with_video.png', timeout=10):
			guibot.click('zoom_join_with_video.png')

		time.sleep(15)

		maximize_window(guibot, ZOOM_APP)

		ts = int(time.time())

		capture_traffic(args, ts)

		pyautogui.moveTo(1200, 850, duration=2)

		if guibot.exists('zoom_client_leave.png', timeout=3):
			guibot.click('zoom_client_leave.png')

		if guibot.exists('zoom_client_leave_meeting.png', timeout=2):
			guibot.click('zoom_client_leave_meeting.png')

		with open('stats.log', 'a') as f:
			f.write(f'\n{ts}-{args.vca}-{args.browser}-{args.record}')

		time.sleep(2)

		pyautogui.hotkey('ctrl', 'w')

		res = Popen('killall "Google Chrome"', shell=True)

	return

def launch_teams(args):

	guibot = GuiBot()
	guibot.add_path('media')

	open_chrome()

	open_webrtc_internals()

	pyautogui.hotkey('ctrl', 't')
	time.sleep(1)

	pyautogui.write(args.id)
	pyautogui.hotkey('enter')

	if args.browser:

		if guibot.exists('teams_cancel.png', timeout=10):
			guibot.click('teams_cancel.png')
		if guibot.exists('teams_browser.png', timeout=5):
			guibot.click('teams_browser.png')
		time.sleep(10)
		if guibot.exists('teams_join_now.png', timeout=20):
			guibot.click('teams_join_now.png')
		maximize_window(guibot, TEAMS)

		pyautogui.moveTo(800, 620, duration=1.5)

		if guibot.exists('teams_camera_off.png', timeout=25):
			guibot.click('teams_camera_off.png')

		ts = int(time.time())

		capture_traffic(args, ts)

		pyautogui.hotkey('ctrl', 'tab')

		collect_webrtc(args, ts)

		pyautogui.hotkey('ctrl', 'w')

		pyautogui.moveTo(800, 620, duration=1.5)

		if guibot.exists('teams_hang_up.png', timeout=5):
			guibot.click('teams_hang_up.png')

		time.sleep(2)

		pyautogui.hotkey('ctrl', 'w')

	else:

		if guibot.exists('teams_launch_client.png', timeout=10):
			guibot.click('teams_launch_client.png')

		if guibot.exists('teams_client_join.png', timeout=10):
			guibot.click('teams_client_join.png')

		if guibot.exists('teams_client_join_now.png', timeout=10):
			guibot.click('teams_client_join_now.png')
		if guibot.exists('teams_client_x.png', timeout=10):
			guibot.click('teams_client_x.png')

		maximize_window(guibot, TEAMS_APP)

		ts = int(time.time())

		capture_traffic(args, ts)

		pyautogui.moveTo(800, 620, duration=1.5)

		if guibot.exists('teams_client_leave', timeout=5):
			guibot.click('teams_client_leave')

		time.sleep(2)

		res = Popen('killall "Google Chrome"', shell=True)

		print("done")

		with open('stats.log', 'a') as f:
			f.write(f'\n{ts}-{args.vca}-{args.browser}-{args.record}')

	res = Popen('killall "Google Chrome"', shell=True)


def launch(args):

	if args.vca == MEET:
		launch_meet(args)
	elif args.vca == ZOOM:
		launch_zoom(args)
	elif args.vca == ELOS:
		launch_elos(args)
	else:
		launch_teams(args)

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
