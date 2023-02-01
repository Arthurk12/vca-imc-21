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
		sudo wondershaper $SHAPE_INTERFACE ${a[0]} ${a[1]}
		python3 src/test.py $APP $TIME -i $CAP_INTERFACE -u $URL -d ${a[0]} -p ${a[1]} -c $i
		ret=$?
		echo $ret
		sleep 1
		sudo wondershaper clear $SHAPE_INTERFACE
		if [ $ret -ne 0 ]; then
			exit 5
		fi
		
	done < $TRACE
done
