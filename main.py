import json
from datetime import datetime

import requests
import urllib3
from urllib3.exceptions import NewConnectionError, MaxRetryError

import config
from set_status import set_status
from xml_builder import create_xml

import colorama
from colorama import Fore, Style

colorama.init()


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


@decor
def post_request(url, data):
    return requests.post(url, headers=config.headers, json=data).content


def get_attrs_for_download(passport_id, certificate_id):
    return {"docs": [
        {
            "type": "idents",
            "id": passport_id,
            "name_category": "idents",
            "name_type": "Паспорт гражданина Российской Федерации",
            "document_name": "Паспорт гражданина Российской Федерации"
        },
        {
            "type": "docs",
            "id": certificate_id,
            "name_category": "docs",
            "name_type": "Аттестат о среднем общем образовании",
            "document_name": "Аттестат о среднем общем образовании"
        }
    ]
    }


class SuperService:
    def __init__(self):
        pass

    def get_entrant_for_id(self, id):
        pass

    def get_entrants_list(self, page):
        entrants_list = get_request(url=config.entrants_list_url.format(page))['data']
        return entrants_list

    def main(self, entrant_id):
        status_ = False
        while not status_:
            try:
                entrant = Entrant(entrant_id)
                print("In process ...")
                entrant.get_info_from_main()
                entrant.get_info_from_identification()
                entrant.get_info_from_contracts()
                entrant.get_info_from_achievements()
                entrant.get_info_from_others()
                entrant.get_info_from_applications()
                entrant.get_trouble_status()

                entrant.birthday = entrant.birthday.strftime("%d.%m.%Y")

                if entrant.has_trouble:
                    print(Fore.RED + str(entrant.id), entrant.surname, entrant.name, entrant.patronymic)
                    print("http://10.3.60.2/cabinets/university/entrants/{}/docs/others".format(entrant.id))
                    print("==============================================")
                    print('entrant.has_trouble', entrant.has_trouble)
                    print("==============================================")
                    print('entrant.has_contracts', '=', entrant.has_contracts)
                    print('entrant.has_more_than_one_certificate', '=', entrant.has_more_than_one_certificate)
                    print('entrant.has_more_than_one_passport', '=', entrant.has_more_than_one_passport)
                    print('entrant.has_other_passport', '=', entrant.has_other_passport)
                    print('entrant.has_other_certificate', '=', entrant.has_other_certificate)
                    print('entrant.has_target_applications', '=', entrant.has_target_applications)
                    print(Style.RESET_ALL, end='')
                elif entrant.email is None:
                    print('entrant.email', '=', 'None')
                else:
                    create_xml(entrant)
                    if need:
                        need_set_status(entrant.id)
                status_ = True
            except (ConnectionRefusedError, requests.exceptions.ProxyError, urllib3.exceptions.MaxRetryError,
                    urllib3.exceptions.NewConnectionError, TimeoutError):
                print(Fore.RED + "Exception")
                print(Style.RESET_ALL, end='')

        # db_insertions.ins_pers(entrant)
        # db_insertions.ins_pass(entrant.passports, db_insertions.get_entrant_id(entrant))
        # db_insertions.ins_cert(entrant.certificates, db_insertions.get_entrant_id(entrant))
        # db_insertions.ins_address(entrant, db_insertions.get_entrant_id(entrant))
        # db_insertions.ins_apps(entrant.applications, db_insertions.get_entrant_id(entrant))


