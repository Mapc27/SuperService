import os

from lxml import etree
import re
import colorama
from colorama import Fore, Style


def create_xml(entrant):
    passports = entrant.passports
    applications = entrant.applications
    certificates = entrant.certificates

    package_data = etree.Element('PackageData')
    ser = etree.SubElement(package_data, "ServiceEntrant")
    entrant_choice = etree.SubElement(ser, "IDEntrantChoice")
    guid = etree.SubElement(entrant_choice, "GUID")
    guid.text = ""
    entrant_id = etree.SubElement(ser, "EntrantID")
    entrant_id.text = str(entrant.id)
    snils = etree.SubElement(entrant_choice, "SNILS")
    snils.text = entrant.snils
    passport = etree.SubElement(entrant_choice, "Passport")
    ps_name = etree.SubElement(passport, "Name")
    ps_name.text = entrant.name
    ps_surname = etree.SubElement(passport, "Surname")
    ps_surname.text = str(entrant.surname)
    ps_patr = etree.SubElement(passport, "Patronymic")
    ps_patr.text = entrant.patronymic
    ps_series = etree.SubElement(passport, "Series")
    try:
        ps_series.text = passports[0].series
    except:
        print(Fore.RED + "ERROR: ps_series.text = passports[0].series")
        print(Style.RESET_ALL)
        return
    ps_number = etree.SubElement(passport, "Number")
    ps_number.text = passports[0].number
    ps_birthday = etree.SubElement(passport, "Birthday")
    ps_birthday.text = str(entrant.birthday)
    ps_uid = etree.SubElement(passport, "UID")
    ps_uid.text = str(passports[0].id)
    ps_issue_date = etree.SubElement(passport, "IssueDate")
    ps_issue_date.text = str(passports[0].issue_date.strftime("%d.%m.%Y"))
    ps_org = etree.SubElement(passport, "DocOrganisation")
    ps_org.text = passports[0].organization

    education_document = etree.SubElement(entrant_choice, "EducationDocument")
    # education_document.text = "Среднее общее образование"
    type = etree.SubElement(education_document, "Type")
    type.text = "Аттестат о среднем общем образовании"
    education_level = etree.SubElement(education_document, "EducationLevel")
    education_level.text = "Среднее общее образование"
    series = etree.SubElement(education_document, "Series")
    if not certificates:
        return
    string = certificates[0].series.replace("нет", "")
    res = re.sub('\\W', "", string)
    series.text = res
    number = etree.SubElement(education_document, "Number")
    number.text = certificates[0].number
    organisation = etree.SubElement(education_document, "Organisation")
    organisation.text = certificates[0].organization
    issue_date = etree.SubElement(education_document, "IssueDate")
    issue_date.text = str(certificates[0].issue_date)

    surname = etree.SubElement(ser, "Surname")
    surname.text = entrant.surname
    name = etree.SubElement(ser, "Name")
    name.text = entrant.name
    patronymic = etree.SubElement(ser, "Patronymic")
    patronymic.text = entrant.patronymic
    gender = etree.SubElement(ser, "Gender")
    if entrant.id_gender == 1:
        entrant.id_gender = "М"
    else:
        entrant.id_gender = "Ж"
    gender.text = str(entrant.id_gender)
    birth_day = etree.SubElement(ser, "Birthday")
    birth_day.text = entrant.birthday
    birth_place = etree.SubElement(ser, "BirthPlace")
    birth_place.text = entrant.birthplace
    phone = etree.SubElement(ser, "Phone")
    phone.text = entrant.phone
    email = etree.SubElement(ser, "Email")
    email.text = entrant.email

    need_hostel = etree.SubElement(ser, "NeedHostel")
    need_hostel.text = str(entrant.need_hostel)
    first_degree = etree.SubElement(ser, "FirstDegree")
    first_degree.text = "Да"

    address = etree.SubElement(ser, "Address")
    a_index = etree.SubElement(address, "IndexAddr")
    a_index.text = entrant.registration_address_index
    id_region = etree.SubElement(address, "IDRegion")
    id_region.text = str(entrant.registration_address_id_region)
    area = etree.SubElement(address, "Area")
    area.text = ""
    if entrant.registration_address_area is not None:
        area.text = entrant.registration_address_area
    city = etree.SubElement(address, "City")
    city.text = entrant.registration_address_city
    place = etree.SubElement(address, "Place")
    place.text = ""
    ct_area = etree.SubElement(address, "CityArea")
    if entrant.registration_address_city_area is not None:
        ct_area.text = entrant.registration_address_city_area
    else:
        ct_area.text = ""
    street = etree.SubElement(address, "Street")
    street.text = entrant.registration_address_street
    house = etree.SubElement(address, "House")
    house.text = entrant.fact_address_house
    if entrant.fact_address_house is None:
        house.text = ""
    apartment = etree.SubElement(address, "Apartment")
    apartment.text = entrant.fact_address_apartment
    if entrant.fact_address_apartment is None:
        apartment.text = ""

    service_applications = etree.SubElement(ser, "ServiceApplications")
    for application in applications:
        app = etree.SubElement(service_applications, "Application")
        id_app = etree.SubElement(app, "ID")
        id_app.text = str(application.id)
        uid_epgu_app = etree.SubElement(app, "EpguUID")
        uid_epgu_app.text = str(application.uid_epgu)
        reg_date = etree.SubElement(app, "RegistrationDate")
        reg_date.text = str(application.registration_date)
        comp_id_edu_source = etree.SubElement(app, "CompetetiveIDEducationSource")
        comp_id_edu_source.text = str(application.competitive_id_education_source)
        comp_id = etree.SubElement(app, "CompetetiveID")
        comp_id.text = str(application.competitive_id)

        comp_uid = etree.SubElement(app, "UIDGroup")
        comp_uid.text = str(application.competitive_uid)
        comp_id_ed_lvl = etree.SubElement(app, "CompIDEduLvl")
        comp_id_ed_lvl.text = str(application.competitive_id_education_level)

        ege = etree.SubElement(app, "ege")
        if application.exams is []:
            continue
        for exam in application.exams:
            discipline = etree.SubElement(ege, "Discipline")
            dis_name = etree.SubElement(discipline, "Name")
            sbjName = exam.name_subject
            sbjName.replace("Результат ЕГЭ", "")
            sbjName.replace("профильная", "")
            dis_name.text = sbjName.strip()
            subj_id = etree.SubElement(discipline, "SubjectID")
            subj_id.text = str(exam.id_subject)
            mark = etree.SubElement(discipline, "Mark")
            mark.text = str(exam.result_value)
            priority = etree.SubElement(discipline, "Priority")
            priority.text = str(exam.priority)

    # etree.ElementTree(package_data).write("xmls\\file.xml")
    if not os.path.exists("xmls"):
        os.mkdir("xmls")

    file_name = entrant.surname + "_" + entrant.name + "_" + entrant.patronymic
    format_name = "xml"
    folder_name = "xmls"
    file = etree.tostring(package_data, encoding='utf-8').decode('utf-8')

    new_name = file_name
    count = 1
    while os.path.exists("{0}\\{1}".format(folder_name, new_name + "." + format_name)):
        new_name = file_name + "_" + str(count)
        count += 1

    file_name = folder_name + "\\" + new_name + "." + format_name

    with open(file_name, 'w', encoding="utf-8") as f:
        f.write(file)
    print(Fore.GREEN + str(entrant.id), file_name)
    print(Style.RESET_ALL)
    # open("xmls\\%s %s %s.xml" % (entrant.surname, entrant.name, entrant.patronymic), 'w', encoding="utf-8").write(
    #     etree.tostring(package_data, encoding='utf-8').decode('utf-8'))
