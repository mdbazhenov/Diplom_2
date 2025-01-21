import requests
import allure
from data import BASE_URL, HEADERS
from methods import ResponseValidator


class TestGetUserOrders:

    @allure.title("Проверка статус-кода при получении заказов авторизованным пользователем")
    def test_get_orders_authorized_user_status_code(self, auth_token):
        headers = {**HEADERS, "Authorization": auth_token}
        response = requests.get(f"{BASE_URL}/orders", headers=headers)

        # Проверка статус кода
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        # Дополнительная проверка содержимого ответа
        response_json = response.json()
        assert isinstance(response_json, dict), "Response is not a valid JSON object"

    @allure.title("Проверка наличия ключа 'orders' в ответе для авторизованного пользователя")
    def test_get_orders_authorized_user_key_in_response(self, auth_token):
        headers = {**HEADERS, "Authorization": auth_token}
        response = requests.get(f"{BASE_URL}/orders", headers=headers)

        # Проверка наличия ключа "orders" в ответе
        response_json = response.json()
        assert "orders" in response_json, "'orders' key is missing in the response"

        # Дополнительная проверка, чтобы убедиться, что orders — это список
        assert isinstance(response_json["orders"], list), "'orders' is not a list"

    @allure.title("Проверка статус-кода при получении заказов неавторизованным пользователем")
    def test_get_orders_unauthorized_user_status_code(self):
        response = requests.get(f"{BASE_URL}/orders", headers=HEADERS)

        # Проверка статус кода
        assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}"

        # Проверка сообщения об ошибке
        response_json = response.json()
        assert response_json.get("message") == "You should be authorised", "Error message is incorrect"

    @allure.title("Проверка сообщения об ошибке при попытке получения заказов неавторизованным пользователем")
    def test_get_orders_unauthorized_user_message(self):
        response = requests.get(f"{BASE_URL}/orders", headers=HEADERS)

        # Проверка сообщения об ошибке
        response_json = response.json()
        assert response_json.get("message") == "You should be authorised", "Error message is incorrect"





