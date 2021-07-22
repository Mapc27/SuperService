import config
import main


entrant_id = input()
login_ = input()
passport_ = input()


def get_data(status, login, password):
    return {"code": status,
            "status_comment":"Здравствуйте. Вы подали заявление в Казанский (Приволжский) федеральный университет"
                             " через портал"
            " ЕПГУ Госуслуги. Направляем Вам информацию по личному кабинету на нашем портале \"Буду студентом\""
            " (https://abiturient.kpfu.ru/) Логин: {} Пароль: {}".format(login, password)
            }


info = main.get_request(url=config.entrant_applications_url.format(entrant_id))['data']

for app in info:
    application_id = app['id']
    if app['id_status'] == 2:
        status_ = "in_competition"
        main.post_request(config.entrant_application_set_status_url.format(application_id),
                          data=get_data(status_, login_, passport_))

    elif app['id_status'] == 1:
        status_ = "new_cheking"
        main.post_request(config.entrant_application_set_status_url.format(application_id),
                          data=get_data(status_, login_, passport_))

        status_ = "in_competition"
        main.post_request(config.entrant_application_set_status_url.format(application_id),
                          data=get_data(status_, login_, passport_))
