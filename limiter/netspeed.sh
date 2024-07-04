#!/bin/bash 

#USAGE: sudo ./netspeed -l limit_in_kbit -s
usage="sudo $(basename "$0") -l speed_limit -s
  -l speed_limit - speed limit with units (eg. 1mbit, 100kbit, more on \`man tc\`)
  -s - remove all limits
"

# default values
LIMIT=0
STOP=0

#limit values under the LIMIT_LOWER_BOUND will be mapped into an effective limit of 1bit/s which is virtually no connection
# default value is 1000 (1kbit)
LIMIT_LOWER_BOUND=1000 

# hardcoded constats
IFACE=ifb0 # fake interface name which will be used for shaping the traffic
NETFACE=eno1 # interface which in connected to the internet

# shift all required and leave only optional

while getopts ':hl:s' option; do
  case "$option" in
   l) LIMIT=$OPTARG
      ;;
   s) STOP=1
      ;;
   h) echo "$usage"
      exit
      ;;
  esac
done
LIMIT_IN_BITS=$(limitToBits "$LIMIT")
#
# functions used in script
#
function limitExists { # detected by ingress on $NETFACE qdisc
   # -n equals true if non-zero string length
  if [[ -n `tc qdisc show | grep "ingress .* $NETFACE"` ]]
  then
    return 0 # true
  else
    return 1 # false
  fi

}
function ifaceExists {
  # -n equals true if non-zero string length
  if [[ -n `ifconfig -a | sed 's/[ \t].*//;/^\(lo\|\)$/d' | grep $IFACE` ]]
  then
    return 0 # true
  else
    return 1 # false
  fi
}
function ifaceIsUp {
  # -n equals true if non-zero string length
  if [[ -n `ifconfig | sed 's/[ \t].*//;/^\(lo\|\)$/d' | grep $IFACE` ]]
  then
    return 0 # true
  else
    return 1 # false
  fi
}
function limitToBits() {
  local limit=$1
  local limit_value=$(echo "$limit" | sed 's/[a-z]*//')
  local limit_unit=$(echo "$limit" | sed 's/[0-9]*//')

  case "$limit_unit" in
    bit) echo $limit_value;;
    kbit) echo $(($limit_value * 1000));;
    mbit) echo $(($limit_value * 1000000));;
    gbit) echo $(($limit_value * 1000000000));;
    tbit) echo $(($limit_value * 1000000000000));;
    bps) echo $(($limit_value / 8));;
    kbps) echo $(($limit_value * 1000 / 8));;
    mbps) echo $(($limit_value * 1000000 / 8));;
    gbps) echo $(($limit_value * 1000000000 / 8));;
    tbps) echo $(($limit_value * 1000000000000 / 8));;
    *) echo "Unknown unit: $limit_unit"; exit 1;;
  esac
}
function createLimit {
  #3. redirect ingress
  tc qdisc add dev $NETFACE handle ffff: ingress
  tc filter add dev $NETFACE parent ffff: protocol ip u32 match u32 0 0 action mirred egress redirect dev $IFACE

  EFECTIVE_LIMIT=$(($LIMIT_IN_BITS < $LIMIT_LOWER_BOUND ? "1bit" : $LIMIT)) 

  #4. apply egress rules to local inteface (like wlan0)
  tc qdisc add dev $NETFACE root handle 1: htb default 10
  tc class add dev $NETFACE parent 1: classid 1:1 htb rate $EFECTIVE_LIMIT
  tc class add dev $NETFACE parent 1:1 classid 1:10 htb rate $EFECTIVE_LIMIT

  #5. and same for our relaying virtual interfaces (to simulate ingress)
  tc qdisc add dev $IFACE root handle 1: htb default 10
  tc class add dev $IFACE parent 1: classid 1:1 htb rate $EFECTIVE_LIMIT
  tc class add dev $IFACE parent 1:1 classid 1:10 htb rate $EFECTIVE_LIMIT
}
function updateLimit {
  #3. redirect ingress
  tc filter replace dev $NETFACE parent ffff: protocol ip u32 match u32 0 0 action mirred egress redirect dev $IFACE

  EFECTIVE_LIMIT=$(($LIMIT < $LIMIT_LOWER_BOUND ? "1bit" : $LIMIT)) 

  #4. apply egress rules to local inteface (like wlan0)
  tc class replace dev $NETFACE parent 1: classid 1:1 htb rate $EFECTIVE_LIMIT
  tc class replace dev $NETFACE parent 1:1 classid 1:10 htb rate $EFECTIVE_LIMIT

  #5. and same for our relaying virtual interfaces (to simulate ingress)
  tc class replace dev $IFACE parent 1: classid 1:1 htb rate $EFECTIVE_LIMIT
  tc class replace dev $IFACE parent 1:1 classid 1:10 htb rate $EFECTIVE_LIMIT
}
function removeLimit {
  if limitExists ; then
    tc qdisc del dev $NETFACE ingress
    tc qdisc del dev $NETFACE root
    tc qdisc del dev $IFACE root
  fi
  if ifaceIsUp ; then
    ip link set dev $IFACE down
  fi
}

#
# main script
#
if [[ `whoami` != "root" ]]; then
  echo "WARNING: script must be executed with root privileges!"
  echo $usage
  exit 1
fi
if [ $STOP -eq 1 ]; then
  echo "REMOVING limit"
  removeLimit
  echo "limit REMOVED"
elif [ "$LIMIT" != "0" ]; then
  # prepare interface
  if ! ifaceExists ; then
    echo "CREATING $IFACE by modprobe"
    modprobe ifb numifbs=1
    if ! ifaceExists ; then
      echo "creating $IFACE by modprobe FAILED"
      echo "exit with ERROR code 2"
      exit 2
    fi
  fi
  # set interface up
  if ifaceIsUp ; then
    echo "$IFACE is already up"
  else
    echo "set $IFACE up"
    ip link set dev $IFACE up # ( use ifconfig to see results)
    if ifaceIsUp ; then
      echo "$IFACE is up"
    else
      echo "enabling $IFACE by ip link FAILED"
      echo "exit with ERROR code 3"
      exit 3
    fi
  fi

  # create/update limits
  if limitExists ; then
    echo "update limit"
    updateLimit
  else
    echo "create limit"
    createLimit
  fi

  echo "limit CREATED"
  exit 0
else
  echo $usage
fi
