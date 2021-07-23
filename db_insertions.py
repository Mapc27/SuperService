import psycopg2
from datetime import datetime


password = "qwerty12345"


def ins_pers(person):
    conn = psycopg2.connect('user = postgres password = {} dbname = postgres'.format(password))
    cur = conn.cursor()
    person.name = '\'%s\'' % person.name
    person.surname = '\'%s\'' % person.surname
    person.patronymic = '\'%s\'' % person.patronymic
    person.birthday = '\'%s\'' % person.birthday
    person.name_gender = '\'%s\'' % person.name_gender
    person.phone = '\'%s\'' % person.phone
    person.email = '\'%s\'' % person.email
    person.snils = '\'%s\'' % person.snils
    person.need_hostel = '\'%s\'' % person.need_hostel
    person.has_trouble = '\'%s\'' % person.has_trouble
    # language=sql
    insert = 'insert into entrant(name, surname, patronymic, birthday, gender, phone, mail, snils, hostel, is_hard) ' \
             'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' % \
             (person.name, person.surname, person.patronymic, person.birthday, person.name_gender,
              person.phone, person.email, person.snils, person.need_hostel, person.has_trouble)

    cur.execute(insert)
    cur.close()
    conn.commit()
    conn.close()


def get_entrant_id(person):
    conn = psycopg2.connect('user = postgres password = {} dbname = postgres'.format(password))
    cur = conn.cursor()
    # language=sql
    take = 'select id from entrant where snils = %s'
    cur.execute(take % person.snils)
    arr = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return arr[0]


def ins_pass(passports, id):
    conn = psycopg2.connect('user = postgres password = {} dbname = postgres'.format(password))
    cur = conn.cursor()

    # language=sql
    insert = "insert into passport(entrant_id, series, number, issue_date, organization, sub_code) " \
             "values(%s,%s,%s,%s,%s,%s)"
    for i in range(len(passports)):
        cur.execute(insert, (
            id, passports[i].series, passports[i].number, passports[i].issue_date.strftime("%d.%m.%Y"),
            passports[i].organization, passports[i].subdivision_code))
    cur.close()
    conn.commit()
    conn.close()


def ins_cert(certificates, id):
    conn = psycopg2.connect('user = postgres password = {} dbname = postgres'.format(password))
    cur = conn.cursor()
    insert = "insert into certificate(entrant_id, series, number, issue_date, organization)" \
             " values(%s,%s,%s,%s,%s)"
    for i in certificates:
        cur.execute(insert, (id, i.series, i.number, i.issue_date.strftime("%d.%m.%Y"), i.organization))
    cur.close()
    conn.commit()
    conn.close()


def ins_address(entrant, id):
    conn = psycopg2.connect('user = postgres password = {} dbname = postgres'.format(password))
    cur = conn.cursor()
    # language=sql
    insert = "insert into address(entrant_id, r_index, r_region_name, r_area, r_city_area, r_city, r_street, f_index," \
             " f_region_name, f_area, f_city_area, f_city, f_street) " \
             " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    cur.execute(insert, (id, entrant.registration_address_index, entrant.registration_address_name_region,
                         entrant.registration_address_area, entrant.registration_address_city_area,
                         entrant.registration_address_city, entrant.registration_address_street,
                         entrant.fact_address_index,
                         entrant.fact_address_name_region,
                         entrant.fact_address_area,
                         entrant.fact_address_city_area, entrant.fact_address_city,
                         entrant.fact_address_street))
    cur.close()
    conn.commit()
    conn.close()


def ins_apps(applications, id):
    conn = psycopg2.connect('user = postgres password = {} dbname = postgres'.format(password))
    cur = conn.cursor()
    # language=sql
    insert = "insert into application(entrant_id, date_changes, status_name, uid, target, subdiv_name, id_edu_level, edu_level) " \
             "values(%s,%s,%s,%s,%s,%s,%s,%s)"
    for i in applications:
        cur.execute(insert, (id, i.registration_date.strftime("%d.%m.%Y"), i.name_status, 000, i.is_target,
                             i.competitive_subdivision_name, i.competitive_id_education_level,
                             i.competitive_name_education_level))
    cur.close()
    conn.commit()
    conn.close()
