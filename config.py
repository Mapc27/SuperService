headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'login=aabibik@kpfu.ru; password=a4c141220eae40c7c42efbe372d8399cea3fefc32ee7321f72f49ade354203af; current-org=1277',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

datetime_format = "%Y-%m-%dT%H:%M:%SZ"

entrants_list_url = 'http://10.3.60.2/api/entrants/list?page={}&limit=20'

# страница абитуриента
# {} = entrant id
entrant_main_url = 'http://10.3.60.2/api/entrants/{}/main'

# вкладка Удостоверяющие личность
# {} = entrant id
entrant_identification_url = 'http://10.3.60.2/api/entrants/{}/docs/short?categories=identification'

# окно паспорта
# {} = document id
entrant_edit_url = 'http://10.3.60.2/api/docs/idents/{}/edit'

# вкладка Договор о целевом обучении
# {} = entrant id
entrant_contracts_url = 'http://10.3.60.2/api/entrants/{}/contracts/list'

# вкладка Индивидуальные достижения
# {} = entrant id
entrant_achievements_url = 'http://10.3.60.2/api/entrants/{}/achievements/list'

# вкладка Другие
# {} = entrant id
entrant_others_url = 'http://10.3.60.2/api/entrants/{}/docs/short?no_categories=identification'