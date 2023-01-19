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
		echo "Setting ${a[0]} down and ${a[1]} up"
		./shaper.sh start ${a[0]} ${a[1]} 0 0 $SHAPE_INTERFACE
		python3 src/test.py $APP $TIME -i $CAP_INTERFACE -u $URL -d ${a[0]} -p ${a[1]} -c $i
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
