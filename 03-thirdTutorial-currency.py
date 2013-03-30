import sys
from PySide.QtCore import *
from PySide.QtGui import *

import urllib2


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        date = self.getdata()
        rates = sorted(self.rates.keys())

        dateLabel = QLabel(date)
        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(rates)
        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 10000000.00)
        self.fromSpinBox.setValue(1.00)
        self.toComboBox = QComboBox()
        self.toComboBox.addItems(rates)
        self.toLabel = QLabel("1.00")

        grid = QGridLayout()
        grid.addWidget(dateLabel, 0, 0)
        grid.addWidget(self.fromComboBox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)


        self.connect(self.fromComboBox, SIGNAL("currentIndexChanged(int)"), self.updateUi)
        self.connect(self.toComboBox, SIGNAL("currentIndexChanged(int)"), self.updateUi)
        self.connect(self.fromSpinBox, SIGNAL("valueChanged(double)"), self.updateUi)


    def updateUi(self):
        to = self.toComboBox.currentText()
        from_ = self.fromComboBox.currentText()

        amount = (self.rates[from_] / self.rates[to]) * self.fromSpinBox.value()
        self.toLabel.setText("%0.2f" % amount)

    def getdata(self):
        self.rates = {}

        try:
            date = "Unknown"
            date_line = []

            fh = urllib2.urlopen("http://www.bankofcanada.ca/en/markets/csv/exchange_eng.csv")

            for line in fh:
                line = line.rstrip()
                if not line or line.startswith(("#", "Closing")):
                    continue

                fields = line.split(",")
                if line.startswith("Date "):
                    # Copy date line because we yet don't know on which day rates are available
                    date_line = fields[:]
                    continue

                value = -1
                # Go from right to left except name and shortname column
                for col in reversed(range(2, len(fields))):
                    try:
                        value = float(fields[col])  # try to get value
                        date = date_line[col]       # no exception > rates are available: update day
                        break
                    except ValueError:
                        # Today is holiday or conversion is not available, go one day back
                        continue

                self.rates[fields[0]] = value

            return "Exchange rates date: " + date
        except Exception, e:
            return "Failued to download:\n%s" % e


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()




