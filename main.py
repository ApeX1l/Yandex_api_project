import sys

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
from draw_map import draw_map


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('design.ui', self)
        self.show_button.clicked.connect(self.show_map)
        self.zoom.setRange(0, 21)

    def show_map(self):
        try:
            latitude = str(self.latitude.text()).strip()
            longitude = str(self.longitude.text()).strip()
            zoom = self.zoom.value()
            im = draw_map(f'{longitude},{latitude}', zoom)
            paing = QPixmap()
            paing.loadFromData(im)
            self.map.setPixmap(paing)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
