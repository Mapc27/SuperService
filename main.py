import requests
import json
from datetime import datetime


import config


def get_request(url):
    return json.loads(requests.get(url, headers=config.headers).text)


def post_request(url, data):
    return requests.post(url, headers=config.headers, json=data)


class SuperService:
    def __init__(self):
        self.page = 1
        self.pages_count = self.get_pages_count()

    def get_pages_count(self):
        return get_request(url=config.entrants_list_url.format(self.page))['paginator']['count_page']

    def get_entrants_list(self):
        entrants_list = get_request(url=config.entrants_list_url.format(self.page))['data']
        self.page += 1
        return entrants_list

    def main(self):
        for entrant_ in self.get_entrants_list():
            entrant = Entrant(entrant_['id'])

            entrant.get_info_from_main()
            entrant.get_info_from_identification()
            entrant.get_info_from_contracts()
            entrant.get_info_from_achievements()
            entrant.get_info_from_others()

            attrs = dir(entrant)

            for i in range(26, len(attrs)):
                print(attrs[i], entrant.__getattribute__(attrs[i]))


class Entrant:
    def __init__(self, id):
        self.id = id
        self.has_achievements = False
        self.has_contracts = False
        self.has_more_than_one_certificate = False
        self.has_more_than_one_passport = False
        self.has_other_passport = False
        self.has_other_certificate = False

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

        self.passports = []
        self.exams = []
        self.certificates = []

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
        info = get_request(config.entrant_identification_url.format(self.id))['data'][0]['docs']
        passport_count = 0
        passport = None

        for doc in info:
            # если это паспорт гражданина РФ
            if doc['id_document_type'] == 1:
                passport_count += 1
                passport = doc
            else:
                self.has_other_passport = True

        if passport_count == 1:
            document_id = passport['id']

            document = get_request(url=config.entrant_edit_url.format(passport['id']))['data']
            doc_series = document['doc_series']
            doc_number = document['doc_number']
            doc_organization = document['doc_organization']
            doc_subdivision_code = document['subdivision_code']
            doc_issue_date = datetime.strptime(document['issue_date'], config.datetime_format)
            entrant_id = document['id_entrant']

            passport = Passport(document_id, doc_series, doc_number, doc_organization, doc_subdivision_code,
                                doc_issue_date, entrant_id)

            self.passports.append(passport)
        if len(self.passports) > 1:
            self.has_more_than_one_passport = True

    def get_info_from_contracts(self):
        info = get_request(url=config.entrant_contracts_url.format(self.id))['data']
        if info:
            self.has_contracts = True

    def get_info_from_achievements(self):
        info = get_request(url=config.entrant_achievements_url.format(self.id))['data']
        if info:
            self.has_achievements = True

    def get_info_from_others(self):
        info = get_request(url=config.entrant_others_url.format(self.id))['data'][0]['docs']
        for doc in info:
            # результат егэ
            if doc['id_document_type'] == 3:
                document_id = doc['id']
                document = get_request(url=config.entrant_others_doc_url.format(document_id))['data']
                document_subject_id = None
                document_subject_mark = None
                document_subject_name = document['doc_name']
                for field in document['fields']:
                    if field['key'] == 'id_subject':
                        document_subject_id = field['defaultValue']
                    elif field['key'] == 'mark':
                        document_subject_mark = field['defaultValue']

                document_subject_issue_date = datetime.strptime(document['issue_date'], config.datetime_format)

                exam = ExamResult(document_id, document_subject_id, document_subject_name, document_subject_mark,
                                  document_subject_issue_date, self.id)
                self.exams.append(exam)

            elif doc['id_document_type'] == 7:
                document_id = doc['id']
                document = get_request(url=config.entrant_others_doc_url.format(document_id))['data']
                document_certificate_series = document['doc_series']
                document_certificate_number = document['doc_number']
                document_certificate_org = document['doc_org']
                document_certificate_is_sge = True
                document_certificate_issue_date = datetime.strptime(document['issue_date'], config.datetime_format)

                for field in document['fields']:
                    if field['key'] == 'id_education_level':
                        if field['defaultValue'] != '2':
                            document_certificate_is_sge = False
                            break

                certificate = Certificate(document_id, document_certificate_series, document_certificate_number,
                                          document_certificate_org, document_certificate_issue_date,
                                          document_certificate_is_sge, self.id)
                self.certificates.append(certificate)

            elif doc['id_document_type'] != 36:
                self.has_other_certificate = True

        if len(self.certificates) > 1:
            self.has_more_than_one_certificate = True

    def get_info_from_applications(self):
        info = get_request(url=config.entrant_applications_url.format(self.id))['data']
        for app in info:
            application_id = app['id']
            application = get_request(url=config.entrant_application_main_url.format(application_id))['data']
            application_changed = application['application']['changed']
            application_id_status = application


class Passport:
    def __init__(self, doc_id, doc_series, doc_number, doc_organization, doc_subdivision_code, doc_issue_date,
                 id_entrant):
        self.doc_id = doc_id
        self.doc_series = doc_series
        self.doc_number = doc_number
        self.doc_organization = doc_organization
        self.doc_subdivision_code = doc_subdivision_code
        self.doc_issue_date = doc_issue_date
        self.id_entrant = id_entrant


class ExamResult:
    def __init__(self, id, subject_id, subject_name, subject_mark, subject_issue_date, entrant_id):
        self.id = id
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.subject_mark = subject_mark
        self.subject_issue_date = subject_issue_date
        self.entrant_id = entrant_id


class Certificate:
    def __init__(self, id, series, number, org, issue_date, is_sge, entrant_id):
        self.id = id
        self.series = series
        self.number = number
        self.org = org
        self.issue_date = issue_date
        # Среднее общее образование
        self.is_sge = is_sge
        self.entrant_id = entrant_id


# entrant = Entrant(8497)
# entrant.get_info_from_main()
# entrant.get_info_from_identification()
# entrant.get_info_from_contracts()
# entrant.get_info_from_achievements()
# entrant.get_info_from_others()
#
# dir = dir(entrant)
#
# for i in range(26, len(dir)):
#     print(dir[i], entrant.__getattribute__(dir[i]))

#
# if __name__ == '__main__':
#     ss = SuperService()
#     ss.main()


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
