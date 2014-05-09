__appname__ = "PyDataMan"
__module__ = "main"

from PySide.QtCore import *
from PySide.QtGui import *
import sys
import re
import sqlite3
import os
import logging
import csv

from ui_files import pyMainWindow

import preferences
import utilities

appDataPath = os.environ["APPDATA"] + "\\PyDataMan\\"

if not os.path.exists(appDataPath):
    try:
        os.makedirs(appDataPath)
    except Exception, e:
        appDataPath = os.getcwd()


logging.basicConfig(filename=appDataPath + "pydataman.log",
                    format="%(asctime)-15s: %(name)-18s - %(levelname)-8s - %(module)-15s - %(funcName)-20s - %(lineno)-6d - %(message)s")

logger = logging.getLogger(name="main-gui")



class Main(QMainWindow, pyMainWindow.Ui_mainWindow):

    dbPath = appDataPath + "pydata.db"
    dbConn = sqlite3.connect(dbPath)

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.dbCursor = self.dbConn.cursor()
        self.dbCursor.execute("""CREATE TABLE IF NOT EXISTS Main(id INTEGER PRIMARY KEY,
                                 username TEXT, name TEXT, phone TEXT, address TEXT, status TEXT)""")
        self.dbConn.commit()

        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "PyDataMan", "PyDataMan")

        self.addData.clicked.connect(self.add_button_clicked)
        self.removeRow.clicked.connect(self.remove_row_clicked)

        self.actionExport.triggered.connect(self.export_action_triggered)
        self.actionPreferences.triggered.connect(self.preferences_action_triggered)
        self.actionExit.triggered.connect(self.exit_action_triggered)

        self.showToolbar = utilities.str2bool(self.settings.value("showToolbar", True))
        self.mainToolBar.setVisible(self.showToolbar)

        self.load_initial_settings()

    def load_initial_settings(self):
        """Loads the initial settings for the application. Sets the mainTable column widths,"""
        self.dbCursor.execute("""SELECT * FROM Main""")
        allRows = self.dbCursor.fetchall()

        for row in allRows:
            inx = allRows.index(row)
            self.mainTable.insertRow(inx)
            self.mainTable.setItem(inx, 0, QTableWidgetItem(row[1]))
            self.mainTable.setItem(inx, 1, QTableWidgetItem(row[2]))
            self.mainTable.setItem(inx, 2, QTableWidgetItem(row[3]))
            self.mainTable.setItem(inx, 3, QTableWidgetItem(row[4]))
            self.mainTable.setItem(inx, 4, QTableWidgetItem(row[5]))


    def add_button_clicked(self):
        """Calls the validate_fields() method and adds the items to the table if true"""
        username = self.username.text()
        first_name = self.firstName.text()
        phone = self.phoneNumber.text()
        address = self.address.text()
        approved = self.approved.isChecked()

        if not self.validate_fields():
            return False

        currentRowCount = self.mainTable.rowCount()

        self.mainTable.insertRow(currentRowCount)
        self.mainTable.setItem(currentRowCount, 0, QTableWidgetItem(username))
        self.mainTable.setItem(currentRowCount, 1, QTableWidgetItem(first_name))
        self.mainTable.setItem(currentRowCount, 2, QTableWidgetItem(phone))
        self.mainTable.setItem(currentRowCount, 3, QTableWidgetItem(address))
        self.mainTable.setItem(currentRowCount, 4, QTableWidgetItem("Approved" if approved else "Not approved"))

        parameters = (None, username, first_name, phone, address, str(approved))
        self.dbCursor.execute('''INSERT INTO Main VALUES (?, ?, ?, ?, ?, ?)''', parameters)
        self.dbConn.commit()

    def remove_row_clicked(self):
        """Removes the selected row from the mainTable"""
        currentRow = self.mainTable.currentRow()

        if currentRow > -1:
            currentUsername = (self.mainTable.item(currentRow, 0).text(), )
            self.dbCursor.execute("""DELETE FROM Main WHERE username=?""", currentUsername)
            self.dbConn.commit()
            self.mainTable.removeRow(currentRow)


    def validate_fields(self):
        """Validates the QLineEdits based on RegEx"""
        self.dbCursor.execute("""SELECT username FROM Main""")
        usernames = self.dbCursor.fetchall()
        for username in usernames:
            if self.username.text() in username[0]:
                QMessageBox.warning(self, "Warning!", "Such username already exists!")
                return False

        if not re.match('^[2-9]\d{2}-\d{3}-\d{4}', self.phoneNumber.text()):
            QMessageBox.warning(self, "Warning", "Phone number seems incorrect!")
            return False

        return True

    def import_action_triggered(self):
        """Database import handler"""
        #THIS IS HOMEWORK! Hint #1 - Read the python doc csv.reader ; Hint #2 - There's nothing new here.
        pass

    def export_action_triggered(self):
        """Database export handler"""

        self.dbCursor.execute("SELECT * FROM Main")

        dbFile = QFileDialog.getSaveFileName(parent=None, caption="Export database to a file", directory=".", filter="PyDataMan CSV (*.csv)")

        if dbFile[0]:
            try:
                with open(dbFile[0], "wb") as csvFile:
                    csvWriter = csv.writer(csvFile, delimiter=',', quotechar="\"", quoting=csv.QUOTE_MINIMAL)

                    rows = self.dbCursor.fetchall()
                    rowCount = len(rows)

                    for row in rows:
                        csvWriter.writerow(row)

                    QMessageBox.information(self, __appname__, "Successfully exported " + str(rowCount) + " rows to a file\r\n" + str(QDir.toNativeSeparators(dbFile[0])))

            except Exception, e:
                QMessageBox.critical(self, __appname__, "Error exporting file, error is\r\n" + str(e))
                return

    def preferences_action_triggered(self):
        """Fires up the Preferences dialog"""
        dlg = preferences.Preferences(self, showToolbar=self.showToolbar)
        sig = dlg.checkboxSig

        sig.connect(self.showHideToolbar)
        dlg.exec_()


    def showHideToolbar(self, param):
        """Shows/hides main toolbar based on the checkbox value from preferences"""
        self.mainToolBar.setVisible(param)
        self.settings.setValue("showToolbar", utilities.bool2str(param))

    def about_action_triggered(self):
        """Opens the About dialog"""
        pass

    def exit_action_triggered(self):
        """This guy closes the application"""
        self.close()

    def closeEvent(self, event, *args, **kwargs):
        """Overrides the default close method"""

        result = QMessageBox.question(self, __appname__, "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if result == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    QCoreApplication.setApplicationName("PyDataMan")
    QCoreApplication.setApplicationVersion("0.1")
    QCoreApplication.setOrganizationName("PyDataMan")
    QCoreApplication.setOrganizationDomain("pydataman.com")


    app = QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()