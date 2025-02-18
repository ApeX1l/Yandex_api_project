import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
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

    def keyPressEvent(self, event):
        cur = self.zoom.value()
        if event.key() == Qt.Key.Key_PageUp:
            print(1)
            self.zoom.setValue(cur + 1)
            self.show_map()
        elif event.key() == Qt.Key.Key_PageDown:
            print(2)
            self.zoom.setValue(cur - 1)
            self.show_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
