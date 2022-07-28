#!/bin/bash

APP=$1
TIME=$2
CAP_INTERFACE=$3
SHAPE_INTERFACE=$4
TRACE=$5
URL=$6


echo "Reading trace $TRACE"

sleep 1

for i in {1..5}
do
	while IFS= read -r line
	do
		echo $line	
		a=( $line )
		echo "Setting ${a[1]} down and ${a[2]} up"
		python3 test.py $APP $TIME -i $CAP_INTERFACE -id $URL -r ${a[1]}-${a[2]}
		ret=$?
		echo $ret
		if [ $ret -ne 0 ]; then
			exit 5
		fi
		sleep 1
		
	done < $TRACE
done
