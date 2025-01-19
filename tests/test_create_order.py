import allure
from methods import UserActions


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, auth_token, ingredients):
        order_data = {"ingredients": ingredients}
        response = UserActions.send_create_order_request(order_data, auth_token)

        # Проверка статус кода
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        # Проверка наличия ключа "order" в ответе
        response_json = response.json()
        assert "order" in response_json, "Order key is missing in the response"

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, ingredients):
        order_data = {"ingredients": ingredients}
        response = UserActions.send_create_order_request(order_data)

        # Проверка статус кода
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        # Проверка наличия ключа "order" в ответе
        response_json = response.json()
        assert "order" in response_json, "Order key is missing in the response"

    @allure.title("Создание заказа с некорректными ингредиентами")
    def test_create_order_with_invalid_ingredients(self, auth_token):
        invalid_ingredients = ["invalid_hash"]
        order_data = {"ingredients": invalid_ingredients}
        response = UserActions.send_create_order_request(order_data, auth_token)

        # Проверка статус кода
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"

        # Проверка сообщения об ошибке
        response_json = response.json()
        assert response_json.get("message") == "One or more ids provided are incorrect", "Error message is incorrect"

    @allure.title("Создание заказа с пустыми ингредиентами")
    def test_create_order_with_empty_ingredients(self, auth_token):
        order_data = {"ingredients": []}
        response = UserActions.send_create_order_request(order_data, auth_token)

        # Проверка статус кода
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"

        # Проверка сообщения об ошибке
        response_json = response.json()
        assert response_json.get("message") == "Ingredient ids must be provided", "Error message is incorrect"



