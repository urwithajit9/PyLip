import sys
from PySide import QtGui
import glob
import pickle

class ConfigureWindow(QtGui.QWidget):

	def __init__(self):
		super(ConfigureWindow,self).__init__()
		self.initUI()

	def initUI(self):
		self.options = {'lang':1,'fannnw':0,'audiofmt':0,'camerano':0}
		self.loadConfiguration()
		self.setWindowTitle('Configuration Window')
		self.setGeometry(130,130,200,200)
		self.show()

		# loading configuraion from file
		#language selection
		self.langLabel = QtGui.QLabel('UI Language ')
		self.langCombobox = QtGui.QComboBox()
		self.langCombobox.addItem('English')
		self.langCombobox.addItem('Tamil')
		self.langCombobox.setCurrentIndex(self.options['lang'])
		
		#FANN network selection
		self.annLabel = QtGui.QLabel('Choose FANN network ')
		self.annCombobox = QtGui.QComboBox()
		for i in glob.glob('../annnw/*'):
			self.annCombobox.addItem(i) 
		self.annCombobox.setCurrentIndex(self.options['fannnw'])

		#Output Audio Format
		self.opaudioLabel = QtGui.QLabel('O/P Audio format ')
		self.opaudioCombobox = QtGui.QComboBox()
		self.opaudioCombobox.addItem('MP3')
		self.opaudioCombobox.addItem('WAV')
		self.opaudioCombobox.addItem('OGG')
		self.opaudioCombobox.setCurrentIndex(self.options['audiofmt'])
	
		#camera to use
		self.cameraLabel =  QtGui.QLabel('Camera to use ')
		self.cameraCombobox = QtGui.QComboBox()
		for i in glob.glob('/sys/class/video4linux/*/name'):
			f = open(i,'r')
			cameraName = f.read()
			self.cameraCombobox.addItem(cameraName)
			f.close()
		self.cameraCombobox.setCurrentIndex(self.options['camerano'])
		#grid initialsation
		self.grid = QtGui.QGridLayout()

		#OK and Cancel Buttons
		self.okButton = QtGui.QPushButton('OK')
		self.okButton.clicked.connect(self.saveConfiguration)
		self.cancelButton = QtGui.QPushButton('Cancel')
		self.cancelButton.clicked.connect(self.close)
		
		#grid defination
		self.grid.addWidget(self.langLabel,0,0)
		self.grid.addWidget(self.langCombobox,0,1)

		self.grid.addWidget(self.annLabel,1,0)
		self.grid.addWidget(self.annCombobox,1,1)

		self.grid.addWidget(self.opaudioLabel,2,0)
		self.grid.addWidget(self.opaudioCombobox,2,1)

		self.grid.addWidget(self.cameraLabel,3,0)
		self.grid.addWidget(self.cameraCombobox,3,1)
		
		self.grid.addWidget(self.okButton,4,0)
		self.grid.addWidget(self.cancelButton,4,1)
		self.setLayout(self.grid)
		
	def saveConfiguration(self):
		fin = open('config.pickle','w')
	#	self.options = {'lang':1,'fannnw':0,'audiofmt':0,'camerano':0}
		self.options['lang'] = self.langCombobox.currentIndex()
		self.options['fannnw'] = self.annCombobox.currentIndex()
		self.options['audiofmt'] = self.opaudioCombobox.currentIndex()
		self.options['camerano'] = self.cameraCombobox.currentIndex()
		pickle.dump(self.options,fin)
		print 'Configuration is saved to file'
		fin.close()
		self.close()
		

	def loadConfiguration(self):
		fin = open('config.pickle','r')
		self.options = pickle.load(fin)
		print self.options
		fin.close()
		
def main():
	app = QtGui.QApplication(sys.argv)
	configWindow = ConfigureWindow()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
