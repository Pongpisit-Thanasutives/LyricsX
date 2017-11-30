import os
import cv2
import numpy as np
import cv2.face
import time
import passwdInput
from sys import exit
status = False
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
def canDecide(ls):
	idx=-1
	for i in range(len(ls)):
		if ls[i]==max(ls):
			if idx==-1:idx=i
			else:return False,idx
	return True,idx
def isNet():
	start_time = time.time()
	font=cv2.FONT_HERSHEY_SIMPLEX
	faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	rec_lbph=cv2.face.LBPHFaceRecognizer_create()
	rec_lbph.read('LBPHFaceRecognizer.yml')
	dic={0:'Net',1:'Waii',2:'Unknow'}
	counterLis=[0 for i in range(len(dic))]
	cv2.startWindowThread()		
	cam=cv2.VideoCapture(0)
	while 1:
		if time.time()-start_time>32:break
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
			if rec_lbph.predict(faces[0])[0]==0 or rec_lbph.predict(faces[0])[0]==1:
				if rec_lbph.predict(faces[0])[1]<140:
					cv2.putText(img,dic[rec_lbph.predict(faces[0])[0]],(x,y),font,5,(0,255,0),cv2.LINE_AA)
					counterLis[rec_lbph.predict(faces[0])[0]]+=1
				else:
					cv2.putText(img,'Unknow',(x,y),font,3,(0,255,0),cv2.LINE_AA)
					counterLis[len(counterLis)-1]+=1
			else:
				cv2.putText(img,'Unknow',(x,y),font,3,(0,255,0),cv2.LINE_AA)
				counterLis[len(counterLis)-1]+=1
		cv2.imshow("Face",img)
		k=cv2.waitKey(30) & 0xff
		img=None
		if k==27:
			break
	del rec_lbph
	cam.release()
	cv2.destroyAllWindows()
	if canDecide(counterLis)[0]:
		return canDecide(counterLis)[0],dic[canDecide(counterLis)[1]]
	else:return False,'Unknow'
def getStatus():
	global status
	return status
logginginUserStatus,logginginUser = isNet()
print("--- You are",logginginUser,"---")
if logginginUserStatus==False:
    print("UNAUTHORIZED USER")
    exit()
if passwdInput.getPasswdInput(logginginUser)==False:
    exit()
status=True