class Entrant:
    def __init__(self, id):
        self.id = id

        self.has_trouble = False
        self.has_achievements = False
        self.has_contracts = False
        self.has_more_than_one_certificate = False
        self.has_more_than_one_passport = False
        self.has_other_passport = False
        self.has_other_certificate = False
        self.has_target_applications = False

        self.name = None
        self.surname = None
        self.patronymic = None

        self.birthday = None
        self.snils = None
        self.birthplace = None
        self.email = None
        self.id_gender = None
        self.name_gender = None
        self.phone = None
        # registration_address
        self.registration_address_index = None
        self.registration_address_id_region = None
        self.registration_address_city = None
        # район
        self.registration_address_area = None
        # городской округ
        self.registration_address_city_area = None
        self.registration_address_street = None
        self.registration_address_name_region = None

        self.registration_address_house = None
        self.registration_address_apartment = None

        # fact address
        self.fact_address_index = None
        self.fact_address_id_region = None
        self.fact_address_city = None
        # район
        self.fact_address_area = None
        # городской округ
        self.fact_address_city_area = None
        self.fact_address_street = None
        self.fact_address_name_region = None

        self.fact_address_house = None
        self.fact_address_apartment = None

        self.need_hostel = False

        self.passports = []
        self.exams = []
        self.certificates = []
        self.applications = []
        self.achievements = []

        self.directory_name = None

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
        self.id_gender = info['id_gender']
        self.name_gender = info['name_gender']
        self.phone = info['phone']

        # registration_address
        if info['registration_address'] is not None:
            self.registration_address_index = info['registration_address']['index_addr']
            self.registration_address_id_region = info['registration_address']['id_region']
            self.registration_address_city = info['registration_address']['city']
            # район
            self.registration_address_area = info['registration_address']['area']
            # городской округ
            self.registration_address_city_area = info['registration_address']['city_area']
            self.registration_address_street = info['registration_address']['street']
            self.registration_address_name_region = info['registration_address']['name_region']

            self.registration_address_house = info['registration_address']['house']
            self.registration_address_apartment = info['registration_address']['apartment']

        # fact address
        if info['fact_address'] is not None:
            self.fact_address_index = info['fact_address']['index_addr']
            self.fact_address_id_region = info['fact_address']['id_region']
            self.fact_address_city = info['fact_address']['city']
            # район
            self.fact_address_area = info['fact_address']['area']
            # городской округ
            self.fact_address_city_area = info['fact_address']['city_area']
            self.fact_address_street = info['fact_address']['street']
            self.fact_address_name_region = info['fact_address']['name_region']

            self.fact_address_house = info['fact_address']['house']
            self.fact_address_apartment = info['fact_address']['apartment']

    def get_info_from_identification(self):
        info = get_request(config.entrant_identification_url.format(self.id))['data'][0]['docs']
        for doc in info:
            # если это паспорт гражданина РФ
            if doc['id_document_type'] == 1:
                passport = doc
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
            else:
                self.has_other_passport = True

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
        none_status = False
        less_3_status = False
        for app in info:
            application_id = app['id']
            application = get_request(url=config.entrant_application_main_url.format(application_id))['data']
            registration_date = application['application']['registration_date']
            registration_date = datetime.strptime(registration_date[0:registration_date.find('T')], config.date_format)
            application_registration_date = registration_date
            application_uid_epgu = app['uid_epgu']
            application_id_status = application['application']['id_status']
            application_name_status = application['application']['name_status']

            application_competitive_id = application['competitive']['id']

            competitive = get_request(url=config.entrant_competitive_url.format(application_competitive_id))['data']
            application_competitive_id_education_source = competitive['id_education_source']
            application_competitive_id_direction = competitive['id_direction']
            application_competitive_uid = competitive['uid']
            # целевое
            if application_competitive_id_education_source == 4:
                self.has_target_applications = True
            application_competitive_name = competitive['name']
            application_competitive_id_education_level = competitive['id_education_level']
            application_competitive_name_education_level = competitive['name_education_level']

            application_competitive_subdivision_name = \
                get_request(url=config.entrant_competitive_programs_url.
                            format(application_competitive_id))['data'][0]['subdivision_name']
            # общежитие
            if get_request(url=config.entrant_application_info_url.format(application_id))['data']['need_hostel']:
                self.need_hostel = True

            application_exams = get_request(url=config.entrant_application_exams.format(application_id))['data']

            exams = []
            for exam in application_exams:
                if exam['app_entrance_test'] is not None:
                    exam_id = exam['id']
                    exam_result_value = exam['result_value']
                    exam_uid = exam['uid']
                    exam_id_subject = exam['id_subject']
                    exam_name_subject = exam['name_subject']
                    exam_priority = exam['priority']

                    exam_obj = Exam(exam_id, exam_result_value, exam_uid, exam_id_subject, exam_name_subject,
                                    exam_priority)
                    exams.append(exam_obj)
                    none_status = True
            if len(exams) < 3:
                less_3_status = True

            application = Application(application_id, application_uid_epgu, application_registration_date,
                                      application_id_status, application_name_status,
                                      application_competitive_id_education_source, application_competitive_id,
                                      application_competitive_id_direction, application_competitive_uid,
                                      self.has_target_applications, application_competitive_subdivision_name,
                                      application_competitive_name, application_competitive_id_education_level,
                                      application_competitive_name_education_level, exams)

            self.applications.append(application)
        if not none_status:
            print(Fore.RED + "ERROR with exams - {0} {1} {2}".format(self.surname, self.name, self.patronymic))
            print(Style.RESET_ALL, end='')
        elif less_3_status:
            print(Fore.RED + 'ERROR len(exams) < 3')
            print(Style.RESET_ALL, end='')

    def get_trouble_status(self):
        if any([self.has_contracts,
                self.has_more_than_one_certificate,
                self.has_more_than_one_passport,
                self.has_other_passport,
                self.has_other_certificate,
                self.has_target_applications]):
            self.has_trouble = True


class Passport:
    def __init__(self, id, series, number, organization, subdivision_code, issue_date,
                 entrant_id):
        self.id = id
        self.series = series
        self.number = number
        self.organization = organization
        self.subdivision_code = subdivision_code
        self.issue_date = issue_date
        self.entrant_id = entrant_id


class ExamResult:
    def __init__(self, id, subject_id, subject_name, subject_mark, subject_issue_date, entrant_id):
        self.id = id
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.subject_mark = subject_mark
        self.subject_issue_date = subject_issue_date
        self.entrant_id = entrant_id


