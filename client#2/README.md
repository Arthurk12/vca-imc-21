# Client#2

This code is suposed to run in the client#2 machine of the architecture. When an experiment starts, the client#2 waits for the client#1 message with the conference link to join. Once in the call, the camera is shared and waits for another message from the client#1 notifying that the round has ended. After each round the client#1 waits for the client#2 to gather metrics before starting a new one.

### Dependencies
```sh
# virtual camera device module
sudo apt install v4l2loopback
# generate fake camera stream
sudo apt install ffmpeg
```

### Running
The client#2 is still not fully automatted, specially regarding the virtual camera device setup which has to be done manually before running the code. To set it up, follow the steps:

1. Load modprobe module:
    ```sh
    sudo modprobe v4l2loopback exclusive_caps=1 max_buffers=2
    ```
2. Open a separate terminal and leave the fake webcam stream running:
    ```sh
    ffmpeg -stream_loop -1 -re -i path_to_the_video_file.mp4 -vcodec rawvideo -threads 0 -f v4l2 /dev/video2
    ```
- Whenever you need to unload the v4l2loopback module run: 
    ```sh
    sudo modprobe -r v4l2loopback
    ```

