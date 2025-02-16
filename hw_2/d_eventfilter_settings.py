"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings_form.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtCore, QtGui
from ui.d_eventfilter_settings_form import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.settings = QtCore.QSettings("MyApp", "EventFilter")
        self.initConnections()
        self.loadSettings()
        self.ui.dial.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

    def initConnections(self):

        self.ui.dial.valueChanged.connect(self.syncWidgets)
        self.ui.horizontalSlider.valueChanged.connect(self.syncWidgets)
        self.ui.dial.installEventFilter(self)
        self.ui.comboBox.currentIndexChanged.connect(self.updateDisplayFormat)
        self.ui.comboBox.addItems(["Decimal", "Hexadecimal", "Binary", "Octal"])

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if watched == self.ui.dial and event.type() == QtCore.QEvent.KeyPress:
            if isinstance(event, QtGui.QKeyEvent):
                if event.key() == QtCore.Qt.Key_Plus:
                    self.ui.dial.setValue(self.ui.dial.value() + 1)
                    print(f"Dial value: {self.ui.dial.value()}")
                elif event.key() == QtCore.Qt.Key_Minus:
                    self.ui.dial.setValue(self.ui.dial.value() - 1)
                    print(f"Dial value: {self.ui.dial.value()}")
                return True
        return super(Window, self).eventFilter(watched, event)

    def syncWidgets(self):
        value = self.ui.dial.value()
        self.ui.horizontalSlider.setValue(value)
        self.updateLCDNumber(value)

    def updateLCDNumber(self, value):
        selected_format = self.ui.comboBox.currentText()
        if selected_format == "Decimal":
            self.ui.lcdNumber.display(value)
        elif selected_format == "Hexadecimal":
            self.ui.lcdNumber.display(hex(value)[2:].upper())
        elif selected_format == "Binary":
            self.ui.lcdNumber.display(bin(value)[2:])
        elif selected_format == "Octal":
            self.ui.lcdNumber.display(oct(value)[2:])

    def updateDisplayFormat(self):
        value = self.ui.dial.value()
        self.updateLCDNumber(value)

    def loadSettings(self):
        display_format = self.settings.value("displayFormat", "Decimal")
        lcd_value = int(self.settings.value("lcdValue", 0))
        self.ui.comboBox.setCurrentText(display_format)
        self.ui.dial.setValue(lcd_value)
        self.ui.horizontalSlider.setValue(lcd_value)
        self.updateLCDNumber(lcd_value)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.settings.setValue("displayFormat", self.ui.comboBox.currentText())
        self.settings.setValue("lcdValue", self.ui.dial.value())


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()


