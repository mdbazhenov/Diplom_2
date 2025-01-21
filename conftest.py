import pytest
import requests
from data import BASE_URL, HEADERS
from helpers import Helper
from methods import UserActions

@pytest.fixture
def auth_token():
    user_data = Helper.get_user_data()  # Получаем данные пользователя из data.py
    UserActions.register_user(user_data)  # Регистрируем пользователя
    response = UserActions.login_user(user_data)  # Логиним пользователя
    response_json = response.json()  # Извлекаем JSON из ответа
    return response_json["accessToken"]  # Возвращаем токен


@pytest.fixture
def authorized_headers(auth_token):
    return {**HEADERS, "Authorization": f"Bearer {auth_token}"}
@pytest.fixture
def ingredients():
    response = requests.get(f"{BASE_URL}/ingredients", headers=HEADERS)
    return [ingredient["_id"] for ingredient in response.json().get("data", [])]
@pytest.fixture
def create_test_user():
    user_data = Helper.get_user_data()
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data, headers=HEADERS)
    access_token = response.json().get("accessToken")
    yield user_data, access_token
    delete_response = requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": f"Bearer {access_token}"})
    if delete_response.status_code != 200:
        print(f"Failed to delete test user: {delete_response.status_code}, {delete_response.json()}")
