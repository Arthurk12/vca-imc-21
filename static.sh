#!/bin/bash

APP=$1
TIME=$2
CAP_INTERFACE=$3
SHAPE_INTERFACE=$4
TRACE=$5
URL=$6

# echo "Starting virtual cam..."
# sudo modprobe v4l2loopback card_label="My Fake Webcam" exclusive_caps=1
# sh -x ./virtualcam.sh



echo "Reading trace $TRACE"

sleep 1

for i in {1..5}
do
	while IFS= read -r line
	do
		echo $line	
		a=( $line )
		echo "Setting ${a[0]} down and ${a[1]} up"
		./shaper.sh start ${a[0]} ${a[1]} 0 0 $SHAPE_INTERFACE
		python3 test.py $APP $TIME -i $CAP_INTERFACE -id $URL -r ${a[0]}-${a[1]} -c $i
		ret=$?
		echo $ret
		if [ $ret -ne 0 ]; then
			./shaper.sh stop 0 0 0 0 $SHAPE_INTERFACE
			exit 5
		fi
		sleep 1
		./shaper.sh stop 0 0 0 0 $SHAPE_INTERFACE
		
	done < $TRACE
done
