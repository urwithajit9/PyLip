import sys
from PySide import QtGui

class MainWindow(QtGui.QMainWindow):
	
	def __init__(self):
		super(MainWindow,self).__init__()

		self.initUI()

	def initUI(self):
		self.setWindowTitle("PyLip")
		self.setGeometry(100,100,450,350)
		self.show()

		statusbar = self.statusBar()
		statusbar.showMessage('Application under intial stage of development')
		

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		helpMenu = menubar.addMenu('&Help')

		#FileMenu Actions
		videoSourceAction = QtGui.QAction(QtGui.QIcon('vidoesource.png'),'Video &Source',self)
		videoSourceAction.setStatusTip('Choose the video source')
		

		configureAction = QtGui.QAction(QtGui.QIcon('configure.png'),'&Configure',self)
		configureAction.setStatusTip('Configure the application')

		exitAction = QtGui.QAction(QtGui.QIcon('exit.png'),'&Exit',self)
		exitAction.setStatusTip('Exit the application')

		fileMenu.addAction(videoSourceAction)
		fileMenu.addAction(configureAction)
		fileMenu.addAction(exitAction)


		#Exit Menu Actions
		docbookAction = QtGui.QAction(QtGui.QIcon('docbook.png'),'&Documentation',self)
		docbookAction.setStatusTip('Show the html documention')
		
		aboutAction = QtGui.QAction(QtGui.QIcon('about.png'),'&About',self)
		aboutAction.setStatusTip('About window')

		helpMenu.addAction(docbookAction)
		helpMenu.addAction(aboutAction)
		


def main():
	app = QtGui.QApplication(sys.argv)
	mainWindow = MainWindow()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
