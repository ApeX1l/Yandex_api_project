import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
from draw_map import draw_map


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('design.ui', self)
        self.show_button.clicked.connect(self.show_map)
        self.zoom.setRange(0, 21)
        self.theme = 'light'
        self.theme_button.clicked.connect(self.change_theme)

    def show_map(self):
        try:
            latitude = str(self.latitude.text()).strip()
            longitude = str(self.longitude.text()).strip()
            zoom = self.zoom.value()
            im = draw_map(f'{longitude},{latitude}', zoom, self.theme)
            paing = QPixmap()
            paing.loadFromData(im)
            self.map.setPixmap(paing)
        except Exception as e:
            print(e)

    def change_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.show_map()

    def keyPressEvent(self, event):
        try:
            cur = self.zoom.value()
            latitude = str(self.latitude.text()).strip()
            longitude = str(self.longitude.text()).strip()
            if event.key() == Qt.Key.Key_PageUp:
                self.zoom.setValue(cur + 1)
            elif event.key() == Qt.Key.Key_PageDown:
                print(1)
                self.zoom.setValue(cur - 1)
            if event.key() == Qt.Key.Key_W:
                latitude = float(latitude) + 0.0005
            elif event.key() == Qt.Key.Key_S:
                latitude = float(latitude) - 0.0005
            elif event.key() == Qt.Key.Key_D:
                longitude = float(longitude) + 0.0005
            elif event.key() == Qt.Key.Key_A:
                longitude = float(longitude) - 0.0005
            self.latitude.setText(str(latitude))
            self.longitude.setText(str(longitude))
            self.show_map()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
