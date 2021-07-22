import os
import json
from datetime import datetime


import requests
import openpyxl

import config


def get_request(url):
    return json.loads(requests.get(url, headers=config.headers).text)


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
            entrant.get_info_from_applications()

            passport_series = ''
            passport_number = ''
            passport_issue_date = ''
            passport_organization = ''
            passport_subdivision_code = ''
            first = True
            for passport in entrant.passports:
                if not first:
                    passport_series += ' | '
                    passport_number += ' | '
                    passport_issue_date += ' | '
                    passport_organization += ' | '
                    passport_subdivision_code += ' | '
                else:
                    first = False
                passport_series += str(passport.series)
                passport_number += str(passport.number)
                # passport_issue_date += str(passport.issue_date.day) + '.' + str(passport.issue_date.month) + '.' +\
                #                        str(passport.issue_date.year)
                passport_issue_date += passport.issue_date.strftime("%d.%m.%Y")
                passport_organization += str(passport.organization)
                passport_subdivision_code += str(passport.subdivision_code)

            certificate_series = ''
            certificate_number = ''
            certificate_issue_date = ''
            certificate_organization = ''
            first = True
            for certificate in entrant.certificates:
                if not first:
                    certificate_series += ' | '
                    certificate_number += ' | '
                    certificate_issue_date += ' | '
                    certificate_organization += ' | '
                else:
                    first = False
                certificate_series += str(certificate.series)
                certificate_number += str(certificate.number)
                # certificate_issue_date += str(certificate.issue_date.day) + '.' + str(certificate.issue_date.month) +\
                #                           '.' + str(certificate.issue_date.year)
                certificate_issue_date += certificate.issue_date.strftime("%d.%m.%Y")
                certificate_organization += str(certificate.organization)

            if entrant.snils is not None:
                snils = entrant.snils[0:3] + ' ' + entrant.snils[3:6] + ' ' + entrant.snils[6:9] + ' '\
                        + entrant.snils[9:11]

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append([
                entrant.surname,
                entrant.name,
                entrant.patronymic,
                entrant.birthday.strftime("%d.%m.%Y"),
                entrant.birthplace,
                entrant.name_gender,
                entrant.phone,
                entrant.email,

                passport_series,
                passport_number,
                passport_issue_date,
                passport_organization,
                passport_subdivision_code,

                snils,
                entrant.birthplace,

                entrant.registration_address_index,
                entrant.registration_address_name_region,
                entrant.registration_address_area,
                entrant.registration_address_city_area,
                entrant.registration_address_city,
                entrant.registration_address_street,

                entrant.fact_address_index,
                entrant.fact_address_name_region,
                entrant.fact_address_area,
                entrant.fact_address_city_area,
                entrant.fact_address_city,
                entrant.fact_address_street,

                certificate_organization,
                certificate_series,
                certificate_number,
                certificate_issue_date,

                entrant.need_hostel,

                entrant.applications
                ])

            wb.save("data.xlsx")


class Entrant:
    def __init__(self, id):
        self.id = id
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

        self.need_hostel = False

        self.passports = []
        self.exams = []
        self.certificates = []
        self.applications = []

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
        directory_name = self.surname + '_' + self.name + '_' + self.patronymic
        if not os.path.exists("applications\\" + directory_name):
            os.mkdir("applications\\" + directory_name)

        info = get_request(url=config.entrant_applications_url.format(self.id))['data']
        print('============== ' + directory_name + ' ============')
        for app in info:
            application_id = app['id']
            application = get_request(url=config.entrant_application_main_url.format(application_id))['data']
            application_changed = application['application']['changed']
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

            application = Application(application_id, application_changed, application_id_status,
                                      application_name_status, application_competitive_id_education_source,
                                      application_competitive_id, application_competitive_id_direction,
                                      application_competitive_uid, self.has_target_applications,
                                      application_competitive_name, application_competitive_id_education_level,
                                      application_competitive_name_education_level)

            self.applications.append(application)

            for passport in self.passports:
                for certificate in self.certificates:
                    pdf = post_request(url=config.entrant_competitive_download_url.format(application_id),
                                       data=get_attrs_for_download(passport.id, certificate.id))

                    start = application_competitive_name.find(' ') + 1
                    end = application_competitive_name.find('(') - 1
                    file_name = application_competitive_name[start:end]
                    count = 1
                    new_name = file_name
                    while os.path.exists('applications\\' + new_name + '.pdf'):
                        new_name = file_name + str(count)
                        count += 1
                    file_name = new_name

                    file_path = "applications\\{0}\\{1}".format(directory_name, file_name)

                    if os.path.exists(file_path + '.pdf'):
                        file_path += str(certificate.id)

                    print(application_competitive_name)
                    with open(file_path + ".pdf", 'wb') as file:
                        file.write(pdf)


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
    def __init__(self, id, date_changed, id_status, name_status, competitive_id_education_source, competitive_id,
                 competitive_id_direction, competitive_uid, is_target, competitive_subdivision_name, competitive_name,
                 competitive_id_education_level, competitive_name_education_level):
        self.id = id #
        self.date_changed = date_changed #
        self.id_status = id_status
        self.name_status = name_status #
        self.competitive_id_education_source = competitive_id_education_source
        self.competitive_id = competitive_id
        self.competitive_id_direction = competitive_id_direction
        self.competitive_uid = competitive_uid #
        self.is_target = is_target #
        self.competitive_subdivision_name = competitive_subdivision_name #
        self.competitive_name = competitive_name #
        self.competitive_id_education_level = competitive_id_education_level #
        self.competitive_name_education_level = competitive_name_education_level #


if __name__ == '__main__':
    ss = SuperService()
    ss.main()