class Certificate:
    def __init__(self, id, series, number, organization, issue_date, is_sge, entrant_id):
        self.id = id
        self.series = series
        self.number = number
        self.organization = organization
        self.issue_date = issue_date
        # Среднее общее образование
        self.is_sge = is_sge
        self.entrant_id = entrant_id


class Application:
    def __init__(self, id, uid_epgu, registration_date, id_status, name_status, competitive_id_education_source,
                 competitive_id, competitive_id_direction, competitive_uid, is_target, competitive_subdivision_name,
                 competitive_name, competitive_id_education_level, competitive_name_education_level, exams):
        self.id = id
        self.uid_epgu = uid_epgu
        self.registration_date = registration_date
        self.id_status = id_status
        self.name_status = name_status
        self.competitive_id_education_source = competitive_id_education_source
        self.competitive_id = competitive_id
        self.competitive_id_direction = competitive_id_direction
        self.competitive_uid = competitive_uid
        self.is_target = is_target
        self.competitive_subdivision_name = competitive_subdivision_name
        self.competitive_name = competitive_name
        self.competitive_id_education_level = competitive_id_education_level
        self.competitive_name_education_level = competitive_name_education_level
        self.exams = exams


class Exam:
    def __init__(self, id, result_value, uid, id_subject, name_subject, priority):
        self.id = id
        self.result_value = result_value
        self.uid = uid
        self.id_subject = id_subject
        self.name_subject = name_subject
        self.priority = priority


class Achievement:
    def __init__(self, achievement_id, achievement_name, achievement_uid_epgu):
        self.achievement_id = achievement_id
        self.achievement_name = achievement_name
        self.achievement_uid_epgu = achievement_uid_epgu


def start_check(start_):
    while not start_.isdigit():
        start_ = input("Попробуйте ещё [1, 20]: ")
        while int(start_) > 20 or int(start_) < 1:
            start_ = input("Попробуйте ещё [1, 20]: ")

    while int(start_) > 20 or int(start_) < 1:
        start_ = input("Попробуйте ещё [1, 20]: ")
        while not start_.isdigit():
            start_ = input("Попробуйте ещё [1, 20]: ")
    return start_


def end_check(start_, end_):
    while not end_.isdigit():
        end_ = input("Попробуйте ещё [{}, 20]: ".format(start_))
        while int(end_) > 20 or int(end_) < start_:
            end_ = input("Попробуйте ещё [{}, 20]: ".format(start_))

    while int(end_) > 20 or int(end_) < start_:
        end_ = input("Попробуйте ещё [{}, 20]: ".format(start_))
        while not end_.isdigit():
            end_ = input("Попробуйте ещё [{}, 20]: ".format(start_))
    return end_


def lst_check(lst_):
    for element_ in lst_.split(' '):
        if not element_.isdigit():
            lst_ = input("Попробуйте ещё. Введите номера страниц через пробел: ")
            return lst_check(lst_)
    return set(lst_.split(' '))


def need_set_status(entrant_id_):
    print("===========================================================")
    print("Set status?")
    print("[0] - нет (просто нажми Enter)")
    print("[1] - да (['1', 'да', 'yes', 'ага'])")
    print("===========================================================")
    response = input("Ввод: ")
    if response.lower() in ['1', 'да', 'yes', 'ага']:
        set_status(entrant_id_)


if __name__ == '__main__':
    ss = SuperService()
    need = input("Предлагать set_status? \n    да - (['1', 'да', 'yes', 'ага']) \n    "
                 "нет - (просто нажми Enter)\n")
    while True:
        print(Style.RESET_ALL, end='')
        print("===========================================================")
        print("[0] - скачивание списка страниц")
        print("[1] - скачивание списка абитуриентов")
        print("[2] - set_status")
        print("[3] - скачивание абитуриентов на странице [1, 20]")
        print("===========================================================")
        value = input("Ввод: ")
        while value not in ['0', '1', '2', '3', '4', '5']:
            value = input("Попробуйте ещё: ")
        if value == "2":
            entrant_id = input("Введите entrant_id: ")
            set_status(entrant_id)
        elif value == "3":
            page = input("Введите страницу: ")
            while not page.isdigit():
                page = input("Попробуйте ещё: ")

            start = input("Введите начало [1, 20]: ")
            start = start_check(start)

            end = input("Введите конец: [{}, 20]".format(start))
            start = end_check(start, end)

            start, end = int(start), int(end)
            lst = ss.get_entrants_list(page)

            for i in range(start - 1, end):
                ss.main(lst[i]['id'])
        elif value == "0":
            lst = input("Введите номера страниц через пробел: ")
            lst = lst_check(lst)
            for page in lst:
                for entrant_ in ss.get_entrants_list(page):
                    ss.main(entrant_['id'])
        elif value == "1":
            lst = input("Введите entrant_id через пробел: ")
            lst = lst_check(lst)
            for entrant_id in lst:
                ss.main(entrant_id)
                print(Fore.BLUE + "===========================================================")
                print(Style.RESET_ALL, end='')
        print("Done")
        print(Fore.BLUE + "===========================================================")
        print(Style.RESET_ALL, end='')
