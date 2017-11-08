import os
import cv2
import numpy as np
import cv2.face
def collect_dataset(name):
	images=[]
	labels=[]
	labels_dic={}
	labels_dic[0]=name
	for image in os.listdir("C:\\Users\\Pongpisit\\PythonCode\\myPics"):
		images.append(cv2.imread("C:\\Users\\Pongpisit\\PythonCode\\myPics\\"+image,0))
		labels.append(0)
	return (images,np.array(labels),labels_dic)
images,labels,labels_dic=collect_dataset('Net')
rec_eig=cv2.face.EigenFaceRecognizer_create()
rec_eig.train(images,labels)
rec_eig.write('eigenFaceRecognizer.yml')
print("Successfully trained")
# rec_fisher=cv2.face.FisherFaceRecognizer_create()
# rec_fisher.train(images,labels)
rec_lbph=cv2.face.LBPHFaceRecognizer_create()
rec_lbph.train(images,labels)
rec_lbph.write('LBPHFaceRecognizer.yml')
print("Successfully trained")
