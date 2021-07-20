headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'login=aabibik@kpfu.ru; password=6ee4eecab075e7ee0e838f90cf681e5ef7253960d86a1e62caf96fd36cb9a943; current-org=1279',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

abiturients_list_url = 'http://85.142.162.4:8032/api/entrants/list?page={}&limit=20'

# страница абитуриента
# {} = abiturient id
abiturient_main_url = 'http://85.142.162.4:8032/api/entrants/{}/main'

# вкладка Удостоверяющие личность
# {} = abiturient id
abiturient_identification_url = 'http://85.142.162.4:8032/api/entrants/{}/docs/short?categories=identification' 

# окно паспорта
# {} = document id
abiturient_edit_url = 'http://85.142.162.4:8032/api/docs/idents/{}/edit' 

# вкладка Договор о целевом обучении
# {} = abiturient id
abiturient_contracts_url = 'http://85.142.162.4:8032/api/entrants/{}/contracts/list'

# вкладка Индивидуальные достижения
# {} = abiturient id
abiturient_achievements_url = 'http://85.142.162.4:8032/api/entrants/{}/achievements/list'

# вкладка Другие
# {} = abiturient id
abiturient_others_url = 'http://85.142.162.4:8032/api/entrants/{}/docs/short?no_categories=identification'



