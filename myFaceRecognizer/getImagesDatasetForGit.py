import os
import cv2
import numpy as np
def cut_faces(image,faces_coord):
	faces=[]
	for (x,y,w,h) in faces_coord:
		w_rm=int(0.2*w/2)
		faces.append(image[y:y+h,x+w_rm:x+w-w_rm])
	return faces
def normalize_intensity(images):
	images_norm=[]
	for image in images:
		is_color=(len(image.shape)==3)	
		if is_color:
			image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		eq=cv2.equalizeHist(image)
		images_norm.append(eq)
	return images_norm
def resize(images,size=(50,50)):
	images_norm=[]
	for image in images:
		if image.shape<size:
			image_norm=cv2.resize(image,size,interpolation=cv2.INTER_AREA)
		else:
			image_norm=cv2.resize(image,size,interpolation=cv2.INTER_CUBIC)
		images_norm.append(image_norm)
	return images_norm
face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
capture=cv2.VideoCapture(0)
os.chdir("C:\\Users\\Pongpisit\\PythonCode\\myPics")
i=0
while 1:
	ret,img=capture.read()
	faces_coord=face_cascade.detectMultiScale(img)
	if len(faces_coord)==1:
		i+=1
		faces=cut_faces(img,faces_coord)
		faces=normalize_intensity(faces)
		faces=resize(faces)
		path='net'+str(i)+'.jpg' 
		cv2.imwrite(path,faces[0])
		print(i)
		cv2.imshow('net',faces[0])
	if i==1000:break
	k=cv2.waitKey(30) & 0xff
	if k==27:break
capture.release()
cv2.destroyAllWindows()