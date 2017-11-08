import os
import cv2
import numpy as np
import cv2.face
import time
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
def isNet():
	start_time = time.time()
	condition=False
	font=cv2.FONT_HERSHEY_SIMPLEX
	faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	rec_lbph=cv2.face.LBPHFaceRecognizer_create()
	rec_lbph.read('LBPHFaceRecognizer.yml')
	dic={0:'Net'};count=0;falseCounter=0
	cv2.startWindowThread()
	cam=cv2.VideoCapture(0)
	while 1:
		if time.time()-start_time>90:break
		ret,img=cam.read();
		gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		faces_coord=faceDetect.detectMultiScale(gray)
		if len(faces_coord)==1:
			faces=cut_faces(img,faces_coord)
			faces=normalize_intensity(faces)
			faces=resize(faces)
			x=faces_coord[0][0];y=faces_coord[0][1];w=faces_coord[0][2];h=faces_coord[0][3]
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			# print(rec_lbph.predict(faces[0]))
			if rec_lbph.predict(faces[0])[1]<138:
				cv2.putText(img,dic[rec_lbph.predict(faces[0])[0]],(x,y),font,5,(0,255,0),cv2.LINE_AA)
				count+=1
				if count==20:
					condition=True
					break
			else:
				count=0
				cv2.putText(img,'Unknow',(x,y),font,3,(0,255,0),cv2.LINE_AA)
				falseCounter+=1
				if falseCounter==60:break
		else:
			count=0;falseCounter+=1
			if falseCounter==60:break
		cv2.imshow("Face",img)
		k=cv2.waitKey(30) & 0xff
		if k==27:
			break
	cam.release()
	cv2.destroyAllWindows()
	return condition
# if isNet():
# 	print("YOU ARE NET!")