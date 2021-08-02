import json

import requests
from colorama import Fore, Style, Back
from urllib3.exceptions import NewConnectionError, MaxRetryError

import config


def decor(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except (ConnectionRefusedError, requests.exceptions.ProxyError, MaxRetryError,
                    NewConnectionError, TimeoutError) as error:
                print(Fore.RED + "Обрабатывается ошибка {}, не переживайте".format(error))
                print(Style.RESET_ALL, end='')
    return wrapper


@decor
def get_request(url):
    return json.loads(requests.get(url, headers=config.headers).text)


class Entrant:
    def __init__(self, id, name, surname, patronymic):
        self.id = id
        self.has_achievements = False
        self.trp_sign = False
        self.certificate_with_honors = False
        self.len_of_achievements = None

        self.name = name
        self.surname = surname
        self.patronymic = patronymic

    def get_info_from_achievements(self):
        info = get_request(url=config.entrant_achievements_url.format(self.id))['data']
        if info:
            self.len_of_achievements = len(info)
            self.has_achievements = True
            for achievement in info:
                if achievement['name'] == "Золотой знак ГТО":
                    self.trp_sign = True
                if achievement['name'] == "Аттестат общего образования с отличием или медалью":
                    self.certificate_with_honors = True


def print_entrant(entrant_: Entrant):
    # if color % 2 == 0:
    #     print(Fore.YELLOW + '=' * 100)
    # else:
    #     print(Fore.CYAN + '=' * 100)
    print(entrant_.surname, entrant_.name, entrant_.patronymic)
    print('http://10.3.60.2/cabinets/university/entrants/{}/docs/achievements'.format(entrant_.id))
    print('Айди абитуриента', '=', entrant_.id)
    if entrant_.trp_sign:
        print('Золотой знак ГТО', ' ' * 33, Back.GREEN + 'Есть' + Back.RESET)
    else:
        print('Золотой знак ГТО', ' ' * 33, Back.RED + 'Нет' + Back.RESET)

    if entrant_.certificate_with_honors:
        print('Аттестат общего образования с отличием или медалью', Back.GREEN + 'Есть' + Back.RESET)
    else:
        print('Аттестат общего образования с отличием или медалью', Back.RED + 'Нет' + Back.RESET)

    print('Количество достижений', '=', entrant_.len_of_achievements)
    print('=' * 100)


if __name__ == '__main__':
    color = 0
    for page in range(1, 26 + 1):
        print(Style.RESET_ALL + "=" * 20, 'page =', page, '=' * 20)
        entrants_list = get_request(url=config.entrants_list_url_100.format(page))['data']
        for ent in entrants_list:
            entrant = Entrant(ent['id'], ent['name'], ent['surname'], ent['patronymic'])
            entrant.get_info_from_achievements()
            if entrant.has_achievements:
                print_entrant(entrant)
                color += 1
