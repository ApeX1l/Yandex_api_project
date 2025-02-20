import requests


def coords(geo):
    server_address = 'https://geocode-maps.yandex.ru/1.x'
    api_key = '878cfabf-805c-4bab-82f1-aabad9738fff'
    map_params = {
        'geocode': geo,
        "apikey": api_key,
        'lang': 'ru_RU',
        'format': 'json'
    }
    response = requests.get(server_address, params=map_params)
    if not response:
        print(response.status_code)
    json_response = response.json()
    address = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
        'GeocoderMetaData']['Address']['formatted']
    index = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
        'GeocoderMetaData']['Address']['postal_code']
    return address, index
