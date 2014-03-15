import sys
from PySide import QtGui,QtCore
import configWindow,aboutWindow
from imgp.ImgP import UpdateFrame
import threading,pickle
class MainWindow(QtGui.QMainWindow):
	
	def __init__(self):
		super(MainWindow,self).__init__()
		self.initUI()
		self.isCamera = False
		self.loadConfiguration()

	def initUI(self):
		self.setWindowTitle("PyLip")
		self.setGeometry(100,100,450,350)
		self.show()
		self.config = None 
		self.statusbar = self.statusBar()
		self.statusbar.showMessage('Application under intial stage of development')
		
		self.imgLabel = QtGui.QLabel(self)
		self.imgLabel.text = "Makes me tired. Meet me at hell"
		self.imgLabel.resize(self.imgLabel.sizeHint())
		self.imgLabel.show()
		self.setCentralWidget(self.imgLabel)
		#self.hbox = QtGui.QHBoxLayout(self)
		#self.hbox.addStretch(1)
		#self.hbox.addWidget(self.imgLabel)
		#self.setLayout(self.hbox)

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
		self.playVideoAction.setStatusTip('Play from the selected video source')
		self.playVideoAction.triggered.connect(self.playVideo)

		self.startRecordAction = QtGui.QAction(QtGui.QIcon('start.png'),'&Record',self)
		self.startRecordAction.setStatusTip('records video from selected device')

		self.stopRecordAction = QtGui.QAction(QtGui.QIcon('stop.png'),'&Stop',self)
		self.stopRecordAction.setStatusTip('Stop recording')

		self.generateAudioAction = QtGui.QAction(QtGui.QIcon('generataudio.png'),'&genearateAudio',self)
		self.generateAudioAction.setStatusTip('Produce the audio')

		self.videoMenu.addAction(self.playVideoAction)
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
		updateFrame = UpdateFrame(self.stop,self.fname,self.isCamera,self.options['camerano'],self.imgLabel)
		updateFrame.start()

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
