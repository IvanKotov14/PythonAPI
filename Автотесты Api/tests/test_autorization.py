import pytest

from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from datetime import datetime
from Lib.my_requests import MyRequests
import allure
@allure.epic("Кейс авторизации")
class TestUserRegister(BaseCase):
    random_part = datetime.now().strftime("%m%d%Y%H%M%S")
    base_part = "qa"
    domain = "qa.com"
    engine_power = 211

    @allure.description("Авторизация с правильными данными")
    def test_get_user_auth(self):
        url = "v1/users/obtain-token"
        valid_authorization = {
            "username": "qa@qa.qa",
            "password": "111"
        }
        response = MyRequests.post(url, data=valid_authorization)
        Asseretions.assert_code_status(response, 200)
        result = response.json()["token"]
        return result

    @allure.description("Негативный кейс авторизации, с отсутствием полей username и password")
    def test_get_user_negative_auth(self):
        url = "v1/users/obtain-token"
        valid_authorization = {
            "username": "qa@qa.qa",
            "password": "111"
        }

        valid_authorization.pop("username")

        response = MyRequests.post(url, data=valid_authorization)
        Asseretions.assert_code_status(response, 400)

        response = MyRequests.post(url, data={})
        Asseretions.assert_code_status(response, 400)


    wrong_authorization = [
        ("", "111"),
        ("qa@qa.qa", ""),
        ("", ""),
        ("qa@qa.qa", "222"),
        ("ca@ca.ca", "111"),
        ("qa@qa.qa", " 111"),
        ("qa@qa.qa", "11 1"),
        ("qa@qa.qa", "111 "),
        ("qa@ qa.qa", "111"),
        ("qa@@qa.qa", "111"),
        ("qaqa.qa", "111"),
        ("qa@.qa", "111"),
        ("qa@", "111"),
        ("qa@qa.", "111"),
        (f"{base_part}{random_part}@{domain}", "111"),
        ("qa@qa.qa", random_part)
    ]

    @allure.description("Проверка авторизации с незарегистрированными данными")
    @pytest.mark.parametrize("username, password", wrong_authorization)
    def test_get_user_not_auth(self, username, password):
        url = "v1/users/obtain-token"
        data = {"username":username,
                "password": password
                }
        response = MyRequests.post(url, data=data)
        Asseretions.assert_code_status(response, 400)

