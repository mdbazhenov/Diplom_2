import requests
import random
import string
from data import BASE_URL, HEADERS
from helpers import Helper
import allure



class UserActions:

    @staticmethod
    @allure.step("Регистрируем пользователя")
    def register_user(data=None):
        """
        Регистрирует пользователя. Если данные не переданы, использует метод get_user_data().
        """
        if data is None:
            data = Helper.get_user_data()  # Используем метод для получения данных
        response = requests.post(f"{BASE_URL}/auth/register", json=data, headers=HEADERS)
        if response.status_code != 200:
            error_message = response.json().get("message", "Unknown error")
            raise ValueError(f"Failed to register user: {response.status_code}, {error_message}")
        return response

    @staticmethod
    @allure.step("Авторизация пользователя")
    def login_user(login_data=None):
        """
        Авторизует пользователя. Если данные не переданы, используются данные из файла data.py.
        """
        if login_data is None:
            login_data = Helper.get_user_data()  # Используем метод для получения данных
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, headers=HEADERS)
        if response.status_code != 200:
            raise ValueError(
                f"Failed to log in: {response.status_code}, {response.json().get('message', 'Unknown error')}"
            )
        return response

    @staticmethod
    @allure.step("Отправка запроса")
    def make_request(method, endpoint, **kwargs):
        url = f"{BASE_URL}{endpoint}"
        headers = kwargs.pop("headers", HEADERS)
        response = requests.request(method, url, headers=headers, **kwargs)
        return response

    @staticmethod
    @allure.step("Обновляем данные пользователя")
    def update_user_data(auth_token, update_data):
        headers = {**HEADERS, "Authorization": auth_token}
        response = requests.patch(f"{BASE_URL}/auth/user", json=update_data, headers=headers)
        return response


    @staticmethod
    @allure.step("Создаем заказ")
    def send_create_order_request(order_data, auth_token=None):
        headers = {**HEADERS}
        if auth_token:
            headers["Authorization"] = auth_token

        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
        return response


class ResponseValidator:

    @staticmethod
    @allure.step("Проверка статус-кода")
    def check_status_code(response, expected_code, expected_message=None):
        if isinstance(response, requests.Response):
            actual_status_code = response.status_code
        elif isinstance(response, dict):
            actual_status_code = 200 if response.get('success') else 400  # Пример: если success = True, код 200
        else:
            raise TypeError(f"Unsupported response type: {type(response)}")

        assert actual_status_code == expected_code, \
            f"Expected status {expected_code}, but got {actual_status_code}"

        if expected_message:
            actual_message = response.get('message', '')
            assert actual_message == expected_message, \
                f"Expected message: {expected_message}, but got {actual_message}"

    @staticmethod
    @allure.step("Проверка наличия ключа в ответе")
    def check_key_in_response(response, key):
        assert key in response.json(), f"Response does not contain key: {key}"

    @staticmethod
    @allure.step("Проверка сообщения в ответе")
    def check_message_in_response(response, expected_message):
        assert response.json()[
                   "message"] == expected_message, f"Expected message '{expected_message}', but got {response.json()['message']}"
