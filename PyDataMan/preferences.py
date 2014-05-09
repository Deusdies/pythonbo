from PySide.QtCore import *
from PySide.QtGui import *


class Preferences(QDialog):

    checkboxSig = Signal(bool) #for PyQt4 it's pyqtSignal(bool)

    def __init__(self, parent=None, showToolbar=True):
        super(Preferences, self).__init__(parent)

        self.resize(200, 100)
        self.setWindowTitle("Preferences")

        self.checkBox = QCheckBox("Show main toolbar")
        self.checkBox.setChecked(showToolbar)

        closeBtn = QPushButton("Close")

        layout = QVBoxLayout()
        layout.addWidget(self.checkBox)
        layout.addWidget(closeBtn)

        self.setLayout(layout)

        closeBtn.clicked.connect(self.close)
        self.checkBox.stateChanged.connect(self.checkBoxStateChanged)


    def checkBoxStateChanged(self):
        self.checkboxSig.emit(self.checkBox.isChecked())