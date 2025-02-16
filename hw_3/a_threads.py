import time
import psutil
import requests
from PySide6 import QtCore


class SystemInfo(QtCore.QThread):
    systemInfoReceived = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = 1
        self.running = True

    def run(self) -> None:
        while self.running:
            cpu_value = psutil.cpu_percent(interval=1)
            ram_value = psutil.virtual_memory().percent
            self.systemInfoReceived.emit([cpu_value, ram_value])
            time.sleep(self.delay)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


class WeatherHandler(QtCore.QThread):
    weatherDataReceived = QtCore.Signal(dict)

    def __init__(self, lat, lon, delay=10, parent=None):
        super().__init__(parent)
        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        self.__delay = delay
        self.running = True

    def run(self) -> None:
        time.sleep(self.__delay)
        while self.running:
            try:
                response = requests.get(self.__api_url, timeout=5)
                data = response.json()
                weather_data = {
                    "temperature": data["current_weather"]["temperature"],
                    "wind_speed": data["current_weather"]["windspeed"]
                }
                self.weatherDataReceived.emit(weather_data)
            except Exception as e:
                print(f"Ошибка запроса погоды: {e}")
            time.sleep(self.__delay)

    def stop(self):

        self.running = False
        self.quit()
        self.wait()
