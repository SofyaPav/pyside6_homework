"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events_form.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""

from ui.c_signals_events_form import Ui_Form
from PySide6 import QtWidgets, QtGui
from datetime import datetime

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButtonLT.clicked.connect(lambda: self.move_window(0, 0))
        self.ui.pushButtonRT.clicked.connect(lambda: self.move_window(self.screen_width() - self.width(), 0))
        self.ui.pushButtonLB.clicked.connect(lambda: self.move_window(0, self.screen_height() - self.height()))
        self.ui.pushButtonRB.clicked.connect(
            lambda: self.move_window(self.screen_width() - self.width(), self.screen_height() - self.height()))
        self.ui.pushButtonCenter.clicked.connect(self.center_window)

        self.ui.pushButtonMoveCoords.clicked.connect(self.move_to_coordinates)

        self.ui.pushButtonGetData.clicked.connect(self.get_window_info)

        self.old_pos = self.pos()
        self.resizeEvent = self.log_resize_event
        self.moveEvent = self.log_move_event


    def move_window(self, x, y):
        self.move(x, y)

    def center_window(self):
        screen = QtGui.QGuiApplication.primaryScreen().geometry()

        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def screen_width(self):
        return QtGui.QGuiApplication.primaryScreen().geometry().width()

    def screen_height(self):
        return QtGui.QGuiApplication.primaryScreen().geometry().height()


    def move_to_coordinates(self):
        x = self.ui.spinBoxX.value()
        y = self.ui.spinBoxY.value()
        self.move_window(x, y)


    def get_window_info(self):
        screen = QtGui.QGuiApplication.primaryScreen()
        geometry = screen.geometry()
        screen_number = QtGui.QGuiApplication.screenAt(self.pos()).name()
        state = {
            "Свернуто": self.isMinimized(),
            "Развернуто": self.isMaximized(),
            "Активно": self.isActiveWindow(),
            "Отображено": self.isVisible(),
        }

        info = (
            f"[{self.current_time()}] Кол-во экранов: {len(QtGui.QGuiApplication.screens())}\n"
            f"Текущее основное окно: {screen.name()}\n"
            f"Разрешение экрана: {geometry.width()}x{geometry.height()}\n"
            f"На каком экране окно находится: {screen_number}\n"
            f"Размеры окна: {self.width()}x{self.height()}\n"
            f"Минимальные размеры окна: {self.minimumWidth()}x{self.minimumHeight()}\n"
            f"Текущее положение: {self.x()}, {self.y()}\n"
            f"Координаты центра окна: {self.x() + self.width() // 2}, {self.y() + self.height() // 2}\n"
            f"Состояние окна: {state}\n"
            "----------------------------------------\n"
        )

        self.ui.plainTextEdit.appendPlainText(info)


    def current_time(self):
        return datetime.now().strftime("%H:%M:%S")


    def log_resize_event(self, event):
        print(f"[{self.current_time()}] Изменён размер окна: {event.size().width()}x{event.size().height()}")

    def log_move_event(self, event):
        new_pos = self.pos()
        print(
            f"[{self.current_time()}] Окно перемещено: {self.old_pos.x()},{self.old_pos.y()} → {new_pos.x()},{new_pos.y()}")
        self.old_pos = new_pos

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
