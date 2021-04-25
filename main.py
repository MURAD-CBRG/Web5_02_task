import sys
import pygame
import os
from size_coord import *


def show_map(ll_spn=None, map_type="map", add_params=None):
    if ll_spn:
        map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?l={map_type}"

    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as error:
        print(error)
        sys.exit(2)

    pygame.init()

    SCREEN_SIZE = [600, 450]

    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.blit(pygame.image.load(map_file), (0, 0))

    pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pass

    pygame.quit()

    os.remove(map_file)


def get_coord(address):
    toponym = geocoder_func(address)

    if not toponym:
        return (None, None)

    toponym_coodrinates = toponym["Point"]["pos"]

    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    return float(toponym_longitude), float(toponym_lattitude)


def main():
    toponym_to_find = " ".join(sys.argv[1:])

    if toponym_to_find:
        lat, lon = get_coord(toponym_to_find)
        ll_spn = f"ll={lat},{lon}&spn=0.005,0.005"
        show_map(ll_spn, "map")

        ll, spn = params_coord(toponym_to_find)
        ll_spn = f"ll={ll}&spn={spn}"
        show_map(ll_spn, "map")

        point_param = f"pt={ll}"
        show_map(ll_spn, "map", add_params=point_param)
    else:
        print('Для работы программы необходимо ввести соответствующую информацию!')


if __name__ == "__main__":
    main()
