import json

import pygsheets
import requests
from colorama import Fore, Style
from urllib3.exceptions import MaxRetryError, NewConnectionError

from app import config


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


class Application:
    def __init__(self, id):
        self.id = id
        self.is_target = False
        self.is_ochno = False
        self.is_bakalavr = False
        self.uid_epgu = False

        self.fill_information()

    def fill_information(self):
        response_ = get_request(config.entrant_application_main_url.format(self.id))
        if response_['data']['competitive']['education_form'] == "Очная форма обучения":
            self.is_ochno = True
        if response_['data']['competitive']['education_level'] == "Специалитет":
            self.is_bakalavr = False
        if ' цел, ' in response_['data']['competitive']['name']:
            self.is_target = True
        self.uid_epgu = response_['data']['application']['uid_epgu']


def fill_table(row_, application: Application):
    if application.is_ochno:
        row_[2] = 1
    else:
        row_[2] = 2

    if application.is_target:
        row_[3] = 4
        row_[6] = '01/1560'
        row_[7] = '6.08.2021'
        row_[8] = '6.08.2021'
    else:
        row_[3] = 1
        row_[6] = '01/1609'
        row_[7] = '17.08.2021'
        row_[8] = '17.08.2021'

    if application.is_bakalavr:
        row_[4] = 2
    else:
        row_[4] = 3

    row_[13] = application.uid_epgu
    row_[14] = application.uid_epgu


if __name__ == '__main__':
    gc = pygsheets.authorize(service_file='keys.json')

    sht = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1qOUwL56hV8GdDDxFohFYgLC1Cm5SPGRU2fMq1rSyFvM/edit?pli=1#gid=1791929670')

    ws = sht.worksheet_by_title('Sheet28')

    first = True
    print(Style.RESET_ALL)
    for i in range(1, len(list(ws)) + 1):
        row = ws[i]
        if first:
            first = False
            continue
        name = row[17]
        response = get_request(config.fio_search_url.format(*name.split(' ')))
        print(name)
        if not response['data']:
            print(Fore.RED, 'NOT FOUND', name)
            continue

        if len(response['data']) > 1:
            print(Fore.RED, 'MORE THAN ONE ENTRANT', name)
            continue

        entrant_id = response['data'][0]['id']

        applications = get_request(config.entrant_applications_url.format(entrant_id))

        count_agreed = 0
        for app in applications['data']:
            if app['agreed']:
                count_agreed += 1

                application = Application(app['id'])
                if application.is_ochno:
                    ws.cell((i, 2+1)).set_value('1')
                else:
                    ws.cell((i, 2+1)).set_value('2')

                if application.is_target:
                    ws.cell((i, 3+1)).set_value('4')
                    ws.cell((i, 6+1)).set_value('01/1560')
                    ws.cell((i, 7+1)).set_value('6.08.2021')
                    ws.cell((i, 8+1)).set_value('6.08.2021')

                else:
                    ws.cell((i, 3+1)).set_value('1')
                    ws.cell((i, 6+1)).set_value('01/1609')
                    ws.cell((i, 7+1)).set_value('17.08.2021')
                    ws.cell((i, 8+1)).set_value('17.08.2021')

                if application.is_bakalavr:
                    ws.cell((i, 4+1)).set_value('2')
                else:
                    ws.cell((i, 4+1)).set_value('3')

                ws.cell((i, 13+1)).set_value(application.uid_epgu)
                ws.cell((i, 14+1)).set_value(application.uid_epgu)

        if count_agreed != 1:
            print(Fore.RED, 'count_agreed != 1')
