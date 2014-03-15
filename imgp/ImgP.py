import cv2
import threading
from PySide import QtGui
class UpdateFrame(threading.Thread):
	def __init__(self,stop_flag,fileName,isCamera,cameraNo,lbl):
		super(UpdateFrame,self).__init__()
		self.stop_flag = stop_flag
		self.fileName = fileName
		self.isCamera = isCamera
		self.cameraNo = cameraNo
		self.label = lbl

	def run(self):
		if self.isCamera == True:
			cap = cv2.VideoCapture(self.cameraNo)
		else:
			cap = cv2.VideoCapture(self.fileName)
		while self.stop_flag:
			ret, frame = cap.read()
			if frame == None:
				print 'Video Source reached end or disconnected'
				break
			d = cv2.cvtColor(frame,cv2.cv.CV_BGR2RGB)
			qimg = QtGui.QImage(d.data,d.shape[1],d.shape[0],QtGui.QImage.Format_RGB888)
			qpm = QtGui.QPixmap.fromImage(qimg)
			self.label.setPixmap(qpm)
			self.label.resize(self.label.sizeHint())
			self.label.repaint()

		cap.release()
