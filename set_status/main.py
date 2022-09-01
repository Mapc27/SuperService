from datetime import datetime
from multiprocessing import Process

from config import HEADERS, COOKIE_DICT
from general import SuperService, TooManyApplicationsFoundException


class SuperServiceStatus(SuperService):
    def main(self):
        file_names = self.divide_file()
        process_list = []

        for file_name in file_names:
            process = Process(target=self.application_loop, args=(file_name,))
            process_list.append(process)

            process.start()

        for process in process_list:
            process.join()

        print("Fold files")
        self.fold_files(file_names)

    def application_loop(self, file_name):
        excel_file, rows = self.get_data_from_file(file_name, start_letter='A', end_letter='C')
        len_rows = len(rows)
        print("len_rows", len_rows)

        for i in range(len_rows):
            print(f"{i+1} of {len_rows}")
            try:
                self.process_application(rows[i])
            except Exception as exception:
                print(exception)
                rows[i][2].value = "Outer Exception"
                raise exception

        print(f"Saving file {file_name}")
        excel_file.save(file_name)

    def process_application(self, row):
        institute_type, app_uid, empty_cell = row[0].value, row[1].value, row[2]
        if not app_uid:
            return

        if not isinstance(app_uid, int):
            if not app_uid.isdigit():
                return
        else:
            app_uid = str(app_uid)

        assert int(institute_type) in [1, 2, 3]

        app_uid = app_uid.replace('appid', '')

        headers = HEADERS.copy()
        headers['Cookie'] = COOKIE_DICT[int(institute_type)]

        try:
            app = self.general_methods.get_app_from_uid(
                app_uid=app_uid,
                headers=headers
            )
            app_id = app['id']
        except TooManyApplicationsFoundException as exception:
            empty_cell.value = "Количество заявлений" + str(exception)
            return
        except (TypeError, IndexError):
            empty_cell.value = "app_id not found"
            return

        if not app_id:
            empty_cell.value = "app_id not found"
            return

        print("app_uid =", app_uid, "|", "app_id =", app_id)

        if app['id_status'] == 4:
            self.general_methods.set_status_service_denied(app_id, headers)
            app = self.general_methods.get_app_from_uid(
                app_uid=app_uid,
                headers=headers
            )
            print('Set status')

        elif app['id_status'] == 8:
            self.general_methods.set_status_out_competition(app_id, headers)
            app = self.general_methods.get_app_from_uid(
                app_uid=app_uid,
                headers=headers
            )
            print('Set status')

        empty_cell.value = app['id_status']


if __name__ == '__main__':
    start_date = datetime.now()
    SuperServiceStatus(city_name='kazan', process_number=1, result_filename="не_прошёл_по_конкурсу").main()
    print("Time:", datetime.now() - start_date)
