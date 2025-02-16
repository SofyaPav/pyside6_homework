from PySide6 import QtWidgets
from b_systeminfo_widget import SystemMonitor
from c_weatherapi_widget import WeatherMonitor


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система и погода")

        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)

        self.system_monitor = SystemMonitor()
        self.weather_monitor = WeatherMonitor()
        layout.addWidget(self.system_monitor)
        layout.addWidget(self.weather_monitor)

        self.setCentralWidget(central_widget)

    def closeEvent(self, event):
        self.system_monitor.closeEvent(event)
        self.weather_monitor.closeEvent(event)
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = MainApp()
    window.show()
    app.exec()
