
# Importing all necessary libraries 
import cv2 
import os 

# Read the video from specified path 
cam = cv2.VideoCapture("C:\\Users\\abhishes\\Videos\\Captures\\Demo1.mp4") 

try: 
	
	# creating a folder named data 
	if not os.path.exists('data'): 
		os.makedirs('data')
	if not os.path.exists('rejectedData'): 
		os.makedirs('rejectedData')
	if not os.path.exists('selectedData'): 
		os.makedirs('selectedData')

# if not created then raise error 
except OSError: 
	print ('Error: Creating directory of data') 

# frame 
currentframe = 0
prevFrame = 0
prevNum = 0
print ("frames generation...")
while(True): 
	
	# reading from frame 
	ret,frame = cam.read() 

	if ret: 
		# if video is still left continue creating images 
		name = './dataCartoon/frame' + str(currentframe) + '.jpg'
		print ('Creating...' + name) 
		cv2.imwrite(name, frame) 				

		# increasing counter so that it will 
		# show how many frames are created 
		currentframe += 1
	else: 
		break

# Release all space and windows once done 
cam.release() 
cv2.destroyAllWindows() 

totalframes = currentframe
selectCounter = 0
keyFrames = []
keyFrames.append(0);

print ("Key frames selection...")
for i in range(1, totalframes):
	img1 = cv2.imread("C:\\Users\\abhishes\\Source\\Repos\\HackAthon\\HackAthon\\dataCartoon\\frame" + str(i) + ".jpg")
	img2 = cv2.imread("C:\\Users\\abhishes\\Source\\Repos\\HackAthon\\HackAthon\\dataCartoon\\frame" + str(prevFrame) + ".jpg")
		
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

	# 0.050 gives 184 frames, 12 sec video
	if metric_val >= 0.050:
		#cv2.imwrite(name, img1)
		prevFrame = i	
		keyFrames.append(i)
		print ("Selected frame: " + str(i))

name = './cartoonSelected/frame0.jpg'
img1 = cv2.imread("C:\\Users\\abhishes\\Source\\Repos\\HackAthon\\HackAthon\\dataCartoon\\frame0.jpg")
selectCounter = selectCounter + 1
prevIndex = keyFrames[0]
cv2.imwrite(name, img1)

print ("Select adjacent frames...")
for i in range(1, len(keyFrames)):
	index = keyFrames[i]
	print ("keyframe " + str(index))
	if ((index - prevIndex) > 70):
		print ("not adding adjacent")
	elif ((index - prevIndex) > 30):
		for j in range(prevIndex+1, prevIndex+12):
			print ("keyframe adjacent" + str(j))
			name = './cartoonSelected/frame' + str(selectCounter) +'.jpg'
			selectCounter = selectCounter + 1
			img1 = cv2.imread("C:\\Users\\abhishes\\Source\\Repos\\HackAthon\\HackAthon\\dataCartoon\\frame"+str(j)+".jpg")
			cv2.imwrite(name, img1)
	elif ((index - prevIndex) > 20):
		for j in range(prevIndex+1, prevIndex+8):
			print ("keyframe adjacent" + str(j))
			name = './cartoonSelected/frame' + str(selectCounter) +'.jpg'
			selectCounter = selectCounter + 1
			img1 = cv2.imread("C:\\Users\\abhishes\\Source\\Repos\\HackAthon\\HackAthon\\dataCartoon\\frame"+str(j)+".jpg")
			cv2.imwrite(name, img1)
	elif ((index - prevIndex) > 10):
		for j in range(prevIndex+1, prevIndex+7):
			print ("keyframe adjacent" + str(j))
			name = './cartoonSelected/frame' + str(selectCounter) +'.jpg'
			selectCounter = selectCounter + 1
			img1 = cv2.imread("C:\\Users\\abhishes\\Source\\Repos\\HackAthon\\HackAthon\\dataCartoon\\frame"+str(j)+".jpg")
			cv2.imwrite(name, img1)
	elif ((index - prevIndex) > 5):
		for j in range(prevIndex+1, prevIndex+6):
			print ("keyframe adjacent" + str(j))
			name = './cartoonSelected/frame' + str(selectCounter) +'.jpg'
			selectCounter = selectCounter + 1
			img1 = cv2.imread("C:\\Users\\abhishes\\Source\\Repos\\HackAthon\\HackAthon\\dataCartoon\\frame"+str(j)+".jpg")
			cv2.imwrite(name, img1)
	else:
		for j in range(prevIndex+1, (index - prevIndex)):
			print ("keyframe adjacent" + str(j))
			name = './cartoonSelected/frame' + str(selectCounter) +'.jpg'
			selectCounter = selectCounter + 1
			img1 = cv2.imread("C:\\Users\\abhishes\\Source\\Repos\\HackAthon\\HackAthon\\dataCartoon\\frame"+str(j)+".jpg")
			cv2.imwrite(name, img1)
	name = './cartoonSelected/frame' + str(selectCounter) +'.jpg'
	selectCounter = selectCounter + 1
	img1 = cv2.imread("C:\\Users\\abhishes\\Source\\Repos\\HackAthon\\HackAthon\\dataCartoon\\frame"+str(index)+".jpg")
	cv2.imwrite(name, img1)

	prevIndex = index
	


