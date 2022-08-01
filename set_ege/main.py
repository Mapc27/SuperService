from pprint import pprint
from typing import List, Union

from config import EXAM_RESULT_DOCUMENT_TYPE_ID, CERTIFICATE_DOCUMENT_TYPE_ID
from general import GeneralMethods, Doc, HasUncheckedExamResultsException, Application, ApplicationDoc, \
    HasNotCheckedCertificateException, ResponseDataNotAloneException


class SuperServiceEge:
    def __init__(self, institute_type=0):
        self.general_methods = GeneralMethods(institute_type)

    @staticmethod
    def get_all_exam_results(docs: List[Union[Doc, ApplicationDoc]]):
        return list(filter(
            lambda entrant_doc: entrant_doc.id_document_type == EXAM_RESULT_DOCUMENT_TYPE_ID,
            docs
        ))

    @staticmethod
    def get_checked_exam_results(entrant_docs: List[Doc]):
        return list(filter(
            lambda entrant_doc: entrant_doc.id_document_type == EXAM_RESULT_DOCUMENT_TYPE_ID and entrant_doc.checked,
            entrant_docs
        ))

    @staticmethod
    def get_checked_certificates(entrant_docs: List[Doc]):
        return list(filter(
            lambda entrant_doc: entrant_doc.id_document_type == CERTIFICATE_DOCUMENT_TYPE_ID and entrant_doc.checked,
            entrant_docs
        ))

    @staticmethod
    def get_snils() -> List[str]:
        with open("snils.txt", 'r') as file:
            return list(map(lambda x: int(x.strip()) if x.strip().isdigit() else None, set(file.readlines())))

    def main(self):
        snils_list = set(self.get_snils())
        print(len(snils_list))
        for snils in snils_list:
            if not snils:
                continue
            pprint(snils)
            self.process_entrant(int(snils))

    def process_entrant(self, snils: int = 17465204978):
        try:
            entrant_id = self.general_methods.get_entrant_id(snils)
        except IndexError:
            print("entrant_id not found")
            return

        try:
            entrant_docs = self.general_methods.get_entrant_docs(entrant_id)
        except ResponseDataNotAloneException:
            with open("files/documents_not_found.txt", 'w') as file:
                file.write(str(snils) + '\n')
                pprint("Write to documents_not_found.txt")
                return

        exam_results = self.get_all_exam_results(entrant_docs)

        try:
            self.has_unchecked_exam_results(exam_results)
        except HasUncheckedExamResultsException:
            with open("files/unchecked_exam_results.txt", 'w') as file:
                file.write(str(snils) + '\n')
                pprint("write to unchecked_exam_results.txt")
                return

        checked_certificates = self.get_checked_certificates(entrant_docs)

        try:
            self.has_unchecked_certificate(checked_certificates)
        except HasNotCheckedCertificateException:
            with open("files/unchecked_certificate.txt", 'w') as file:
                file.write(str(snils) + '\n')
                pprint("Write to unchecked_certificate.txt")
                return

        checked_certificate = checked_certificates[0]

        right_app_docs = exam_results.copy()
        right_app_docs.append(checked_certificate)

        entrant_apps = self.general_methods.get_entrant_applications(entrant_id)
        for entrant_app in entrant_apps:
            self.process_application(entrant_app, right_app_docs)

    def process_application(self, application: Application, right_app_docs: List[Doc]):
        app_docs_list = self.general_methods.get_application_docs_list(application.id)

        new_right_app_docs = map(lambda right_app_doc: right_app_doc.dict(), right_app_docs)
        new_right_app_docs = [ApplicationDoc.parse_obj(new_exam_result) for new_exam_result in new_right_app_docs]

        for right_app_doc in new_right_app_docs:
            if right_app_doc not in app_docs_list:
                print(application.id)
                print("Здесь нужно")

    @staticmethod
    def has_unchecked_exam_results(exam_results: List[Doc]):
        for exam_result in exam_results:
            if not exam_result.checked:
                raise HasUncheckedExamResultsException(f"{exam_result} has checked attr = {exam_result.checked}")

    @staticmethod
    def has_unchecked_certificate(checked_certificates: List[Doc]):
        if len(checked_certificates) == 0:
            raise HasNotCheckedCertificateException("Entrant hasn't checked certificates")


if __name__ == '__main__':
    SuperServiceEge().main()
