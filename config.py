DEBUG = False

KAZAN_COOKIE = "login=aabibik@kpfu.ru; password=4114489c0028e78ec00859edc886aac19f7a6cc1db1af17368c53817ac0679b3;" \
               " current-org=1279"
CHELNY_COOKIE = "login=aabibik@kpfu.ru; password=4114489c0028e78ec00859edc886aac19f7a6cc1db1af17368c53817ac0679b3;" \
                " current-org=1947"
ELABUGA_COOKIE = "login=aabibik@kpfu.ru; password=4114489c0028e78ec00859edc886aac19f7a6cc1db1af17368c53817ac0679b3;" \
                 " current-org=1946"

COOKIE_DICT = {
    'kazan': KAZAN_COOKIE,
    'elabuga': ELABUGA_COOKIE,
    'chelny': CHELNY_COOKIE,
    1: KAZAN_COOKIE,
    2: ELABUGA_COOKIE,
    3: CHELNY_COOKIE,
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
}

PROXIES = {
    "http": "http://10.101.246.3:3128",
}

EXAM_RESULT_DOCUMENT_TYPE_ID = 3
CERTIFICATE_DOCUMENT_TYPE_ID = 7
VPO_DOCUMENT_TYPE_ID = 8
SPO_DOCUMENT_TYPE_ID = 9
NPO_DOCUMENT_TYPE_ID = 10

HOST_URL = 'http://10.3.60.2/'

if DEBUG:
    PROXIES = {}
    HOST_URL = 'http://85.142.162.4:8032/'


ENTRANTS_LIST_URL = HOST_URL + "api/entrants/list?page=1&limit=20&search_snils={}"
ENTRANT_DOCS_URL = HOST_URL + "api/entrants/{}/docs/short?no_categories=identification"

ENTRANT_APPLICATIONS_URL = HOST_URL + "api/entrants/{}/applications"
ENTRANT_APPLICATION_DOCS_LIST_URL = HOST_URL + "api/applications/{}/docs/list"

ENTRANT_APPLICATION_EDIT_URL = HOST_URL + "api/applications/{}/info/edit"
ENTRANT_APPLICATION_INFO_URL = HOST_URL + "api/applications/{}/info"

ENTRANT_APPLICATION_SET_STATUS_URL = HOST_URL + 'api/applications/{}/status/set'

ENTRANT_SET_ORIGINAL_URL = HOST_URL + "api/entrants/{}/original-education-document"
ENTRANT_SHORT_URL = HOST_URL + "api/entrants/{}/short"


APP_SEARCH_URL = HOST_URL + "api/applications/list?page=1&limit=20&search_snils=&search_number={}"
APP_SEARCH_UID_URL = HOST_URL + "api/applications/list?page=1&limit=20&search_uid_epgu={}"
