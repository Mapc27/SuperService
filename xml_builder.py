from lxml import etree
import codecs


def create_xml(entrant):
    passports = entrant.passports
    applications = entrant.applications
    cerificates = entrant.certificates

    package_data = etree.Element('PackageData')
    ser = etree.SubElement(package_data, "ServiceEntrant")
    entrant_choice = etree.SubElement(ser, "IDEntrantChoice")
    guid = etree.SubElement(entrant_choice, "GUID")
    guid.text = ""
    snils = etree.SubElement(entrant_choice, "SNILS")
    snils.text = entrant.snils
    passport = etree.SubElement(entrant_choice, "Passport")
    ps_name = etree.SubElement(passport, "Name")
    ps_name.text = entrant.name
    ps_surname = etree.SubElement(passport, "Surname")
    ps_surname.text = str(entrant.surname)
    ps_series = etree.SubElement(passport, "Series")
    ps_series.text = passports[0].series
    ps_number = etree.SubElement(passport, "Number")
    ps_number.text = passports[0].number
    ps_birthday = etree.SubElement(passport, "Birthday")
    ps_birthday.text = str(entrant.birthday)
    ps_IDOCKCM = etree.SubElement(passport, "IDOCKCM")
    ps_IDOCKCM.text = "РОССИЯ"
    ps_org = etree.SubElement(passport, "DocOrganisation")
    ps_org.text = passports[0].organization

    education_document = etree.SubElement(entrant_choice, "EducationDocument")
    education_document.text = "Среднее общее образование"
    type = etree.SubElement(education_document, "Type")
    type.text = ""
    education_level = etree.SubElement(education_document, "EducationLevel")
    education_level.text = ""
    series = etree.SubElement(education_document, "Series")
    if not certificates:
        return
    series.text = certificates[0].series
    number = etree.SubElement(education_document, "Number")
    number.text = certificates[0].number
    organisation = etree.SubElement(education_document, "Organisation")
    organisation.text = certificates[0].organization
    issue_date = etree.SubElement(education_document, "IssueDate")
    issue_date.text = str(certificates[0].issue_date)

    surname = etree.SubElement(ser, "Surname")
    surname.text = entrant.surname
    name = etree.SubElement(ser, "Name")
    name.text = ""
    patronymic = etree.SubElement(ser, "Patronymic")
    patronymic.text = ""
    gender = etree.SubElement(ser, "Gender")
    gender.text = ""
    birth_day = etree.SubElement(ser, "Birthday")
    birth_day.text = ""
    birth_place = etree.SubElement(ser, "BirthPlace")
    birth_place.text = ""
    phone = etree.SubElement(ser, "Phone")
    phone.text = ""
    email = etree.SubElement(ser, "Email")
    email.text = ""

    need_hostel = etree.SubElement(ser, "NeedHostel")
    need_hostel.text = ""
    first_degree = etree.SubElement(ser, "FirstDegree")
    first_degree.text = "Да"
    addresses = etree.SubElement(ser, "Addresses")

    address = etree.SubElement(addresses, "Address")
    a_index = etree.SubElement(address, "IndexAddr")
    a_index.text = ""
    id_region = etree.SubElement(address, "IDRegion")
    id_region.text = ""
    area = etree.SubElement(address, "Area")
    area.text = ""
    city = etree.SubElement(address, "City")
    city.text = ""
    place = etree.SubElement(address, "Place")
    place.text = ""
    ct_area = etree.SubElement(address, "CityArea")
    ct_area.text = ""
    street = etree.SubElement(address, "Street")
    street.text = ""
    house = etree.SubElement(address, "House")
    house.text = ""
    apartment = etree.SubElement(address, "Apartment")

    service_applications = etree.SubElement(ser, "ServiceApplications")
    for i in applications:
        app = etree.SubElement(service_applications, "Application")
        id_app = etree.SubElement(app, "ID")
        id_app.text = str(i.id)
        reg_date = etree.SubElement(app, "RegistrationDate")
        reg_date.text = str(i.registration_date)
        comp_id_edu_source = etree.SubElement(app, "CompetetiveIDEducationSource")
        comp_id_edu_source.text = str(i.competitive_id_education_source)
        comp_id = etree.SubElement(app, "CompetetiveID")
        comp_id.text = str(i.competitive_id)
        comp_id_dir = etree.SubElement(app, "CompetetiveIDDirection")
        comp_id_dir.text = str(i.competitive_id_direction)
        comp_uid = etree.SubElement(app, "CompetitiveUID")
        comp_uid.text = str(i.competitive_uid)
        comp_id_ed_lvl = etree.SubElement(app, "CompetitiveIDEducationLeve")
        comp_id_ed_lvl.text = str(i.competitive_id_education_level)
        competitive_name_education_level = etree.SubElement(app, "CompetitiveNameEducationLevel")
        competitive_name_education_level.text = i.competitive_name_education_level
        competitive_group = etree.SubElement(app, "CompetitiveGroup")
        competitive_group.text = ""
        competitive_group_id = etree.SubElement(app, "CompetitiveGroupID")
        competitive_group_id.text = ""
        competitive_group_target = etree.SubElement(app, "CompetitiveGroupTarget")
        competitive_group_target.text = ""
        ege = etree.SubElement(app, "ege")
        for i in entrant.exams:
            discipline = etree.SubElement(ege, "Discipline")
            dis_name = etree.SubElement(discipline, "Name")
            dis_name.text = i.subject_name
            dis_id = etree.SubElement(discipline,"ID")
            dis_id.text = str(i.id)
            subj_id = etree.SubElement(discipline, "SubjectID")
            subj_id.text = str(i.subject_id)
            mark = etree.SubElement(discipline, "Mark")
            mark.text = str(i.subject_mark)
            issue_date_d = etree.SubElement(discipline, 'IssueDate')
            issue_date_d.text = str(i.subject_issue_date)
            priority = etree.SubElement(discipline, "Priority")
            priority.text = ""

    # etree.ElementTree(package_data).write("xmls\\file.xml")
    open("xmls\\%s.xml" % entrant.name, 'w', encoding="utf-8").write(etree.tostring(package_data, encoding='utf-8').decode('utf-8'))
