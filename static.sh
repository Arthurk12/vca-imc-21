#!/bin/bash

URL=$1
TIME=$2
TRACE=$3
ROUNDS=${4:-5}

parse_yaml() {
    local prefix=$2
    local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')
    sed -ne "s|^\($s\):|\1|" \
        -e "s|^\($s\)\($w\)$s:$s[\"']\(.*\)[\"']$s\$|\1$fs\2$fs\3|p" \
        -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p"  $1 |
    awk -F$fs '{
        indent = length($1)/2;
        vname[indent] = $2;
        for (i in vname) {if (i > indent) {delete vname[i]}}
        if (length($3) > 0) {
            vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
            printf("%s%s%s=\"%s\"\n", "'$prefix'",vn, $2, $3);
        }
    }'
}

eval $(parse_yaml config/config.yml "CONFIG_")
SHAPER_METHOD=$CONFIG_bash_shaper_method
ROUTER_IP=$CONFIG_bash_shaper_router_ip
ROUTER_USER=$CONFIG_bash_shaper_router_user
SHAPER_INTERFACE=$CONFIG_bash_shaper_interface
CAP_INTERFACE=$CONFIG_bash_captureInterface
VIDEO_FILE=$CONFIG_bash_videoFile
DEV_VIDEO=$CONFIG_bash_devVideo

shape() {
	case $1 in
		start)
				case $SHAPER_METHOD in

					router)
						ssh -n $ROUTER_USER@$ROUTER_IP '/queue simple enable 0'
						ssh -n $ROUTER_USER@$ROUTER_IP "/queue simple set 0 max-limit=${2}k/${3}k burst-limit=${2}k/${3}k"
						;;

					wondershaper)
						sudo wondershaper $SHAPER_INTERFACE $2 $3
						;;

					tc)
						./shaper.sh start $2 $3 0 0 $SHAPER_INTERFACE
						;;
				*)
				esac
				echo "shaping started"
			;;
		
		stop)
			case $SHAPER_METHOD in

				router)
					ssh -n $ROUTER_USER@$ROUTER_IP '/queue simple disable 0'
					;;

				wondershaper)
					sudo wondershaper stop $SHAPER_INTERFACE
					;;

				tc)
					./shaper.sh stop 0 0 0 0 $SHAPER_INTERFACE
					;;
			*)
			esac
			echo "shaping started"
			;;
	*)
	esac

}

term() {
	echo ctrl c pressed!
	tmux kill-session -t 0
	shape stop
	exit
}
trap term SIGINT

echo "---Starting experiment with below config values--"
echo "Shaper method:" $SHAPER_METHOD
echo "Router Ip:" $ROUTER_IP
echo "Router User:" $ROUTER_USER
echo "Shaper Interface:" $SHAPER_INTERFACE
echo "Capture Interface:" $CAP_INTERFACE
echo "Video File:" $VIDEO_FILE
echo "Dev video:" $DEV_VIDEO
echo "--------------------------------------------------"

echo "Reading trace $TRACE"

sleep 1

for i in $(seq 1 $ROUNDS)
do
	while IFS= read -r line
	do
		a=( $line )
		echo "Setting ${a[0]} down and ${a[1]} up"
    if [ ${a[0]} -ne "0" ] && [ ${a[1]} -ne "0" ]; then
			shape start ${a[0]} ${a[1]}
    fi
    tmux new -d "ffmpeg -stream_loop -1 -re -i ${VIDEO_FILE} -vcodec rawvideo -threads 0 -f v4l2 ${DEV_VIDEO}"
		python3 src/test.py -u $URL $TIME -i $CAP_INTERFACE -d ${a[0]} -p ${a[1]} -c $i
		ret=$?
		echo $ret
    tmux kill-session -t 0
		sleep 1
    if [ ${a[0]} -ne "0" ] && [ ${a[1]} -ne "0" ]; then
			shape stop
    fi
		if [ $ret -ne 0 ]; then
			exit 5
		fi
		
	done < $TRACE
done
