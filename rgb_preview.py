#!/usr/bin/env python3

import cv2
import depthai as dai
import sys
# Create pipeline
pipeline = dai.Pipeline()

FRAMERATE=60
WIDTH, HEIGHT= 512,512

gst_str = f"appsrc ! videoconvert ! shmsink wait-for-connection=0 socket-path=/tmp/sock5 sync=true shm-size={(WIDTH*HEIGHT*3+128)*2}"
out = cv2.VideoWriter(gst_str, cv2.CAP_GSTREAMER, 0, float(FRAMERATE), (WIDTH, HEIGHT), True)

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutRgb = pipeline.create(dai.node.XLinkOut)

xoutRgb.setStreamName("rgb")

# Properties
camRgb.setPreviewSize(WIDTH, HEIGHT)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
camRgb.setFps(FRAMERATE)

# Linking
camRgb.preview.link(xoutRgb.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    print('Connected cameras: ', device.getConnectedCameras())
    # Print out usb speed
    print('Usb speed: ', device.getUsbSpeed().name)

    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=True)

    while True:
        inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived

        # Retrieve 'bgr' (opencv format) frame
        frame = inRgb.getCvFrame()
        #cv2.imshow("rgb", frame)
        #print(sys.getsizeof(frame))
        
        out.write(frame)
        # if frame.any():
        #     print(len(frame))
            #
        if cv2.waitKey(1) == ord('q'):
            break
