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
        self.map.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.show_button.clicked.connect(self.show_map)
        self.zoom.setRange(0, 21)
        self.map_width = 411
        self.map_height = 381
        self.theme = 'light'
        self.theme_button.clicked.connect(self.change_theme)
        self.reset_button.clicked.connect(self.reset)
        self.full_address.setWordWrap(True)
        self.index_radio.toggled.connect(self.postal_index)
        self.marks = []
        self.index_bool = False

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
            self.address, self.index = coords(f'{longitude},{latitude}')
            self.full_address.setText(f'{self.address} {self.index if self.index_bool else ''}')
            paing = QPixmap()
            paing.loadFromData(im)
            self.map.setPixmap(paing)
        except Exception as e:
            print(e, 101)

    def update_map(self):
        try:
            zoom = self.zoom.value()
            latitude = str(self.latitude.text()).strip()
            longitude = str(self.longitude.text()).strip()
            im = draw_map(f'{longitude},{latitude}', zoom, self.theme, self.marks)
            self.full_address.setText(f'{self.address} {self.index if self.index_bool else ''}')
            paing = QPixmap()
            paing.loadFromData(im)
            self.map.setPixmap(paing)
        except Exception as e:
            print(e, 102)

    def reset(self):
        self.full_address.clear()
        self.index_bool = False
        self.address = ''
        self.index = ''
        self.index_radio.setChecked(False)
        self.marks.clear()
        self.update_map()

    def postal_index(self):
        if self.index_radio.isChecked():
            self.index_bool = True
        else:
            self.index_bool = False
        self.update_map()

    def change_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.update_map()

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
                self.update_map()
        except Exception as e:
            # print(e, 103)
            pass

    def mousePressEvent(self, event):
        try:
            label_point = self.map.mapFromParent(event.pos())
            label_x = label_point.x()
            label_y = label_point.y()
            if 0 <= label_x < self.map_width and 0 <= label_y < self.map_height:
                lat, lon = self.pixel_to_geo(label_x, label_y)
                self.marks.append(f'{lon},{lat},pm2dgl')
                address, index = coords(f'{lon},{lat}')
                self.address = address
                self.index = index
            else:
                print('Клик за пределами карты')
            self.update_map()
        except Exception as e:
            print(e, 104)

    def pixel_to_geo(self, x, y):
        try:
            zoom = self.zoom.value()
            center_lat = float(self.latitude.text().strip())
            center_lon = float(self.longitude.text().strip())
            lon_per_pixel = 360 / (2 ** (zoom + 8))
            lat_per_pixel = 180 / (2 ** (zoom + 8))
            delta_x = x - self.map_width / 2
            delta_y = y - self.map_height / 2
            lon = center_lon + delta_x * lon_per_pixel
            lat = center_lat - delta_y * lat_per_pixel
            return lat, lon
        except Exception as e:
            print(e, 105)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
