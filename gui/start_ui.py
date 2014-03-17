import sys
from PySide import QtGui,QtCore
import configWindow,aboutWindow
from imgp.ImgP import UpdateFrame,WriteFrame
import threading,pickle
class MainWindow(QtGui.QMainWindow):
	
	def __init__(self):
		super(MainWindow,self).__init__()
		self.initUI()
		self.isCamera = False
		self.fname = None
		self.loadConfiguration()

	def initUI(self):
		self.setWindowTitle("PyLip")
		self.setGeometry(100,100,450,350)
		self.show()
		self.config = None 
		self.statusbar = self.statusBar()
		self.statusbar.showMessage('Application under intial stage of development')

		self.imgLabel = QtGui.QLabel(self)
		self.setCentralWidget(self.imgLabel)

		self.menubar = self.menuBar()
		self.fileMenu = self.menubar.addMenu('&File')
		self.videoMenu = self.menubar.addMenu('&Video')
		self.helpMenu = self.menubar.addMenu('&Help')

		#FileMenu Actions
		self.videoSourceAction = QtGui.QAction(QtGui.QIcon('vidoesource.png'),'Video &Source',self)
		self.videoSourceAction.setStatusTip('Choose the video source')

		self.videoSourceMenu = QtGui.QMenu()
		self.videoSourceAction.setMenu(self.videoSourceMenu)
		self.fileSourceAction = QtGui.QAction(QtGui.QIcon('videofile.png'),'Video &File',self)
		self.fileSourceAction.triggered.connect(self.fileSourceActionTriggered)

		self.cameraSourceAction = QtGui.QAction(QtGui.QIcon('webcamera.png'),'&WebCamera',self)
		self.videoSourceMenu.addAction(self.fileSourceAction)
		self.videoSourceMenu.addAction(self.cameraSourceAction)
		self.cameraSourceAction.triggered.connect(self.cameraSourceActionTriggered)
		
		self.configureAction = QtGui.QAction(QtGui.QIcon('configure.png'),'&Configure',self)
		self.configureAction.setStatusTip('Configure the application')
		self.configureAction.triggered.connect(self.showConfigureWindow)

		self.exitAction = QtGui.QAction(QtGui.QIcon('exit.png'),'&Exit',self)
		self.exitAction.setStatusTip('Exit the application')
		self.exitAction.triggered.connect(self.close)

		self.fileMenu.addAction(self.videoSourceAction)
		self.fileMenu.addAction(self.configureAction)
		self.fileMenu.addAction(self.exitAction)

		# Video Menu Actions
		self.playVideoAction = QtGui.QAction(QtGui.QIcon('playvideo.png'),'&PlayVideo',self)
		self.playVideoAction.setStatusTip('Play the video source')
		self.playVideoAction.triggered.connect(self.playVideo)
		
		self.stopVideoAction = QtGui.QAction(QtGui.QIcon('stopvideo.png'),'&StopVideo',self)
		self.stopVideoAction.setStatusTip('Stop Playing Video')
		self.stopVideoAction.setEnabled(False)
		self.stopVideoAction.triggered.connect(self.stopVideo)

		self.startRecordAction = QtGui.QAction(QtGui.QIcon('start.png'),'&Record',self)
		self.startRecordAction.setStatusTip('records video from selected device')
		self.startRecordAction.triggered.connect(self.startRecord)

		self.stopRecordAction = QtGui.QAction(QtGui.QIcon('stop.png'),'&Stop',self)
		self.stopRecordAction.setStatusTip('Stop recording')
		self.stopRecordAction.setEnabled(False)
		self.stopRecordAction.triggered.connect(self.stopRecord)

		self.generateAudioAction = QtGui.QAction(QtGui.QIcon('generataudio.png'),'&genearateAudio',self)
		self.generateAudioAction.setStatusTip('Produce the audio')

		self.videoMenu.addAction(self.playVideoAction)
		self.videoMenu.addAction(self.stopVideoAction)
		self.videoMenu.addAction(self.startRecordAction)
		self.videoMenu.addAction(self.stopRecordAction)
		self.videoMenu.addAction(self.generateAudioAction)

		#Exit Menu Actions
		self.docbookAction = QtGui.QAction(QtGui.QIcon('docbook.png'),'&Documentation',self)
		self.docbookAction.setStatusTip('Show the html documention')
		
		self.aboutAction = QtGui.QAction(QtGui.QIcon('about.png'),'&About',self)
		self.aboutAction.setStatusTip('About window')
		self.aboutAction.triggered.connect(self.showAboutWindow)

		self.helpMenu.addAction(self.docbookAction)
		self.helpMenu.addAction(self.aboutAction)
		self.helpMenu.triggered.connect(self.openHelp)
		
	def fileSourceActionTriggered(self):
		self.isCamera = False
		self.fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/home')
		print self.fname, 'is selected'
		self.statusbar.showMessage(self.fname +'is selected as video source')

	def cameraSourceActionTriggered(self):
		self.isCamera = True
		self.statusbar.showMessage('Camera is selected to as video source')
		print 'Camera Source Selected'

	def showConfigureWindow(self):
		self.statusbar.showMessage('Opening the configure Window')
		self.config = configWindow.ConfigureWindow()
		self.config.show()
	
	def showAboutWindow(self):
		self.statusbar.showMessage('Opening The about Window')
		self.about= aboutWindow.AboutWindow()	
		self.about.show()

	def openHelp(self):
		QtGui.QDesktopServices.openUrl('file://help.html');

	def playVideo(self):	
		self.stop = threading.Event()
		self.stopVideoAction.setEnabled(True)
		self.playVideoAction.setEnabled(False)
		self.startRecordAction.setEnabled(False)
		self.generateAudioAction.setEnabled(False)
		self.updateFrame = UpdateFrame(self.stop,self.fname,self.isCamera,self.options['camerano'],self)
		self.updateFrame.start()

	def stopVideo(self):
		self.stopVideoAction.setEnabled(False)
		self.playVideoAction.setEnabled(True)
		self.updateFrame.stop_flag = False
		self.startRecordAction.setEnabled(True)
		self.generateAudioAction.setEnabled(True)
	
	def startRecord(self):
		self.stop = threading.Event()
		self.playVideoAction.setEnabled(False)
		self.startRecordAction.setEnabled(False)
		self.generateAudioAction.setEnabled(False)
		self.stopRecordAction.setEnabled(True)
		self.fname , ok = QtGui.QInputDialog.getText(self,'File Name','Enter video\'s filename :')
		self.fname = self.fname + '.mpeg'
		if ok == False:
			self.stopRecord()
		else:
			self.writeFrame = WriteFrame(self.stop,self.fname,self.isCamera,self.options['camerano'],self)
			self.writeFrame.start()

	def stopRecord(self):
		self.playVideoAction.setEnabled(True)
		self.startRecordAction.setEnabled(True)
		self.generateAudioAction.setEnabled(True)
		self.stopVideoAction.setEnabled(False)
		self.writeFrame.stop_flag = False


	def updateOneFrame(self,data):
		self.pixmap = QtGui.QPixmap.fromImage(data)
		self.imgLabel.setPixmap(self.pixmap)
		self.imgLabel.resize(self.imgLabel.sizeHint())
		self.imgLabel.repaint()

	def loadConfiguration(self):
		fin = open('config.pickle','r')
		self.options = pickle.load(fin)
		print self.options
		fin.close()

def main():
	app = QtGui.QApplication(sys.argv)
	mainWindow = MainWindow()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
