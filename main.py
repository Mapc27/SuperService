import requests
import json
from datetime import datetime


import config


def get_request(url):
    return json.loads(requests.get(url, headers=config.headers).text)


def post_request(url, data):
    return requests.post(url, headers=config.headers, json=data)


class SuperService:
    def __init__(self, page, count_page):
        self.page = page
        self.count_page = count_page

    def get_entrants_list(self):
        pass


class Entrant:
    def __init__(self, id):
        self.id = id
        self.has_more_than_one_doc = False
        self.has_achievements = False
        self.has_contracts = False
        self.has_other_doc = False

        self.name = None
        self.surname = None
        self.patronymic = None

        self.birthday = None
        self.snils = None
        self.birthplace = None
        self.email = None
        self.fact_address = None
        self.id_gender = None
        self.name_gender = None
        self.phone = None
        # registration_address
        self.registration_address_id_region = None
        self.registration_address_city = None
        # район
        self.registration_address_area = None
        # городской округ
        self.registration_address_city_area = None
        self.registration_address_city_street = None
        self.registration_address_name_region = None

        self.passport = None

    def get_info_from_main(self):
        info = get_request(config.entrant_main_url.format(self.id))['data']

        # name
        self.name = info['name']
        self.surname = info['surname']
        self.patronymic = info['patronymic']

        self.birthday = datetime.strptime(info['birthday'], config.datetime_format)
        self.snils = info['snils']
        self.birthplace = info['birthplace']
        self.email = info['email']
        self.fact_address = info['fact_address']
        self.id_gender = info['id_gender']
        self.name_gender = info['name_gender']
        self.phone = info['phone']
        # registration_address
        self.registration_address_id_region = info['registration_address']['id_region']
        self.registration_address_city = info['registration_address']['city']
        # район
        self.registration_address_area = info['registration_address']['area']
        # городской округ
        self.registration_address_city_area = info['registration_address']['city_area']
        self.registration_address_city_street = info['registration_address']['street']
        self.registration_address_name_region = info['registration_address']['name_region']

    def get_info_from_identification(self):
        info = get_request(config.entrant_identification_url.format(self.id))['docs']
        passport_count = 0
        passport = None

        for doc in info:
            # если это паспорт гражданина РФ
            if doc['id_document_type'] == 1:
                passport_count += 1
                passport = doc
            if passport_count > 1:
                self.has_more_than_one_doc = True
                break

        if passport_count == 1:
            doc_id = passport['id']

            info = get_request(url=config.entrant_edit_url.format(passport['id']))['data']
            doc_series = info['doc_series']
            doc_number = info['doc_number']
            doc_organization = info['doc_organization']
            doc_subdivision_code = info['subdivision_code']
            doc_issue_date = datetime.strptime(info['issue_date'], config.datetime_format)
            entrant_id = info['id_entrant']

            passport = Passport(doc_id, doc_series, doc_number, doc_organization, doc_subdivision_code, doc_issue_date,
                                entrant_id)

            self.passport = passport

    def get_info_from_contracts(self):
        info = get_request(url=config.entrant_contracts_url.format(self.id))['data']
        if not info:
            self.has_contracts = True

    def get_info_from_achievements(self):
        info = get_request(url=config.entrant_achievements_url.format(self.id))['data']
        if not info:
            self.has_achievements = True

    def get_info_from_others(self):
        info = get_request(url=config.entrant_others_url.format(self.id))['data']['docs']
        for doc in info:
            # результат егэ
            if doc['id_document_type'] == 3:
                mark =
                subject =
            elif doc['id_document_type'] == 7:
                pass
            else:
                self.has_other_doc = True



class Passport:
    def __init__(self, doc_id, doc_series, doc_number, doc_organization, doc_subdivision_code, doc_issue_date,
                 id_entrant):
        self.doc_id = doc_id
        self.doc_series = doc_series
        self.doc_number = doc_number
        self.doc_organization = doc_organization
        self.doc_subdivision_code = doc_subdivision_code
        self.doc_issue_date = datetime.strptime(doc_issue_date, config.datetime_format)
        self.id_entrant = id_entrant


class ExamResult:
    def __init__(self):
        self.

print(get_request(url=config.entrant_others_url.format(10688)))























# page = 1
# output_dict = json.loads(get_request(url.format(page)).text)
# while output_dict['data'] != []:
#     print(output_dict)
#     for i in output_dict['data']:
#         print(i)
#     page += 1
#     output_dict = json.loads(get_request(url.format(page)).text)
#
# data = {"docs":[{"type":"idents","id":55193,"name_category":"idents","name_type":"Паспорт гражданина Российской Федерации","document_name":"Паспорт гражданина Российской Федерации"},{"type":"docs","id":572969,"name_category":"docs","name_type":"Аттестат о среднем общем образовании","document_name":"Аттестат о среднем общем образовании"}]}
#
# # print(get_request(url=config.entrant.format(id)))
#
# pdf = post_request(url='http://10.3.60.2/api/applications/159442/generate/pdf', data=data).content
# print(pdf)
#
# with open("file.txt", 'wb') as file:
#     file.write(pdf)

# entrant = Entrant(27609)
# entrant.get_info_from_main()
# dir = dir(entrant)
#
# for i in range(26, len(dir)):
#     print(dir[i], entrant.getattribute(dir[i]))
