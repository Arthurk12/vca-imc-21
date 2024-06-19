# Limiter

This code is suposed to run in the limiter machine of the architecture. This machine should be in network bridge with the client#1. The code relies on the execution of the netspeed.sh script to apply the network constraints.

## Setup
### bridge
To setup the bridge use:
```sh
#create bridge
sudo brctl addbr br0

#add the 2 interfaces to the bridge
sudo brctl addif br0 eno1 enx28ee521ab790

#enable the new bridge interface
sudo ip link set dev br0 up

#assign ip to bridge
sudo dhclient br0
```
(source: https://linuxhint.com/linux_network_bridges_bonds/)

### netspeed.sh
- The netspeed.sh script has to be run as sudo. To do so, you have to add the user to the sudoers list:
    1. Open `/etc/sudoers`
    2. Add the following line:  `<user_name>    ALL=(ALL) PASSWD:ALL`
- Also make sure the script has the required permissions to execute:
    ```sh
    sudo chmod +x ./netspeed.sh
    ```
- To change the interface to which the constraints will be applyied, open the `netspeed.sh` file and edit the `NETFACE` constant to the name of the corresponding interface(it has to be the inteface connected to the gateway/internet)
- To clear any network constraint that may have been left over from the experiment, run:
    ```sh
    sudo ./netspeed.sh -s
    ```
## Running
To run the limiter script, use the command:
```sh
python3 limiter.py <constraints_trace_dataset.csv>
```