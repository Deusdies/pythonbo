import sys
from PySide.QtCore import *
from PySide.QtGui import *

class ZeroSpinBox(QSpinBox):

    zeros = 0

    def __init__(self, parent=None):
        super(ZeroSpinBox, self).__init__(parent)

        self.connect(self, SIGNAL("valueChanged(int)"), self.checkzero)

    def checkzero(self):
        if self.value() == 0:
            self.zeros += 1
            self.nulls = 5
            self.emit(SIGNAL("atzero"), self.zeros, self.nulls)



class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        dial = QDial()
        dial.setNotchesVisible(True)

        zerospinbox = ZeroSpinBox()

        layout = QHBoxLayout()
        layout.addWidget(dial)
        layout.addWidget(zerospinbox)
        self.setLayout(layout)

        self.connect(dial, SIGNAL("valueChanged(int)"), zerospinbox.setValue)
        self.connect(zerospinbox, SIGNAL("valueChanged(int)"), dial.setValue)
        self.connect(zerospinbox, SIGNAL("atzero"), self.announce)

        self.setWindowTitle("Signals and Slots")

    def announce(self, zeros, nulls):
        print "ZeroSPinBox has been at zero " + str(zeros) + " times."
        print "The constant nulls is ", str(nulls)



app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()


