#!/bin/bash

URL=$1
TIME=$2
CAP_INTERFACE=$3
SHAPE_INTERFACE=$4
TRACE=$5

echo "Reading trace $TRACE"

sleep 1

for i in {1..5}
do
	while IFS= read -r line
	do
		echo $line	
		a=( $line )
		echo "Setting ${a[0]} down and ${a[1]} up"
    if [ ${a[0]} -ne "0" ] && [ ${a[1]} -ne "0" ]; then
      sudo wondershaper $SHAPE_INTERFACE ${a[0]} ${a[1]}
    fi
    tmux new -d 'ffmpeg -stream_loop -1 -re -i media/test.mp4 -vcodec rawvideo -threads 0 -f v4l2 /dev/video0'
		python3 src/test.py -u $URL $TIME -i $CAP_INTERFACE -d ${a[0]} -p ${a[1]} -c $i
		ret=$?
		echo $ret
    tmux kill-session -t 0
		sleep 1
    if [ ${a[0]} -ne "0" ] && [ ${a[1]} -ne "0" ]; then
      sudo wondershaper clear $SHAPE_INTERFACE
    fi
		if [ $ret -ne 0 ]; then
			exit 5
		fi
		
	done < $TRACE
done
