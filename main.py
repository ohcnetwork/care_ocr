# Importing all necessary libraries
import cv2
import os
import time
import requests

# Read the video from specified path
cam = cv2.VideoCapture("./data/vid2.mov")

try:

    # creating a folder named data
    if not os.path.exists('data'):
        os.makedirs('data')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

# frame
currentframe = 0
url="http://127.0.0.1:8000/api/predict"
queue = []
while (True):
    time.sleep(10) # take schreenshot every 10 seconds
    # reading from frame
    ret, frame = cam.read()

    if ret:
        # if video is still left continue creating images
        name = './data/images/frame' + str(currentframe) + '.jpg'
        # print('Creating...' + name)

        # # writing the extracted images
        cv2.imwrite(name, frame)
        queue.append(name)
        curr_image = queue.pop(0)
        files={"image":open(curr_image, 'rb')}
        response = requests.post(url=url, files=files)
        # os.remove(curr_image)

        print(response.json())

        # increasing counter so that it will
        # show how many frames are created
        currentframe += 1
    else:
        break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()