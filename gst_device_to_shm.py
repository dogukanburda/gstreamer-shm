import time
import cv2

# Cam properties
fps = 5.
frame_width = 1920
frame_height = 1080
# Create capture
cap = cv2.VideoCapture(0)

# Set camera properties
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
cap.set(cv2.CAP_PROP_FPS, fps)

# Define the gstreamer sink
gst_str = "appsrc ! videoconvert ! shmsink wait-for-connection=1 socket-path=/tmp/foo sync=true  shm-size=10000000"

# Check if cap is open
if cap.isOpened() is not True:
    print ("Cannot open camera. Exiting.")
    quit()

# Create videowriter as a SHM sink
out = cv2.VideoWriter(gst_str, 0, fps, (frame_width, frame_height), True)

# Loop it
while True:
    # Get the frame
    ret, frame = cap.read()
    # Check
    if ret is True:
        # Flip frame
        frame = cv2.flip(frame, 1)
        # Write to SHM
        out.write(frame)
    else:
        print ("Camera error.")
        time.sleep(10)

cap.release()
