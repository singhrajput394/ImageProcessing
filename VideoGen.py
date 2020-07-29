
import cv2
import numpy as np
import glob

img_array = []
#for filename in glob.glob('C:/Users/abhishes/Source/Repos/HackAthon/HackAthon/selectedData/*.jpg'):
for i in range(0,2026):
    img = cv2.imread("C:\\Users\\abhishes\\Source\\Repos\\HackAthon\\HackAthon\\cartoonSelected\\frame"+ str(i) +".jpg")
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
    print ("Reading img "+ str(i))


out = cv2.VideoWriter('project_050_2026.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()