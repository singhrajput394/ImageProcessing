# Importing all necessary libraries 
import cv2 
import os 

# Read the video from specified path 
cam = cv2.VideoCapture("C:\\Users\\abhishes\\Videos\\Captures\\Demo_FlowIntegration.mp4") 

try: 
	
	# creating a folder named data 
	if not os.path.exists('data'): 
		os.makedirs('data')
	if not os.path.exists('rejectedData'): 
		os.makedirs('rejectedData')

# if not created then raise error 
except OSError: 
	print ('Error: Creating directory of data') 

# frame 
currentframe = 0
prevFrame = 0

while(True): 
	
	# reading from frame 
	ret,frame = cam.read() 

	if ret: 
		# if video is still left continue creating images 
		name = './data/frame' + str(currentframe) + '.jpg'
		name1 = './rejecteddata/frame' + str(currentframe) + '.jpg'
		print ('Creating...' + name) 
		
		if currentframe != 0:
			img1 = frame
			img2 = prevFrame

			# Convert it to HSV
			img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
			img2_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

			# Calculate the histogram and normalize it
			hist_img1 = cv2.calcHist([img1_hsv], [0,1], None, [180,256], [0,180,0,256])
			cv2.normalize(hist_img1, hist_img1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX);
			hist_img2 = cv2.calcHist([img2_hsv], [0,1], None, [180,256], [0,180,0,256])
			cv2.normalize(hist_img2, hist_img2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX);

			# find the metric value
			metric_val = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_BHATTACHARYYA)
			print ("Metric value:")
			print (metric_val)
			
			if metric_val > 0.1:
				# writing the extracted images 
				cv2.imwrite(name, frame) 
				prevFrame = frame;
			else:
				cv2.imwrite(name1, frame) 
		else:
			cv2.imwrite(name, frame)
			prevFrame = frame

		# increasing counter so that it will 
		# show how many frames are created 
		currentframe += 1
	else: 
		break

	


# Release all space and windows once done 
cam.release() 
cv2.destroyAllWindows() 

