import requests


def geocoder_func(address):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": '40d1649f-0493-4b70-98ba-98533de7710b',
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_request, params=geocoder_params)

    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {geocoder_request}
            Http статус: {response.status_code} ({response.reason})""")

    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


def params_coord(address):
    toponym = geocoder_func(address)

    if not toponym:
        return (None, None)

    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    data_base = toponym["boundedBy"]["Envelope"]

    koef1, koef2 = data_base["lowerCorner"].split(" ")
    koef3, koef4 = data_base["upperCorner"].split(" ")

    delta_x, delta_y = abs(float(koef1) - float(koef3)) / 2.0, abs(float(koef4) - float(koef2)) / 2.0

    return ",".join([toponym_longitude, toponym_lattitude]), f"{delta_x},{delta_y}"
