DEBUG = False

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'login=aabibik@kpfu.ru; password=a4c141220eae40c7c42efbe372d8399cea3fefc32ee7321f72f49ade354203af; current-org=1277',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

datetime_format = "%Y-%m-%dT%H:%M:%SZ"
datetime_format_for_application = "%Y-%m-%dT%H:%M:%SZ"
date_format = "%Y-%m-%d"

url = 'http://10.3.60.2/'
if DEBUG:
    url = 'http://85.142.162.4:8032/'
    headers['Cookie'] = 'login=aabibik@kpfu.ru; password=6ee4eecab075e7ee0e838f9' \
                        '0cf681e5ef7253960d86a1e62caf96fd36cb9a943; current-org=1279'


# 	"Аттестат о среднем (полном) общем образовании" id = 7
entrants_list_url = url + 'api/entrants/list?page={}&limit=20'
entrants_list_url_100 = url + 'api/entrants/list?page={}&limit=100'

# страница абитуриента
# {} = entrant id
entrant_main_url = url + 'api/entrants/{}/main'

# вкладка Удостоверяющие личность
# {} = entrant id
entrant_identification_url = url + 'api/entrants/{}/docs/short?categories=identification'

# окно паспорта
# {} = document id
entrant_edit_url = url + 'api/docs/idents/{}/edit'

# вкладка Договор о целевом обучении
# {} = entrant id
entrant_contracts_url = url + 'api/entrants/{}/contracts/list'

# вкладка Индивидуальные достижения
# {} = entrant id
entrant_achievements_url = url + 'api/entrants/{}/achievements/list'

# {0}, {1} = entrant id, achievement id
entrant_achievements_download_url = url + 'api/entrants/{0}/achievements/{1}/file'

# вкладка Другие
# {} = entrant id
entrant_others_url = url + 'api/entrants/{}/docs/short?no_categories=identification'

# вкладка другие -> документ
# {} = document id
entrant_others_doc_url = url + 'api/docs/{}/edit'

# вкладка заявления
# {} = entrant id
entrant_applications_url = url + 'api/entrants/{}/applications'

# страница заявления main
# {} = application id
entrant_application_main_url = url + 'api/applications/{}/main'

# окно направления
# {} = competitive id
entrant_competitive_url = url + 'api/competitive/{}/main'

# скачивание
# {} = document id
entrant_competitive_download_url = url + 'api/applications/{}/generate/pdf'

# Для общежития
# {} = application id
entrant_application_info_url = url + 'api/applications/{}/info'

# вкладка другие -> документ
# {} = document id
entrant_others_doc_url = url + 'api/docs/{}/edit'

# вкладка заявления
# {} = entrant id
entrant_applications_url = url + 'api/entrants/{}/applications'

# страница заявления main
# {} = application id
entrant_application_main_url = url + 'api/applications/{}/main'

# окно направления
# {} = competitive id
entrant_competitive_url = url + 'api/competitive/{}/main'

# За институтом
# {} = competitive id
entrant_competitive_programs_url = url + 'api/competitive/{}/programs'

# скачивание
# {} = document id
entrant_competitive_download_url = url + 'api/applications/{}/generate/pdf'

# set status
# {} = application id
entrant_application_set_status_url = url + 'api/applications/{}/status/set'

# get exams for application
# {} = application id
entrant_application_exams = url + 'api/applications/{}/tests/list'

subjects_dict = {
    '186': 'Английский язык (устный)',
    '4': 'Биология',
    '5': 'География',
    '184': 'Изложение',
    '24': 'Иностранный язык - английский',
    '14': 'Иностранный язык - испанский',
    '68': 'Иностранный язык - китайский',
    '12': 'Иностранный язык - немецкий',
    '13': 'Иностранный язык - французский',
    '3': 'Информатика и ИКТ',
    '189': 'Испанский язык (устный)',
    '7': 'История',
    '190': 'Китайский язык (устный)',
    '38': 'Крымско-татарский язык',
    '8': 'Литература',
    '2': 'Математика',
    '185': 'Математика базовая',
    '187': 'Немецкий язык (устный)',
    '9': 'Обществознание',
    '1': 'Русский язык',
    '183': 'Сочинение',
    '10': 'Физика',
    '188': 'Французский язык (устный)',
    '11': 'Химия',
}

education_level_dict = {
    2: "Бакалавриат",
    3: "Специалитет",
}

download_data = {"docs": [
            {
                "type": "idents",
                "id": None,
                "name_category": "idents",
                "name_type": "Паспорт гражданина Российской Федерации",
                "document_name": "Паспорт гражданина Российской Федерации"
            },
            {
                "type": "docs",
                "id": None,
                "name_category": "docs",
                "name_type": "Аттестат о среднем общем образовании",
                "document_name": "Аттестат о среднем общем образовании"
            }
        ]
}

status_data = {
      "done": True,
      "data": [
        {
          "code": "entrant_agreed_call_off",
          "id": 13,
          "name": "Отзыв согласия"
        },
        {
          "code": "new",
          "id": 1,
          "name": "Новое"
        },
        {
          "code": "entrant_edit",
          "id": 5,
          "name": "Редактирование профиля"
        },
        {
          "code": "new_cheking",
          "id": 2,
          "name": "Принято к рассмотрению"
        },
        {
          "code": "additional_info_wait",
          "id": 3,
          "name": "Запрос дополнительных сведений"
        },
        {
          "code": "check_date_vi",
          "id": 6,
          "name": "Назначена дата ВИ"
        },
        {
          "code": "current_date_vi",
          "id": 7,
          "name": "Выбор даты ВИ"
        },
        {
          "code": "in_competition",
          "id": 8,
          "name": "Участвует в конкурсе"
        },
        {
          "code": "entrant_agreed",
          "id": 9,
          "name": "Согласие"
        },
        {
          "code": "out_competition",
          "id": 10,
          "name": "Не прошло по конкурсу"
        },
        {
          "code": "in_order",
          "id": 11,
          "name": "Включено в приказ на зачисление"
        },
        {
          "code": "app_edit",
          "id": 14,
          "name": "Отказ от зачисления"
        },
        {
          "code": "app_call_off",
          "id": 15,
          "name": "Отзыв заявления"
        },
        {
          "code": "add_education",
          "id": 16,
          "name": "Согласие/Документ об образовании"
        },
        {
          "code": "service_denied",
          "id": 12,
          "name": "Отклонено"
        }
      ]
}

accept_url = url + 'api/applications/list?page={}&limit={}&filter_status=9'

search_url = url + 'api/entrants/list?page=1&limit=20&search_snils={}'

fio_search_url = url + 'api/entrants/list?page=1&limit=20&search_surname={0}&search_name={1}&search_patronymic={2}'

agreed_url = url + 'api/applications/{}/info/agreed'
