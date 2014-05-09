from PySide.QtCore import *
from PySide.QtGui import *
import sys

import mainGui


class MainWindow(QMainWindow, mainGui.Ui_MainWindow):

    mojsignal = Signal(str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        #self.connect(self.actionExit, SIGNAL("clicked()"), self.exitApp)

        self.actionExit.triggered.connect(self.exitApp)

        self.mojsignal.connect(self.zdravo)

    def zdravo(self, lol):
        print lol

    def exitApp(self):
        self.mojsignal.emit("Zdravo!")



app = QApplication(sys.argv)
form = MainWindow()
form.show()
app.exec_()
