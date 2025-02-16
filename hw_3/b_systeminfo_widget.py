from PySide6 import QtWidgets
from ui.widget_b import Ui_Form
from a_threads import SystemInfo


class SystemMonitor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.system_thread = SystemInfo()
        self.system_thread.systemInfoReceived.connect(self.update_system_info)
        self.system_thread.start()

        self.ui.lineEdit.textChanged.connect(self.update_delay)

    def update_system_info(self, data):
        cpu, ram = data
        self.ui.lineEdit_2.setText(f"{cpu:.2f}%")
        self.ui.lineEdit_3.setText(f"{ram:.2f}%")

    def update_delay(self):
        try:
            delay = int(self.ui.lineEdit.text())
            self.system_thread.delay = delay
        except ValueError:
            pass

    def closeEvent(self, event):
        self.system_thread.stop()
        event.accept()
