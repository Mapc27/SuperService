import os
import json
import re
import time
from datetime import datetime

import requests

import config
import db_insertions
from xml_builder import create_xml


def get_request(url):
    return json.loads(requests.get(url, headers=config.headers).text)


def post_request(url, data):
    try:
        return requests.post(url, headers=config.headers, json=data).content
    except requests.exceptions.ProxyError:
        time.sleep(5)
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
            create_main_directories()
            entrant.create_directory()
            entrant.get_info_from_contracts()
            entrant.get_info_from_achievements()
            entrant.get_info_from_others()
            entrant.get_info_from_applications()
            entrant.get_trouble_status()

            entrant.birthday = entrant.birthday.strftime("%d.%m.%Y")

            create_xml(entrant)
            db_insertions.ins_pers(entrant)
            db_insertions.ins_pass(entrant.passports, db_insertions.get_entrant_id(entrant))
            db_insertions.ins_cert(entrant.certificates, db_insertions.get_entrant_id(entrant))
            db_insertions.ins_address(entrant, db_insertions.get_entrant_id(entrant))
            db_insertions.ins_apps(entrant.applications, db_insertions.get_entrant_id(entrant))


def create_main_directories():
    if not os.path.exists('achievements'):
        os.mkdir('achievements')

    if not os.path.exists('applications'):
        os.mkdir('applications')


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

    def create_directory(self):
        directory_name = self.surname + '_' + self.name + '_' + self.patronymic

        new_name = directory_name
        count = 1
        while os.path.exists("\\applications\\{}".format(new_name)) or os.path.exists("\\achievements\\{}"
                                                                                              .format(new_name)):
            new_name = directory_name + "_" + str(count)
            count += 1
        self.directory_name = new_name

        os.mkdir("achievements\\" + self.directory_name)
        os.mkdir("applications\\" + self.directory_name)

    def write_file(self, folder_name, file_name, format_name, file):
        new_name = file_name
        count = 1
        while os.path.exists("\\{0}\\{1}\\{2}".format(folder_name, self.directory_name, new_name + "." + format_name)):
            new_name = file_name + "_" + str(count)
            count += 1

        file_name = "\\" + folder_name + self.directory_name + "\\" + new_name + "." + format_name

        with open(file_name, 'wb') as f:
            f.write(file)

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

            self.registration_address_house =  info['registration_address']['house']
            self.registration_address_apartment =  info['registration_address']['apartment']

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
        else:
            return

        for achievement_ in info:
            achievement_id = achievement_['id']
            achievement_name = achievement_['name']
            achievement_uid_epgu = achievement_['uid_epgu']
            achievement_file = achievement_['file']
            achievement = Achievement(achievement_id, achievement_name, achievement_uid_epgu)

            self.achievements.append(achievement)

            if achievement_file:
                headers = config.headers

                headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'

                response = requests.get(url=config.entrant_achievements_download_url.format(self.id, achievement_id),
                                        headers=headers)

                file = response.content
                headers = response.headers
                content_type = re.findall(r'([a-z]{4,11}/[\w\+\-\.]+)', headers['Content-Type'])[0].split('/')[-1]

                self.write_file("achievements", achievement_name, content_type, file)

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

                document_certificate_has_file = document['file']
                document_certificate_name_document_type = doc['name_document_type']

                for field in document['fields']:
                    if field['key'] == 'id_education_level':
                        if field['defaultValue'] != '2':
                            document_certificate_is_sge = False
                            break

                certificate = Certificate(document_id, document_certificate_series, document_certificate_number,
                                          document_certificate_org, document_certificate_issue_date,
                                          document_certificate_is_sge, document_certificate_has_file, self.id)
                self.certificates.append(certificate)

                if document_certificate_has_file:
                    headers = config.headers

                    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                    headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'

                    response = requests.get(
                        url=config.entrant_others_download_url.format(document_id),
                        headers=headers)

                    file = response.content
                    response_headers = response.headers
                    content_type = re.findall(r'([a-z]{4,11}/[\w\+\-\.]+)', response_headers['Content-Type'])[0].split('/')[-1]

                    self.write_file("achievements", document_certificate_name_document_type, content_type, file)

            elif doc['id_document_type'] != 36:
                self.has_other_certificate = True

        if len(self.certificates) > 1:
            self.has_more_than_one_certificate = True

    def get_info_from_applications(self):
        if self.directory_name is None:
            directory_name = self.surname + '_' + self.name + '_' + self.patronymic
        else:
            directory_name = self.directory_name

        info = get_request(url=config.entrant_applications_url.format(self.id))['data']
        print('============== ' + directory_name + ' ============')
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

            application = Application(application_id, application_uid_epgu, application_registration_date,
                                      application_id_status, application_name_status,
                                      application_competitive_id_education_source, application_competitive_id,
                                      application_competitive_id_direction, application_competitive_uid,
                                      self.has_target_applications, application_competitive_subdivision_name,
                                      application_competitive_name, application_competitive_id_education_level,
                                      application_competitive_name_education_level, exams)

            self.applications.append(application)

            for passport in self.passports:
                for certificate in self.certificates:
                    pdf = post_request(url=config.entrant_competitive_download_url.format(application_id),
                                       data=get_attrs_for_download(passport.id, certificate.id))

                    start = application_competitive_name.find(' ') + 1
                    end = application_competitive_name.find('(') - 1
                    file_name = application_competitive_name[start:end]

                    file_path = "applications\\{0}\\{1}".format(self.directory_name, file_name)

                    print(application_competitive_name)
                    with open(file_path + ".pdf", 'wb') as file:
                        file.write(pdf)

                    self.write_file("applications", file_name, )

    def get_trouble_status(self):
        if any([self.has_achievements,
                self.has_contracts,
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
    def __init__(self, id, series, number, organization, issue_date, is_sge, document_certificate_has_file, entrant_id):
        self.id = id
        self.series = series
        self.number = number
        self.organization = organization
        self.issue_date = issue_date
        # Среднее общее образование
        self.is_sge = is_sge
        self.document_certificate_has_file = document_certificate_has_file
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


if __name__ == '__main__':
    ss = SuperService()
    ss.main()
