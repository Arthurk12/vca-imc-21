#!/bin/bash
# WTFPL license
# You might need to change /dev/video2 to something different depending on what hardware you have plugged in
# sudo modprobe v4l2loopback card_label="My Fake Webcam" exclusive_caps=1
# echo "Enter the file path (no spaces):"
# read filepath
echo starting stream...
filename='media/test.mp4'
# ffmpeg -re -stream_loop -1 -i ${filename} -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video2
ffmpeg -stream_loop -1 -re -i ${filename} -vcodec rawvideo -threads 0 -f v4l2 /dev/video2