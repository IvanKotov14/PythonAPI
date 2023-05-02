from testststststs.test_autorization import TestUserRegister

from testststststs.test_refistation_in_AgentApp import TestRegisterInAgentApp

from Lib.assertions import Asseretions

from Lib.base_case import BaseCase
from Lib.my_requests import MyRequests
import allure
import pytest


@allure.epic("Получение полного расчёт по СК")
class TestReceivingAnAward(BaseCase):
    @allure.description("Получения полного расчета")
    def test_log_receiving_an_award(self):
        agriment_id = TestRegisterInAgentApp().test_log_AgentApp()
        url = f"v1/agreements/{agriment_id}/results/TEST_COMPANY"
        receiving_an_award = {
            "agreement_id": agriment_id,
            "ins_company_code": "TEST_COMPANY"
        }
        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {token}"
        }
        response = MyRequests.post(url, headers=headers, json=receiving_an_award)
        Asseretions.assert_code_status(response, 200)

    @allure.description("Нигативный тест на получения расчета")
    @pytest.mark.parametrize("agriment_id", [""," ","12","qw","#$",None,])
    def test_log_receiving_an_award_invalid(self, agriment_id):
        url = f"v1/agreements/{agriment_id}/results/TEST_COMPANY"
        receiving_an_award = {
            "agreement_id": agriment_id,
            "ins_company_code": "TEST_COMPANY"
        }
        token = TestUserRegister().test_get_user_auth()
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {token}"
        }
        response = MyRequests.post(url, headers=headers, json=receiving_an_award)
        Asseretions.assert_code_status(response, 404)