import psycopg2
from datetime import datetime


def ins_pers(person):
    conn = psycopg2.connect('user = postgres password = qwerty12345 dbname = postgres')
    cur = conn.cursor()
    person.name = '\'%s\''%person.name
    person.surname = '\'%s\''%person.surname
    person.patronymic = '\'%s\''% person.patronymic
    person.birthday = '\'%s\''% person.birthday
    person.name_gender = '\'%s\''% person.name_gender
    person.phone = '\'%s\''% person.phone
    person.email = '\'%s\''% person.email
    person.snils = '\'%s\''% person.snils
    person.need_hostel = '\'%s\''% person.need_hostel
    person.has_trouble = '\'%s\''% person.has_trouble
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
    conn = psycopg2.connect('user = postgres password = qwerty12345 dbname = postgres')
    cur = conn.cursor()
    #language=sql
    take = 'select id from entrant where snils = %s'
    cur.execute(take % person.snils)
    arr = cur.fecthone()
    conn.commit()
    conn.close()
    return arr[0]


def ins_pass(passports, id):
    conn = psycopg2.connect('user = postgres password = qwerty12345 dbname = postgres')
    cur = conn.cursor()

    # language=sql
    insert = "insert into passport(entrant_id, series, number, issue_date, organization, sub_code) " \
             "values(%s,%s,%s,%s,%s,%s)"
    for i in passports:
        i.series = '\'%s\'' % i.series
        i.number = '\'%s\'' % i.number
        i.issue_date = '\'%s\'' % i.issue_date
        i.orgranization = '\'%s\'' % i.orgranization
        i.sub_code = '\'%s\'' % i.sub_code
        cur.execute(insert % (
            id, passports.series, passports.number, passports.issue_date, passports.orgranization, passports.sub_code))


def ins_cert(certificates):
    pass


def ins_address(address):
    pass


def ins_apps(applications):
    pass
