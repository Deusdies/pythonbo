from PySide.QtCore import *
from PySide.QtGui import *
import sys

__appname__ = "Ninth Video"

class Program(QDialog):

    def __init__(self, parent=None):
        super(Program, self).__init__(parent)
        self.setWindowTitle(__appname__)

        btn = QPushButton("Button")
        self.spinboxlabel = QLabel("Spinbox value is ")
        self.checkboxlabel = QLabel("Checkbox is ")


        layout = QVBoxLayout()
        layout.addWidget(btn)
        layout.addWidget(self.spinboxlabel)
        layout.addWidget(self.checkboxlabel)
        self.setLayout(layout)

        self.connect(btn, SIGNAL("clicked()"), self.openDialog)

    def openDialog(self):
        dialog = Dialog()
        if dialog.exec_():
            self.spinboxlabel.setText(str(dialog.spinBox.value()))
            self.checkboxlabel.setText(str(dialog.checkBox.isChecked()))



class Dialog(QDialog):

    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setWindowTitle(__appname__ + " Dialog")

        self.spinBox = QSpinBox()
        self.checkBox = QCheckBox("Check me out!")
        okButton = QPushButton("Save")
        cancelButton = QPushButton("Cancel")

        layout = QGridLayout()

        layout.addWidget(self.spinBox, 0, 0)
        layout.addWidget(self.checkBox, 0, 1)
        layout.addWidget(okButton)
        layout.addWidget(cancelButton)
        self.setLayout(layout)

        self.connect(okButton, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(cancelButton, SIGNAL("clicked()"), self, SLOT("reject()"))

    def accept(self):

        class GreaterThanFive(Exception): pass

        spinboxval = self.spinBox.value()

        try:
            if spinboxval > 5:
                print "spinboxval"
                raise GreaterThanFive, ("The value of the spinbox cannot be greater than 5")

        except GreaterThanFive, e:
            print "LOL"













app = QApplication(sys.argv)
form = Program()
form.show()
app.exec_()

