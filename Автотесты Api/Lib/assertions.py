from requests import Response
import json
class Asseretions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expented_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в Json формате. Ответ текста '{response.text}'"
        assert name in response_as_dict, f"Ответ Json не содержит ключ 'name'"
        assert response_as_dict[name] == expented_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в Json формате. Ответ текста '{response.text}'"
        assert name in response_as_dict, f"Ответ Json не содержит ключ '{name}'"
    @staticmethod
    def assert_code_status(respose:Response, expected_status_code):
        assert respose.status_code == expected_status_code, f"Ответ статус кода {respose.status_code}, не соответсвует ожидаемому {expected_status_code}"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в Json формате. Ответ текста '{response.text}'"
        assert name not in response_as_dict, f"Ответ Json содержит ключ '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names:list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в Json формате. Ответ текста '{response.text}'"
        for name in names:
            assert name in response_as_dict, f"Ответ Json не содержит ключ '{names}'"


