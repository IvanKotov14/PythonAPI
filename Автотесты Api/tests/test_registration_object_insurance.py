from testststststs.test_autorization import TestUserRegister

from testststststs.test_registration_driver import TestDriverRegister
from testststststs.test_registration_owner import TestRegisterOwner
from testststststs.test_registration_auto import TestRegisterCar
from testststststs.test_registration_insurant import TestRegisterInsurant

from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
import allure
import pytest
from datetime import datetime

@allure.epic("Кейс создания обьекта страрования")
class TestRegisterObgectInsurent(BaseCase):
    random_part = datetime.now().strftime("%m%d%Y%H%M%S")
    @allure.description("Создания обьекта страхования с авторизицией и правильными данными")
    def test_log_object_insurance(self):
        url = "v1/insured_objects/"
        drivers_id = TestDriverRegister().test_log_driver()
        owner_id = TestRegisterOwner().test_log_owner()
        car_id = TestRegisterCar().test_log_car()
        insurant_id = TestRegisterInsurant().test_log_insurant()
        valid_object_insurance = {"drivers": [
            drivers_id
        ],
            "owner": owner_id,
            "car": car_id,
            "insurant": insurant_id
        }
        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {token}"
        }
        response = MyRequests.post(url, headers=headers, json=valid_object_insurance)
        Asseretions.assert_code_status(response, 201)
        result = self.get_json_value(response, "id")
        return result

    @allure.description("Создания обьекта страхования с авторизацией, без указания адреса или данных воовсе")
    def test_log_object_insurance_negative(self):
        url = "v1/insured_objects/"
        drivers_id = TestDriverRegister().test_log_driver()
        owner_id = TestRegisterOwner().test_log_owner()
        car_id = TestRegisterCar().test_log_car()
        insurant_id = TestRegisterInsurant().test_log_insurant()
        valid_object_insurance = {"drivers": [
            drivers_id
        ],
            "owner": owner_id,
            "car": car_id,
            "insurant": insurant_id
        }
        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {token}"
        }

        valid_object_insurance.pop("insurant")

        response = MyRequests.post(url, headers=headers, json=valid_object_insurance)
        Asseretions.assert_code_status(response, 400)

        valid_object_insurance.pop("car")

        response = MyRequests.post(url, headers=headers, json=valid_object_insurance)
        Asseretions.assert_code_status(response, 400)

        response = MyRequests.post(url, headers=headers, json={})
        Asseretions.assert_code_status(response, 400)

    @allure.description("Создание обьекта страхования с произвольными данными и ожидаемым ответом")
    @pytest.mark.parametrize("drivers, owner, car, insurant, expected_status", [
        (["f2002d36-900d-4bdd-a059-c0a9bdef01f6"], "db0c6fac-6bff-4eae-abed-2705d96263e9",
         "9f4a216c-4064-452e-ab7b-114ff7959f78", "8af1200e-145f-4ce4-82f9-57ee969f50f9", 400),
        # Взятия простого id owner и insurant
        (["f2002d36-900d-4bdd-a059-c0a9bdef01f6"], "a9e9a4de-0af8-438a-baff-e78a18c20971",
         "9f4a216c-4064-452e-ab7b-114ff7959f78", "8af1200e-145f-4ce4-82f9-57ee969f50f9", 400),
        # Взятия простого id insurant
        (["f2002d36-900d-4bdd-a059-c0a9bdef01f6"], "db0c6fac-6bff-4eae-abed-2705d96263e9",
         "9f4a216c-4064-452e-ab7b-114ff7959f78", "9f085269-7280-4c2d-ba67-42ea8041ce1e", 400),
        # Взятия простого id owner
        (["f2002d36-900d-4bdd-a059-c0a9bdef01f6"], "a9e9a4de-0af8-438a-baff-e78a18c20971",
         "9f4a216c-4064-452e-ab7b-114ff7959f78", "9f085269-7280-4c2d-ba67-42ea8041ce1e", 201),  # Просто верные данные
        (["9a4d8ed6-73e7-4118-b42a-4bba0ad1e80c", "9a4d8ed6-73e7-4118-b42a-4bba0ad1e80c"],
         "a9e9a4de-0af8-438a-baff-e78a18c20971", "9f4a216c-4064-452e-ab7b-114ff7959f78",
         "9f085269-7280-4c2d-ba67-42ea8041ce1e", 400),  # Передача двух одинаковых водителей
        (["0af072a1-23b2-43cf-be0b-00417ccde007", "f2002d36-900d-4bdd-a059-c0a9bdef01f6"],
         "a9e9a4de-0af8-438a-baff-e78a18c20971", "9f4a216c-4064-452e-ab7b-114ff7959f78",
         "9f085269-7280-4c2d-ba67-42ea8041ce1e", 201),  # Передача двух разных водителей
        (["0af072a1-23b2-43cf-be0b-00417ccde007", "f2002d36-900d-4bdd-a059-c0a9bdef01f6",
          "13cc251c-244c-41ff-9add-2369206d5bc0", "13cc251c-244c-41ff-9add-2369206d5bc0"],
         "a9e9a4de-0af8-438a-baff-e78a18c20971", "9f4a216c-4064-452e-ab7b-114ff7959f78",
         "9f085269-7280-4c2d-ba67-42ea8041ce1e", 400),  # Передача четырех водителей, два из которых одиннаковые
        (["0af072a1-23b2-43cf-be0b-00417ccde007", "f2002d36-900d-4bdd-a059-c0a9bdef01f6",
          "13cc251c-244c-41ff-9add-2369206d5bc0", "fabf3c22-88a6-48b2-bdad-4fcb53a32290"],
         "a9e9a4de-0af8-438a-baff-e78a18c20971", "9f4a216c-4064-452e-ab7b-114ff7959f78",
         "9f085269-7280-4c2d-ba67-42ea8041ce1e", 201),  # Передача четырех водителей с верным id
        (["", "f2002d36-900d-4bdd-a059-c0a9bdef01f6"],
         "a9e9a4de-0af8-438a-baff-e78a18c20971", "9f4a216c-4064-452e-ab7b-114ff7959f78",
         "9f085269-7280-4c2d-ba67-42ea8041ce1e", 400),
        (["0af072a1-23b2-43cf-be0b-00417ccde007", ""],
         "a9e9a4de-0af8-438a-baff-e78a18c20971", "9f4a216c-4064-452e-ab7b-114ff7959f78",
         "9f085269-7280-4c2d-ba67-42ea8041ce1e", 400),
        ([""],
         "a9e9a4de-0af8-438a-baff-e78a18c20971", "9f4a216c-4064-452e-ab7b-114ff7959f78",
         "9f085269-7280-4c2d-ba67-42ea8041ce1e", 400),
        (["f2002d36-900d-4bdd-a059-c0a9bdef01f6"], "",
         "9f4a216c-4064-452e-ab7b-114ff7959f78", "9f085269-7280-4c2d-ba67-42ea8041ce1e", 400),
        (["f2002d36-900d-4bdd-a059-c0a9bdef01f6"], "a9e9a4de-0af8-438a-baff-e78a18c20971",
         "", "9f085269-7280-4c2d-ba67-42ea8041ce1e", 400),
        (["f2002d36-900d-4bdd-a059-c0a9bdef01f6"], "a9e9a4de-0af8-438a-baff-e78a18c20971",
         "9f4a216c-4064-452e-ab7b-114ff7959f78", "", 400),
        ([random_part], "a9e9a4de-0af8-438a-baff-e78a18c20971", "9f4a216c-4064-452e-ab7b-114ff7959f78",
         "9f085269-7280-4c2d-ba67-42ea8041ce1e", 400),
        (["f2002d36-900d-4bdd-a059-c0a9bdef01f6"], random_part, "9f4a216c-4064-452e-ab7b-114ff7959f78",
         "9f085269-7280-4c2d-ba67-42ea8041ce1e", 400),
        (["f2002d36-900d-4bdd-a059-c0a9bdef01f6"], "a9e9a4de-0af8-438a-baff-e78a18c20971", random_part,
         "9f085269-7280-4c2d-ba67-42ea8041ce1e", 400),
        (["f2002d36-900d-4bdd-a059-c0a9bdef01f6"], "a9e9a4de-0af8-438a-baff-e78a18c20971",
         "9f4a216c-4064-452e-ab7b-114ff7959f78", random_part, 400),
        ([""], "", "", "", 400)
    ])
    def test_log_object_insurance_invalid(self, drivers, owner, car, insurant, expected_status):
        url = "v1/insured_objects/"
        invalid_object_insurance = {"drivers":drivers,
                                    "owner": owner,
                                    "car": car,
                                    "insurant": insurant
                                    }
        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {token}"
        }
        response = MyRequests.post(url, headers=headers, json=invalid_object_insurance)
        Asseretions.assert_code_status(response, expected_status)