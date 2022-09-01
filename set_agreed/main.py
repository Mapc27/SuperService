from datetime import datetime
from multiprocessing import Process

from config import HEADERS, COOKIE_DICT
from general import SetAgreedException, SuperService


class SuperServiceAgreed(SuperService):
    def __init__(self, city_name, process_number, agreed, result_filename=None):
        super().__init__(city_name, process_number, result_filename)
        self.agreed = agreed

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
        excel_file, rows = self.get_data_from_file(file_name, start_letter='A', end_letter='D')
        len_rows = len(rows)
        print("len_rows", len_rows)

        for i in range(len_rows):
            print(f"{i+1} of {len_rows}")
            try:
                self.process_application(rows[i])
            except Exception as e:
                print(e)
                rows[i][3].value = "Outer Exception"

        print(f"Saving file {file_name}")
        excel_file.save(file_name)

    def process_application(self, row):
        institute_type, app_uid, agreed_date, empty_cell = row[0].value, row[1].value, row[2].value, row[3]
        if not app_uid:
            return

        if not isinstance(app_uid, int):
            if not app_uid.isdigit():
                return

        assert int(institute_type) in [1, 2, 3]

        app_uid = app_uid.replace('appid', '')

        headers = HEADERS.copy()
        headers['Cookie'] = COOKIE_DICT[int(institute_type)]

        try:
            app_id = self.general_methods.get_app_from_uid(
                app_uid=app_uid,
                headers=headers
            )['id']
        except TypeError:
            empty_cell.value = "app_id not found"
            return

        if not app_id:
            empty_cell.value = "app_id not found"
            return

        print("app_uid =", app_uid, "|", "app_id =", app_id)
        try:
            self.general_methods.set_agreed(
                app_id,
                *self.general_methods.str_to_datetime(agreed_date),
                self.agreed,
                headers
            )
        except SetAgreedException as exception:
            print("app_uid =", app_uid, "|", "app_id =", app_id, "exception", exception)
            empty_cell.value = str(exception)


if __name__ == '__main__':
    start_date = datetime.now()
    SuperServiceAgreed(city_name='kazan', process_number=10, agreed=True, result_filename="согласия").main()
    print("Time:",  datetime.now() - start_date)
