import sys
from PySide import QtGui,QtCore
import configWindow

class MainWindow(QtGui.QMainWindow):
	
	def __init__(self):
		super(MainWindow,self).__init__()

		self.initUI()

	def initUI(self):
		self.setWindowTitle("PyLip")
		self.setGeometry(100,100,450,350)
		self.show()
		self.config = None 
		self.statusbar = self.statusBar()
		self.statusbar.showMessage('Application under intial stage of development')
		

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		videoMenu = menubar.addMenu('&Video')
		helpMenu = menubar.addMenu('&Help')

		#FileMenu Actions
		videoSourceAction = QtGui.QAction(QtGui.QIcon('vidoesource.png'),'Video &Source',self)
		videoSourceAction.setStatusTip('Choose the video source')

		videoSourceMenu = QtGui.QMenu()
		videoSourceAction.setMenu(videoSourceMenu)
		fileSourceAction = QtGui.QAction(QtGui.QIcon('videofile.png'),'Video &File',self)
		fileSourceAction.triggered.connect(self.fileSourceActionTriggered)

		cameraSourceAction = QtGui.QAction(QtGui.QIcon('webcamera.png'),'&WebCamera',self)
		videoSourceMenu.addAction(fileSourceAction)
		videoSourceMenu.addAction(cameraSourceAction)
		
		configureAction = QtGui.QAction(QtGui.QIcon('configure.png'),'&Configure',self)
		configureAction.setStatusTip('Configure the application')
		configureAction.triggered.connect(self.showConfigureWindow)

		exitAction = QtGui.QAction(QtGui.QIcon('exit.png'),'&Exit',self)
		exitAction.setStatusTip('Exit the application')
		exitAction.triggered.connect(self.close)

		fileMenu.addAction(videoSourceAction)
		fileMenu.addAction(configureAction)
		fileMenu.addAction(exitAction)

		# Video Menu Actions
		playVideoAction = QtGui.QAction(QtGui.QIcon('playvideo.png'),'&PlayVideo',self)
		playVideoAction.setStatusTip('Play from the selected video source')

		startRecordAction = QtGui.QAction(QtGui.QIcon('start.png'),'&Record',self)
		startRecordAction.setStatusTip('records video from selected device')

		stopRecordAction = QtGui.QAction(QtGui.QIcon('stop.png'),'&Stop',self)
		stopRecordAction.setStatusTip('Stop recording')

		generateAudioAction = QtGui.QAction(QtGui.QIcon('generataudio.png'),'&genearateAudio',self)
		generateAudioAction.setStatusTip('Produce the audio')

		videoMenu.addAction(playVideoAction)
		videoMenu.addAction(startRecordAction)
		videoMenu.addAction(stopRecordAction)
		videoMenu.addAction(generateAudioAction)

		#Exit Menu Actions
		docbookAction = QtGui.QAction(QtGui.QIcon('docbook.png'),'&Documentation',self)
		docbookAction.setStatusTip('Show the html documention')
		
		aboutAction = QtGui.QAction(QtGui.QIcon('about.png'),'&About',self)
		aboutAction.setStatusTip('About window')

		helpMenu.addAction(docbookAction)
		helpMenu.addAction(aboutAction)
		
	def fileSourceActionTriggered(self):
		 fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                    '/home')
		 print fname, 'is selected'
		 self.statusbar.showMessage(fname +'is selected as video source')

	def cameraSourceActionTriggered(self):
		self.statusbar.showMessage('Camera is selected to as video source')
		print 'Camera Source Selected'

	def showConfigureWindow(self):
		self.statusbar.showMessage('Opening the configure Window')
		self.config = configWindow.ConfigureWindow()
		self.config.show()
		
def main():
	app = QtGui.QApplication(sys.argv)
	mainWindow = MainWindow()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
