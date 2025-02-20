import requests


def search_org(organiz):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        "apikey": api_key,
        "text": organiz,
        "lang": "ru_RU",
        "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        pass
    json_response = response.json()
    organization = json_response["features"][0]
    point = organization["geometry"]["coordinates"]
    org_point = f"{point[0]},{point[1]}"
    marker = 'pm2dgl'
    return f"{org_point},{marker}"


print(search_org('Кремль'))
