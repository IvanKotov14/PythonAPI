from testststststs.test_autorization import TestUserRegister

from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
import allure
import pytest

@allure.epic("Кейс ввода данных авто")
class TestRegisterCar(BaseCase):
    engine_power = 211

    @allure.description("Регистрация авто с авторизованного пользователя и правильными данными")
    def test_log_car(self):
        url = "v3/insured_objects/cars"
        valid_car = {
            "car_model_id": 864026180,
            "engine_power": self.engine_power,
            "chassis_number": 12,
            "car_body_number": 12,
            "vin_number": "WAUZZZ8T4BA037241",
            "number_plate": "Р904МХ178",
            "manufacturing_year": 2010,
            "max_mass": 122,
            "credential": [
                {"credential_type": "VEHICLE_REGISTRATION",
                 "issue_date": "2010-11-01",
                 "number": "267461",
                 "series": "78УН"}
            ]
        }

        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {token}"
        }
        response = MyRequests.post(url, headers=headers, json=valid_car)
        Asseretions.assert_code_status(response, 201)
        result = self.get_json_value(response, "id")
        return result
    @allure.description("Регистрация авто без передачи некоторых полей и без данных воовсе")
    def test_log_car_negative(self):
        url = "v3/insured_objects/cars"
        invalid_car = {
            "car_model_id": 864026180,
            "engine_power": self.engine_power,
            "chassis_number": 12,
            "car_body_number": 12,
            "vin_number": "WAUZZZ8T4BA037241",
            "number_plate": "Р904МХ178",
            "manufacturing_year": 2010,
            "max_mass": 122,
            "credential": [
                {"credential_type": "VEHICLE_REGISTRATION",
                 "issue_date": "2010-11-01",
                 "number": "267461",
                 "series": "78УН"}
            ]
        }

        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {token}"
        }

        invalid_car.pop("car_model_id")

        response = MyRequests.post(url, headers=headers, json=invalid_car)
        Asseretions.assert_code_status(response, 400)


        response = self.session.post(url, headers=headers, json={})
        Asseretions.assert_code_status(response, 400)

    @allure.description("Регистрация авто с произвольными данными и ожидаемым ответом")
    @pytest.mark.parametrize(
        "car_model_id, engine_power, chassis_number, car_body_number, vin_number, number_plate, manufacturing_year, max_mass, credential, expected_status",
        [
        (864026180, 211, "", "", "WAUZZZ8T4BA037241", "", 2010, 122, [{"credential_type": "VEHICLE_REGISTRATION", "issue_date": "2010-11-01", "number": "267461", "series": "78УН"}], 201),
        (864026180, 211, "", "", "", "Р904МХ178", 2010, 122, [{"credential_type": "VEHICLE_REGISTRATION", "issue_date": "2010-11-01", "number": "267461", "series": "78УН"}], 201),
        (864026180, 211, "", "", "", "", 2010, 122, [{"credential_type": "VEHICLE_REGISTRATION", "issue_date": "2010-11-01", "number": "267461", "series": "78УН"}], 400),
        (864026180, 211, "12345678901234567", "", "", "", 2010, 122, [{"credential_type": "VEHICLE_REGISTRATION", "issue_date": "2010-11-01", "number": "267461", "series": "78УН"}], 201),
        (864026180, 211, "", "12345678901234567", "", "", 2010, 122, [{"credential_type": "VEHICLE_REGISTRATION", "issue_date": "2010-11-01", "number": "267461", "series": "78УН"}], 201),
        (864026180, 211, "", "", "WAUZZZ8T4BA037241", "Р904МХ178", 2010, 122, [{"credential_type": "VEHICLE_REGISTRATION", "issue_date": "2010-11-01", "number": "267461", "series": "78УН"}], 201),
        (864026180, 211, "", "", "", "", "", 122, [{"credential_type": "VEHICLE_REGISTRATION", "issue_date": "2010-11-01", "number": "267461", "series": "78УН"}], 400),
        (864026180, 211, "", "", "", "", 2023, 122, [{"credential_type": "VEHICLE_REGISTRATION", "issue_date": "2010-11-01", "number": "267461", "series": "78УН"}], 400),
        (864026180, 211, "", "", "", "", 2010, 0, [{"credential_type": "VEHICLE_REGISTRATION", "issue_date": "2010-11-01", "number": "267461", "series": "78УН"}], 400),
        (864026180, 211, "", "", "", "", 2010, "", [{"credential_type": "VEHICLE_REGISTRATION", "issue_date": "2010-11-01", "number": "267461", "series": "78УН"}], 400),
        (864026180, 100, "invalid", "", "", "", 2010, 122, [{"credential_type": "VEHICLE_REGISTRATION", "issue_date": "2010-11-01", "number": "267461","series": "78УН"}], 400),
        (864026180, 100, "12345678901234567", "invalid", "", "", 2010, 122, [{"credential_type": "VEHICLE_REGISTRATION", "issue_date": "2010-11-01", "number": "267461","series": "78УН"}], 400),
        (864026180, 100, "", "invalid", "", "", 2010, 122, [{"credential_type": "VEHICLE_REGISTRATION", "issue_date": "2010-11-01", "number": "267461","series": "78УН"}], 400),
        ]
    )
    def test_log_car_invalid(self, car_model_id, engine_power, chassis_number, car_body_number, vin_number, number_plate, manufacturing_year, max_mass, credential, expected_status):
        url = "v3/insured_objects/cars"
        valid_car = {
            "car_model_id": car_model_id,
            "engine_power": engine_power,
            "chassis_number": chassis_number,
            "car_body_number": car_body_number,
            "vin_number": vin_number,
            "number_plate": number_plate,
            "manufacturing_year": manufacturing_year,
            "max_mass": max_mass,
            "credential": credential
        }

        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {token}"
        }
        response = MyRequests.post(url, headers=headers, json=valid_car)
        Asseretions.assert_code_status(response, expected_status)

