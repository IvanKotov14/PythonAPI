from testststststs.test_autorization import TestUserRegister

from testststststs.test_registration_object_insurance import TestRegisterObgectInsurent
from testststststs.test_registration_treaty import TestRegisterTreaty

from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
import allure
import pytest

@allure.epic("Кейс обновления данных с системе AgentApp")
class TestRegisterInAgentApp(BaseCase):
    @allure.description("Добовления существующего пользователя с авторизацией в системе AgentApp")
    def test_log_AgentApp(self):
        agriment_id = TestRegisterTreaty().test_log_treaty()
        object_insurance = TestRegisterObgectInsurent().test_log_object_insurance()
        url = f"v1/agreements/{agriment_id}"
        valid_log_AgentApp = {
            "insured_object": object_insurance
        }
        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {token}"
        }
        response = MyRequests.patch(url, headers=headers, json=valid_log_AgentApp)
        Asseretions.assert_code_status(response, 200)
        result = self.get_json_value(response, "id")
        return result

    def test_log_AgentApp_noToken(self):
        agriment_id = TestRegisterTreaty().test_log_treaty()
        url = f"v1/agreements/{agriment_id}"
        object_insurance = TestRegisterObgectInsurent().test_log_object_insurance()
        valid_log_AgentApp = {
            "insured_object": object_insurance
        }
        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": ""
        }

        response = MyRequests.patch(url, headers=headers, json=valid_log_AgentApp)
        Asseretions.assert_code_status(response, 401)
        Asseretions.assert_json_has_not_key(response, "id")

    @pytest.mark.parametrize("object_insuranse", [""," ","12","qw","#$",None,])
    def test_log_AgentApp_invalid(self, object_insuranse):
        agriment_id = TestRegisterTreaty().test_log_treaty()
        url = f"v1/agreements/{agriment_id}"
        valid_log_AgentApp = {
            "insured_object": object_insuranse
        }
        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {token}"
        }
        response = MyRequests.patch(url, headers=headers, json=valid_log_AgentApp)
        Asseretions.assert_code_status(response, 400)
        Asseretions.assert_json_has_not_key(response, "id")