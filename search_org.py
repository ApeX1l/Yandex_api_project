from pprint import pprint

import requests


def search_org(organiz, lat=None, lon=None):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        "apikey": api_key,
        "text": organiz,
        "lang": "ru_RU",
        'll' if lat and lon else '': f'{lat},{lon}',
        'spn': '0.001,0.001',
        "type": "biz",
        'results': 1
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print(response.status_code)
    json_response = response.json()
    organization = json_response["features"][0]
    name = organization['properties']['CompanyMetaData']['name']
    point = organization["geometry"]["coordinates"]
    org_point = f"{point[0]},{point[1]}"
    marker = 'pm2dgl'
    if not lat and not lon:
        return f"{org_point},{marker}"
    return (point[0], point[1]), name


# print(search_org('Петербургская 1 Казань'))
