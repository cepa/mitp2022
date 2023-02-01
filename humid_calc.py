from PyQt5.QtWidgets import (
    QApplication,
    QFormLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QVBoxLayout
)
import sys
import math


DEFAULT_RELATIVE_HUMIDITY   = 50
DEFAULT_AIR_TEMPERATURE     = 21
DEFAULT_AIR_PRESSURE        = 1013.25


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator wilgotności")

        layout = QVBoxLayout()
        self.setLayout(layout)

        form = QFormLayout()
        layout.addLayout(form)

        self.relHumidLine = QLineEdit()
        self.relHumidLine.insert(str(DEFAULT_RELATIVE_HUMIDITY))
        relHumidBox = QHBoxLayout()
        relHumidBox.addWidget(self.relHumidLine)
        relHumidBox.addWidget(QLabel('%'))
        form.addRow("Wilgotność względna:", relHumidBox)

        self.airTempLine = QLineEdit()
        self.airTempLine.insert(str(DEFAULT_AIR_TEMPERATURE))
        airTempBox = QHBoxLayout()
        airTempBox.addWidget(self.airTempLine)
        airTempBox.addWidget(QLabel('°C'))
        form.addRow("Temperatura powietrza: ", airTempBox)

        self.atmPressLine = QLineEdit()
        self.atmPressLine.insert(str(DEFAULT_AIR_PRESSURE))
        atmPressBox = QHBoxLayout()
        atmPressBox.addWidget(self.atmPressLine)
        atmPressBox.addWidget(QLabel('hPa'))
        form.addRow("Ciśnienie atmosferyczne: ", atmPressBox)
        
        button = QPushButton("Przelicz")
        button.clicked.connect(self.onCalculate)
        form.addRow(button)

        self.absHumidLabel = QLabel('=')
        form.addRow("Wilgotność bezwzględna", self.absHumidLabel)

        self.condTempLabel = QLabel('=')
        form.addRow("Temperatura kondensacji", self.condTempLabel)

    def onCalculate(self):
        print("onCalculate")
        relHumid = self.relHumidLine.text()
        airTemp = self.airTempLine.text()
        atmPress = self.atmPressLine.text()
        print([relHumid, airTemp, atmPress])
        absHumid, condTemp = self.calculateAbsoluteHumidity(float(relHumid), float(airTemp))
        print([absHumid, condTemp])
        self.absHumidLabel.setText('= %.02f g/m3' % absHumid)
        self.condTempLabel.setText('= %.02f °C' % condTemp)

    def calculateAbsoluteHumidity(self, relHumid, temp):
        absHumid = (1320.65 / (temp + 273.15) * (10 ** (7.4475 * temp / (temp + 233.71)))) * relHumid / 100
        condTemp = math.pow(relHumid / 100, 1.0 / 8.0) * (112 + 0.9 * temp) + (0.1 * temp) - 112
        return absHumid, condTemp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
