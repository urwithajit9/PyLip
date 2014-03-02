import sys
from PySide import QtGui
import glob

class ConfigureWindow(QtGui.QWidget):

	def __init__(self):
		super(ConfigureWindow,self).__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle('Configuration Window')
		self.setGeometry(130,130,200,200)
		self.show()
		#language selection
		langLabel = QtGui.QLabel('UI Language ')
		langCombobox = QtGui.QComboBox()
		langCombobox.addItem('English')
		langCombobox.addItem('Tamil')
		
		#FANN network selection
		annLabel = QtGui.QLabel('Choose FANN network ')
		annCombobox = QtGui.QComboBox()
		for i in glob.glob('../annnw/*'):
			annCombobox.addItem(i) 

		#Outpu Audio Format
		opaudioLabel = QtGui.QLabel('O/P Audio format ')
		opaudioCombobox = QtGui.QComboBox()
		opaudioCombobox.addItem('MP3')
		opaudioCombobox.addItem('WAV')
		opaudioCombobox.addItem('OGG')
	
		#camera to use
		cameraLabel =  QtGui.QLabel('Camera to use ')
		cameraCombobox = QtGui.QComboBox()
		for i in glob.glob('/sys/class/video4linux/*/name'):
			f = open(i,'r')
			cameraName = f.read()
			cameraCombobox.addItem(cameraName)
			f.close()
		#grid initialsation
		self.grid = QtGui.QGridLayout()

		#OK and Cancel Buttons
		okButton = QtGui.QPushButton('OK')
		cancelButton = QtGui.QPushButton('Cancel')
		
		#grid defination
		self.grid.addWidget(langLabel,0,0)
		self.grid.addWidget(langCombobox,0,1)

		self.grid.addWidget(annLabel,1,0)
		self.grid.addWidget(annCombobox,1,1)

		self.grid.addWidget(opaudioLabel,2,0)
		self.grid.addWidget(opaudioCombobox,2,1)

		self.grid.addWidget(cameraLabel,3,0)
		self.grid.addWidget(cameraCombobox,3,1)
		
		self.grid.addWidget(okButton,4,0)
		self.grid.addWidget(cancelButton,4,1)
		self.setLayout(self.grid)
		
def main():
	app = QtGui.QApplication(sys.argv)
	configWindow = ConfigureWindow()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
