# Client#1

This code is suposed to run in the client#1 machine of the architecture. When an experiment starts, the client#1 automates all the actions to join and leave the conference, share a fake virtual webcam in the conference and gather metrics about the experiment.

### Dependencies
```sh
sudo apt install python3-dev
sudo apt install python3-tk
# network traffic local interface capture
sudo apt install tshark
# virtual camera device module
sudo apt install v4l2loopback
# generate fake camera stream
sudo apt install ffmpeg
# run virtual camera and experiment in parallel
sudo apt install tmux 
```

### Running
To run the code, use the following command:

```sh
python3 main.py -u <url_to_join_the_conference> -i <interface_to_sniff> -e <experiment_name> -r <rounds_number> <duration_of_each_round>
```
