from testststststs.test_autorization import TestUserRegister

from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
import allure
import pytest

@allure.epic("Кейс ввода данных водителя")
class TestDriverRegister(BaseCase):
    @allure.description("Регистрация водителя с авторизованного пользователя и правильными данными")
    def test_log_driver(self):
        url = "v1/insured_objects/drivers"
        valid_driver = {
            "first_name": "Игорь",
            "last_name": "Угрев",
            "patronymic": "Игоревич",
            "birth_date": "1990-01-01",
            "driving_experience_started": "2010-10-10",
            "driver_licenses": [
                {
                    "credential_type": "DRIVER_LICENSE",
                    "number": "012345",
                    "series": "1234",
                    "issue_date": "2010-10-10"
                }
            ]
        }
        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {token}"
        }
        response = MyRequests.post(url, headers=headers, json=valid_driver)
        Asseretions.assert_code_status(response, 201)
        Asseretions.assert_json_has_key(response, "id")
        result = self.get_json_value(response, "id")
        return result

    @allure.description("Регистрация авторизованного водителя без определенного поля или без данных вовсе")
    def test_log_negative_driver(self):
        url = "v1/insured_objects/drivers"
        valid_driver = {
            "first_name": "Игорь",
            "last_name": "Угрев",
            "patronymic": "Игоревич",
            "birth_date": "1990-01-01",
            "driving_experience_started": "2010-10-10",
            "driver_licenses": [
                {
                    "credential_type": "DRIVER_LICENSE",
                    "number": "012345",
                    "series": "1234",
                    "issue_date": "2010-10-10"
                }
            ]
        }
        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {token}"
        }

        del valid_driver["driver_licenses"]

        response = MyRequests.post(url, headers=headers, json=valid_driver)
        Asseretions.assert_code_status(response, 400)

        response = MyRequests.post(url, headers=headers, json={})
        Asseretions.assert_code_status(response, 400)

    @allure.description("Регистрация водителя без авторизациии")
    def no_token_valid_driver(self):
        url = "v1/insured_objects/drivers"
        valid_driver = {
            "first_name": "Игорь",
            "last_name": "Угрев",
            "patronymic": "Игоревич",
            "birth_date": "1990-01-01",
            "driving_experience_started": "2010-10-10",
            "driver_licenses": [
                {
                    "credential_type": "DRIVER_LICENSE",
                    "number": "012345",
                    "series": "1234",
                    "issue_date": "2010-10-10"
                }
            ]
        }
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": ""
        }
        response = MyRequests.post(url, headers=headers, json=valid_driver)
        Asseretions.assert_code_status(response, 400)

    @allure.description("Регистрация авторизованного водителя с произвольными данными и ожидаемым ответом")
    @pytest.mark.parametrize(
        "first_name,last_name,patronymic,birth_date,driving_experience_started,credential_type,number,series,issue_date,expected_status_code",
        [
            ("Анна", "Сидорова", "Андреевна", "1985-05-05", "2005-12-31", "DRIVER_LICENSE", "678910", "5678",
             "2005-12-31", 201),
            (
            "Петр", "Иванов", "Сергеевич", "1978-11-11", "1999-07-01", "DRIVER_LICENSE", "111213", "9101", "1999-07-01",
            201),
            (
            "Иван", "Петров", "Николаевич", "1995-12-31", "2015-05-01", "DRIVER_LICENSE", "54321", "4321", "2015-05-01",
            400),
            ("Ольга", "Кузнецова", "Анатольевна", "1988-06-15", "2008-09-20", "DRIVER_LICENSE", "567890", "6789",
             "2025-06-15", 400),
            ("", "Иванов", "Сергеевич", "1978-11-11", "1999-07-01", "DRIVER_LICENSE", "111213", "9101", "1999-07-01",
             400),
            (
            "Петр", "", "Сергеевич", "1978-11-11", "1999-07-01", "DRIVER_LICENSE", "111213", "9101", "1999-07-01", 400),
            ("Петр", "Иванов", "", "1978-11-11", "1999-07-01", "DRIVER_LICENSE", "111213", "9101", "1999-07-01", 400),
            ("Петр", "Иванов", "Сергеевич", "", "1999-07-01", "DRIVER_LICENSE", "111213", "9101", "1999-07-01", 400),
            ("Петр", "Иванов", "Сергеевич", "1978-11-11", "", "DRIVER_LICENSE", "111213", "9101", "1999-07-01", 400),
            ("Петр", "Иванов", "Сергеевич", "1978-11-11", "1999-07-01", "", "111213", "9101", "1999-07-01", 400),
            (
            "Петр", "Иванов", "Сергеевич", "1978-11-11", "1999-07-01", "DRIVER_LICENSE", "", "9101", "1999-07-01", 400),
            ("", "", "", "", "", "", "", "", "", 400),
            ("", "", "", "1978-11-11", "1999-07-01", "DRIVER_LICENSE", "111213", "9101", "1999-07-01", 400),
            ("Петр", "Иванов", "Сергеевич", "1978-11-11", "1999-07-01", "INVALID_TYPE", "54321", "9101", "1999-07-01",
             400)
        ])
    def test_log_invalid_driver(self, first_name, last_name, patronymic, birth_date, driving_experience_started,
                                credential_type,
                                number, series, issue_date, expected_status_code):
        url = "v1/insured_objects/drivers"
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "patronymic": patronymic,
            "birth_date": birth_date,
            "driving_experience_started": driving_experience_started,
            "driver_licenses": [
                {
                    "credential_type": credential_type,
                    "number": number,
                    "series": series,
                    "issue_date": issue_date
                }
            ]
        }
        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {token}"
        }
        response = MyRequests.post(url, headers=headers, json=data)
        Asseretions.assert_code_status(response, expected_status_code)
