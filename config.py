DEBUG = True

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'login=aabibik@kpfu.ru; password=a4c141220eae40c7c42efbe372d8399cea3fefc32ee7321f72f49ade354203af; current-org=1277',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

datetime_format = "%Y-%m-%dT%H:%M:%SZ"

url = 'http://10.3.60.2/'
if DEBUG:
    url = 'http://85.142.162.4:8032/'
    headers['Cookie'] = 'login=aabibik@kpfu.ru; password=6ee4eecab075e7ee0e838f9' \
                        '0cf681e5ef7253960d86a1e62caf96fd36cb9a943; current-org=1279'


# 	"Аттестат о среднем (полном) общем образовании" id = 7
entrants_list_url = url + 'api/entrants/list?page={}&limit=20'

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

# вкладка Другие
# {} = entrant id
entrant_others_url = url + 'api/entrants/{}/docs/short?no_categories=identification'