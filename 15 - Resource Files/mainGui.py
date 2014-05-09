# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Wed Oct 24 22:26:41 2012
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_mainDialog(object):
    def setupUi(self, mainDialog):
        mainDialog.setObjectName("mainDialog")
        mainDialog.resize(400, 231)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/app-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainDialog.setWindowIcon(icon)
        self.archButton = QtGui.QPushButton(mainDialog)
        self.archButton.setGeometry(QtCore.QRect(30, 80, 101, 61))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/arch-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.archButton.setIcon(icon1)
        self.archButton.setIconSize(QtCore.QSize(32, 32))
        self.archButton.setObjectName("archButton")
        self.fedoraButton = QtGui.QPushButton(mainDialog)
        self.fedoraButton.setGeometry(QtCore.QRect(140, 80, 111, 61))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/fedora-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fedoraButton.setIcon(icon2)
        self.fedoraButton.setIconSize(QtCore.QSize(32, 32))
        self.fedoraButton.setObjectName("fedoraButton")
        self.windowsButton = QtGui.QPushButton(mainDialog)
        self.windowsButton.setGeometry(QtCore.QRect(260, 80, 111, 61))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/windows-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.windowsButton.setIcon(icon3)
        self.windowsButton.setIconSize(QtCore.QSize(32, 32))
        self.windowsButton.setFlat(False)
        self.windowsButton.setObjectName("windowsButton")

        self.retranslateUi(mainDialog)
        QtCore.QMetaObject.connectSlotsByName(mainDialog)

    def retranslateUi(self, mainDialog):
        mainDialog.setWindowTitle(QtGui.QApplication.translate("mainDialog", "Pick an OS", None, QtGui.QApplication.UnicodeUTF8))
        self.archButton.setText(QtGui.QApplication.translate("mainDialog", "Load Arch", None, QtGui.QApplication.UnicodeUTF8))
        self.fedoraButton.setText(QtGui.QApplication.translate("mainDialog", "Load Fedora", None, QtGui.QApplication.UnicodeUTF8))
        self.windowsButton.setText(QtGui.QApplication.translate("mainDialog", "Load Windows", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
