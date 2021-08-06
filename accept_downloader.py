import json
import time

import requests
import pygsheets
from colorama import Fore, Style
from urllib3.exceptions import MaxRetryError, NewConnectionError

import config


def decor(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except (ConnectionRefusedError, requests.exceptions.ProxyError, MaxRetryError,
                    NewConnectionError, TimeoutError) as error:
                print(Fore.RED + "Обрабатывается ошибка {}, не переживайте".format(error))

    return wrapper


@decor
def get_request(url):
    return json.loads(requests.get(url, headers=config.headers).text)


if __name__ == '__main__':
    page = 1
    limit = 20
    timeout = 600
    gc = pygsheets.authorize(service_file='superservise-508865179b8c.json')

    sht = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1qOUwL56hV8GdDDxFohFYgLC1Cm5SPGRU2fMq1rSyFvM/edit?pli=1#gid=1791929670')

    ws_accept = sht.worksheet_by_title('Согласие')

    while True:
        ws_accept.refresh()
        was_print = False
        response = get_request(config.accept_url.format(page, limit))
        count_page = response['paginator']['count_page']
        for page in range(1, count_page + 1):
            response = get_request(config.accept_url.format(page, limit))
            for app in response['data']:
                need_append = True
                for row in ws_accept:
                    if str(row[6]) == str(app['id']):
                        need_append = False

                if need_append:
                    href = 'http://10.3.60.2/cabinets/university/application/{}'.format(app['id'])
                    is_target = False
                    if 'бюджет, цел,' in app['name_competitive_group']:
                        is_target = True

                    ws_accept.insert_rows(len(list(ws_accept)), values=[is_target, app['entrant_fullname'], href,
                                                                        app['name_competitive_group'],
                                                                        app['name_status'], app['education_level'],
                                                                        app['id']])

                    print(Fore.GREEN + str(is_target), app['entrant_fullname'], href, app['name_competitive_group'],
                          app['name_status'], app['education_level'], app['id'])
                    was_print = True

        if not was_print:
            print(Style.RESET_ALL)
            print("Новых согласий нет")
        for i in range(0, timeout + 1):
            style = Fore.GREEN
            if timeout - i < timeout // 3:
                style = Fore.RED
            elif timeout - i < timeout // 3 * 2:
                style = Fore.YELLOW
            print(style + '\rДо следующего просмотра осталось {}s'.format(timeout - i), end='', flush=True)
            time.sleep(1)
        print()
        print(Fore.LIGHTCYAN_EX + '=' * 100)
        print('=' * 100)
        print(Style.RESET_ALL)
