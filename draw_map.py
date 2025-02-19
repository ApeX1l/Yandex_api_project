import requests
from io import BytesIO
from PyQt6.QtGui import QPixmap


def draw_map(address_ll, delta, theme, org_point=None):
    apikey = "604d9abb-48ac-4c58-9c7f-c0dca0c09445"
    # print(address_ll)
    # print(delta)
    map_params = {
        # позиционируем карту центром на наш исходный адрес
        "ll": address_ll,
        'z': delta,
        'theme': theme,
        "apikey": apikey,
        # добавим точку, чтобы указать найденную аптеку
        "pt": f"{org_point},pm2dgl" if org_point else None
    }
    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    return response.content
