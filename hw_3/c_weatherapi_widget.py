from PySide6 import QtWidgets
from ui.widget_c import Ui_Form
from a_threads import WeatherHandler


class WeatherMonitor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.weather_thread = None
        self.ui.pushButton.clicked.connect(self.toggle_weather)

    def toggle_weather(self):
        if self.weather_thread is None:
            lat = float(self.ui.lineEdit.text())
            lon = float(self.ui.lineEdit_2.text())
            delay = int(self.ui.lineEdit_3.text())

            self.weather_thread = WeatherHandler(lat, lon, delay)
            self.weather_thread.weatherDataReceived.connect(self.update_weather)
            self.weather_thread.start()

            self.ui.lineEdit.setDisabled(True)
            self.ui.lineEdit_2.setDisabled(True)
            self.ui.lineEdit_3.setDisabled(True)
            self.ui.pushButton.setText("Остановить")
        else:
            if self.weather_thread.isRunning():
                self.weather_thread.stop()
                self.weather_thread.wait()

            self.weather_thread = None

            self.ui.lineEdit.setEnabled(True)
            self.ui.lineEdit_2.setEnabled(True)
            self.ui.lineEdit_3.setEnabled(True)
            self.ui.pushButton.setText("Запустить")

    def update_weather(self, data):
        self.ui.textEdit.setText(f"Температура: {data['temperature']}°C\nСкорость ветра: {data['wind_speed']} км/ч")

    def closeEvent(self, event):
        if self.weather_thread:
            self.weather_thread.stop()
        event.accept()
