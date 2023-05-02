import json

from requests import Response

from datetime import datetime

class BaseCase:
    def get_cookie(self, response:Response, cookie_name):
        assert cookie_name in response.cookies, f"Ошибка: не могу найти cookie с именем {cookie_name} в последнем ответе"
        return response.cookies[cookie_name]
    def get_header(self, responce:Response, headers_name):
        assert headers_name in responce.headers, f"Ошибка: не могу найти заголовок с именем {headers_name} в последнем ответе"
        return responce.headers[headers_name]
    def get_json_value(self, response:Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Ответ не в Json формате. Ответ текста {response.text}"

        assert name in response_as_dict, f"Ответ Json не является ключем '{name}'"

        return response_as_dict[name]
    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

