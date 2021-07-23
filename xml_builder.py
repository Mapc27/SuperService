from lxml import etree
import codecs

def create_xml(entrant):

    passports = entrant.get_info_from_identification()
    applications = entrant.get_info_from_applications()
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
    ps_series = etree.SubElement(passport,"Series")
    # ps_series.text = passports[0].series
    ps_number = etree.SubElement(passport, "Number")
    ps_number.text = "passports[0].number"
    ps_birthday = etree.SubElement(passport, "Birthday")
    ps_birthday.text = str(entrant.birthday)
    ps_IDOCKCM = etree.SubElement(passport, "IDOCKCM")
    ps_IDOCKCM = "РОССИЯ"
    ps_org = etree.SubElement(passport, "DocOrganisation")
    ps_org.text = "passports[0].organization"

    education_document = etree.SubElement(entrant_choice, "EducationDocument")
    education_document.text = "Среднее общее образование"
    type = etree.SubElement(education_document, "Type")
    type.text = ""
    education_level = etree.SubElement(education_document, "EducationLevel")
    education_level.text = ""
    series = etree.SubElement(education_document, "Series")
    series.text = ""
    number = etree.SubElement(education_document, "Number")
    number.text = ""
    organisation = etree.SubElement(education_document, "Organisation")
    organisation.text = ""
    issue_date = etree.SubElement(education_document, "IssueDate")
    issue_date.text = ""

    surname = etree.SubElement(ser, "Surname")
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
    first_degree.text = ""
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
    application = etree.SubElement(service_applications, "Application")
    competitive_group = etree.SubElement(application, "CompetitiveGroup")
    competitive_group.text = ""
    competitive_group_id = etree.SubElement(application, "CompetitiveGroupID")
    competitive_group_id.text = ""
    competitive_group_target = etree.SubElement(application, "CompetitiveGroupTarget")
    competitive_group_target.text = ""
    ege = etree.SubElement(application, "ege")
    ege.text = ""
    discipline = etree.SubElement(ege, "Discipline")
    discipline.text = ""


    # etree.ElementTree(package_data).write("xmls\\file.xml")
    open("xmls\\file.xml",'w', encoding = "utf-8").write(etree.tostring(package_data, encoding='utf-8').decode('utf-8'))
