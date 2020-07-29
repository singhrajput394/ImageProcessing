import argparse
import os
import cv2
#from VideoGet import VideoGet


from threading import Thread
import cv2

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture("C:\\Users\\abhishes\\Videos\\Captures\\video.mp4")
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):    
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True


video_getter = VideoGet().start()
 
currentframe =0

while True:
	if video_getter.stopped:
		video_getter.stop()
		break

	frame = video_getter.frame
	name = './dataCartoon/frame' + str(currentframe) + '.jpg'
		
	print ('Creating...' + name) 
	currentframe = currentframe + 1
				# writing the extracted images 
	cv2.imwrite(name, frame) 