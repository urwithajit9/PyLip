from PySide import QtGui
import sys
class AboutWindow(QtGui.QWidget):
	def __init__(self):
		super(AboutWindow,self).__init__()
		self.initUI()
	def initUI(self):
		self.setWindowTitle('About PyLip')
		self.label = QtGui.QLabel('<center><b> PyLip</b> <br> This is a lipreading applicatiion.<br>It is developed as miniproject for collegework.<br> version 0.1<br> written by Aravindhan K <br> It is hosted at <br> <a>https://github.com/aravindgeek/PyLip </a></center>',self)
		self.OK = QtGui.QPushButton('OK',self)
		self.OK.resize(self.OK.sizeHint())
		self.OK.move(110,160)
		self.OK.clicked.connect(self.close)
		self.setGeometry(125,150,300,200)
		#self.show()
def main():
	app = QtGui.QApplication(sys.argv)
	aboutWindow = AboutWindow()
	aboutWindow.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
