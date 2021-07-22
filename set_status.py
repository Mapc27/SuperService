import json

import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'login=aabibik@kpfu.ru; password=a4c141220eae40c7c42efbe372d8399cea3fefc32ee7321f72f49ade354203af; current-org=1277',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

url = 'http://10.3.60.2/'
entrants_list_url = url + 'api/entrants/list?page={}&limit=20'
entrant_applications_url = url + 'api/entrants/{}/applications'
entrant_application_set_status_url = url + 'api/applications/{}/status/set'


def get_request(url):
    return json.loads(requests.get(url, headers=headers).text)


def post_request(url, data):
    return requests.post(url, headers=headers, json=data).content


while True:
    entrant_id = input('entrant_id:  ')
    info = get_request(url=entrant_applications_url.format(entrant_id))['data']

    for app in info:
        application_id = app['id']
        if app['id_status'] == 2:
            status = "in_competition"
            post_request(entrant_application_set_status_url.format(application_id),
                              data={"code": status})

        elif app['id_status'] == 1 or app['id_status'] == 5:
            status = "new_cheking"
            post_request(entrant_application_set_status_url.format(application_id),
                              data={"code": status})

            status = "in_competition"
            post_request(entrant_application_set_status_url.format(application_id),
                              data={"code": status})
