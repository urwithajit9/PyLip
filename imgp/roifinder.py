import numpy as np
import cv2
import glob
import pickle
from collections import deque
import time
class ROIFind:
	def findMeanGrid(self,img):
		a = np.zeros((100,100)) 
		x,y,z = img.shape
		im = cv2.Canny(img,30,200)
		i = 0
		while i * 12< y:
			j = 0
			while j*12 < x:
				a[i][j] = cv2.mean(im[i*12:i*12+12,j*12:j*12+12])[0]
				j = j + 1 
			i = i + 1
		return a[0:i,0:j]
	
	def drawRegion(self,i,j,img):
		im = img
		cv2.rectangle(im,(i*12,j*12),(i*12+ 6 *12, j*12 + 4*12),(255,0,0),2)
		return im
	
	def findMouthRegion(self,img,mask,bias):
		meanGrid = self.findMeanGrid(img)
		x,y = meanGrid.shape
		m,n,error = 0, 0 ,99999
		for i in range(x-4):
			for j in range(y-6):
				er = np.multiply(np.square(np.matrix(meanGrid[i:i+4,j:j+6]) - self.mask),self.bias).mean()
				if er < error :
					m = i
					n = j
					error = er
		match = (m,n)
		return match

	def findRegionUnderEye(self,img):
		

	def getMarkedFrame(self,img):
		match = self.findMouthRegion(img,self.mask,self.bias)
		markedFrame = self.drawRegion(match[0],match[1],img)
		time.sleep(1)
		return markedFrame, match

	def __init__(self):	
		fin = open('../imgp/mouthbox','r')
		self.mask = pickle.load(fin)
		self.bias = [[17,11,6,4,5,7],[12,2,3,2,3,2],[10,1,5,5,4,8],[3,2,10,13,16,18]] 
		self.bias = np.matrix(self.bias)
		fin.close()
		cv2.destroyAllWindows()
