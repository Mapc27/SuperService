import requests
import json


import config


def get_request(url):
    return json.loads(requests.get(url, headers=config.headers).text)

def post_request(url, json):
    return requests.post(url, headers=config.headers, json=json)


class SuperService:
    def get_abiturients(self):
        pass


class Abiturient:
    def __init__(self, id) -> None:
        pass

# page = 1
# output_dict = json.loads(get_request(url.format(page)).text)
# while output_dict['data'] != []:
#     print(output_dict)

#     for i in output_dict['data']:
#         print(i)
#     page += 1
#     output_dict = json.loads(get_request(url.format(page)).text)

id = 10039

print(get_request(url=config.abiturient_main_url.format(id)))