import cv2

# Load the images
img1 = cv2.imread('C:\\Users\\abhishes\\Videos\\Captures\\frame4096.jpg')
img2 = cv2.imread('C:\\Users\\abhishes\\Videos\\Captures\\frame4299.jpg')

#img1 = cv2.imread('C:\\Users\\abhishes\\Videos\\Captures\\test.png')
#img2 = cv2.imread('C:\\Users\\abhishes\\Videos\\Captures\\Flow_Run2.png')

# Convert it to HSV
img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
img2_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

# Calculate the histogram and normalize it
hist_img1 = cv2.calcHist([img1_hsv], [0,1], None, [180,256], [0,180,0,256])
cv2.normalize(hist_img1, hist_img1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX);
hist_img2 = cv2.calcHist([img2_hsv], [0,1], None, [180,256], [0,180,0,256])
cv2.normalize(hist_img2, hist_img2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX);

# find the metric value
metric_val = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CORREL)
metric_val1 = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CHISQR)
metric_val2 = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_INTERSECT)
metric_val3 = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_BHATTACHARYYA)
print (metric_val);
print (metric_val1);
print (metric_val2);
print (metric_val3);
