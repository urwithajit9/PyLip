import cv2
import threading,time
from PySide import QtGui,QtCore
class UpdateFrame(QtCore.QThread,QtCore.QObject):
	frameSignal = QtCore.Signal(QtGui.QImage)
	def __init__(self,stop_flag,fileName,isCamera,cameraNo,wui):
		super(UpdateFrame,self).__init__()
		self.wui = wui
		self.qimg = None
		self.stop_flag = stop_flag
		self.fileName = fileName
		self.isCamera = isCamera
		self.cameraNo = cameraNo
		self.frameSignal.connect(self.wui.updateOneFrame)
 
	def run(self):
		if self.isCamera == True:
			cap = cv2.VideoCapture(self.cameraNo)
		else:
			cap = cv2.VideoCapture(self.fileName)
		#cap.set(cv2.cv.CV_CAP_PROP_FPS,25)
		while self.stop_flag:
			if self.isCamera == False:
				time.sleep(0.04)
			ret, frame = cap.read()
			if frame == None:
				print 'Video Source reached end or disconnected'
				self.wui.stopVideo()
				break
			d = cv2.cvtColor(frame,cv2.cv.CV_BGR2RGB)
			self.qimg = QtGui.QImage(d.data,d.shape[1],d.shape[0],QtGui.QImage.Format_RGB888)
			self.frameSignal.emit(self.qimg)
		cap.release()
		self.exit()
		self.exec_()

class WriteFrame(QtCore.QThread,QtCore.QObject):
	frameSignal = QtCore.Signal(QtGui.QImage)
	def __init__(self,stop_flag,fileName,isCamera,cameraNo,wui):
		super(WriteFrame,self).__init__()
		self.wui = wui
		self.qimg = None
		self.stop_flag = stop_flag
		self.fileName = fileName
		self.isCamera = isCamera
		self.cameraNo = cameraNo
		self.frameSignal.connect(self.wui.updateOneFrame)
 
	def run(self):
		if self.isCamera == True:
			cap = cv2.VideoCapture(self.cameraNo)
			ret, frame = cap.read()
			height, width, layers = frame.shape
			vidWriter = cv2.VideoWriter(self.fileName,cv2.cv.CV_FOURCC('P','I','M','1')	,25,(width,height))
			while self.stop_flag:
				print 'reading a video frame'
				ret, frame = cap.read()
				vidWriter.write(frame)
				if frame == None:
					print 'Video Source reached end or disconnected'
					self.wui.stopRecord()
					break
				d = cv2.cvtColor(frame,cv2.cv.CV_BGR2RGB)
				self.qimg = QtGui.QImage(d.data,d.shape[1],d.shape[0],QtGui.QImage.Format_RGB888)
				self.frameSignal.emit(self.qimg)
			cap.release()
			vidWriter.release()
		else:
			print 'video source must be a camera'
			
		self.exit()
		self.exec_()

class ProcessedFrame(QtCore.QThread,QtCore.QObject):
	frameSignal = QtCore.Signal(QtGui.QImage)
	def __init__(self,stop_flag,fileName,isCamera,cameraNo,wui):
		super(ProcessedFrame,self).__init__()
		self.wui = wui
		self.qimg = None
		self.stop_flag = stop_flag
		self.fileName = fileName
		self.isCamera = isCamera
		self.cameraNo = cameraNo
		self.frameSignal.connect(self.wui.updateOneFrame)
 
	def run(self):
		if self.isCamera == True:
			cap = cv2.VideoCapture(self.cameraNo)
		else:
			cap = cv2.VideoCapture(self.fileName)
		#cap.set(cv2.cv.CV_CAP_PROP_FPS,25)
		while self.stop_flag:
			ret, frame = cap.read()
			if frame == None:
				print 'Video Source reached end or disconnected'
				self.wui.stopVideo()
				break
			d = cv2.cvtColor(frame,cv2.cv.CV_BGR2RGB)
			self.qimg = QtGui.QImage(d.data,d.shape[1],d.shape[0],QtGui.QImage.Format_RGB888)
			self.frameSignal.emit(self.qimg)
		cap.release()
		self.exit()
		self.exec_()

