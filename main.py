import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
from draw_map import draw_map
from search_org import search_org
from get_address import coords


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
        self.reset_button.clicked.connect(self.reset)
        self.full_address.setWordWrap(True)
        self.marks = []

    def show_map(self):
        try:
            zoom = self.zoom.value()
            latitude = str(self.latitude.text()).strip()
            longitude = str(self.longitude.text()).strip()
            object = str(self.object.text()).strip()
            if object != '':
                coord = search_org(object)
                if coord not in self.marks:
                    self.marks.append(coord)
                latitude = str(coord.split(',')[1])
                longitude = str(coord.split(',')[0])
                self.latitude.setText(latitude)
                self.longitude.setText(longitude)
            im = draw_map(f'{longitude},{latitude}', zoom, self.theme, self.marks)
            address, index = coords(f'{longitude},{latitude}')
            self.full_address.setText(address)
            paing = QPixmap()
            paing.loadFromData(im)
            self.map.setPixmap(paing)
        except Exception as e:
            print(e)

    def update_map(self):
        try:
            zoom = self.zoom.value()
            latitude = str(self.latitude.text()).strip()
            longitude = str(self.longitude.text()).strip()
            im = draw_map(f'{longitude},{latitude}', zoom, self.theme, self.marks)
            paing = QPixmap()
            paing.loadFromData(im)
            self.map.setPixmap(paing)
        except Exception as e:
            print(e)

    def reset(self):
        self.full_address.clear()
        self.marks.clear()
        self.update_map()

    def change_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        return self.update_map()

    def keyPressEvent(self, event):
        fl = False
        try:
            cur = self.zoom.value()
            latitude = str(self.latitude.text()).strip()
            longitude = str(self.longitude.text()).strip()
            if event.key() == Qt.Key.Key_PageUp:
                self.zoom.setValue(cur + 1)
                fl = True
            elif event.key() == Qt.Key.Key_PageDown:
                self.zoom.setValue(cur - 1)
                fl = True
            if event.key() == Qt.Key.Key_W:
                latitude = float(latitude) + 0.001
                fl = True
            if event.key() == Qt.Key.Key_S:
                latitude = float(latitude) - 0.001
                fl = True
            if event.key() == Qt.Key.Key_D:
                longitude = float(longitude) + 0.001
                fl = True
            if event.key() == Qt.Key.Key_A:
                longitude = float(longitude) - 0.001
                fl = True
            self.latitude.setText(str(round(float(latitude), 6)))
            self.longitude.setText(str(round(float(longitude), 6)))
            if fl:
                return self.update_map()
        except Exception as e:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
