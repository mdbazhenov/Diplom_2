import allure
from methods import UserActions

class TestUserLogin:
    @allure.title("Проверка статус-кода при логине существующего пользователя")
    def test_login_existing_user_status_code(self, create_test_user):
        user_data, _ = create_test_user
        response = UserActions.make_request(
            method="POST",
            endpoint="/auth/login",
            json=user_data
        )
        # Проверка статус-кода
        assert response.status_code == 200, "Код ответа должен быть 200 при успешном логине"
        # Проверка содержимого ответа
        response_json = response.json()
        assert isinstance(response_json, dict), "Response is not a valid JSON object"

    @allure.title("Проверка наличия accessToken в ответе при логине существующего пользователя")
    def test_login_existing_user_contains_access_token(self, create_test_user):
        user_data, _ = create_test_user
        response = UserActions.make_request(
            method="POST",
            endpoint="/auth/login",
            json=user_data
        )
        # Проверка наличия accessToken в ответе
        response_json = response.json()
        assert "accessToken" in response_json, "Токен доступа должен присутствовать в ответе"
        # Дополнительная проверка, что токен доступа является строкой
        assert isinstance(response_json["accessToken"], str), "accessToken should be a string"

    @allure.title("Проверка флага успеха при логине существующего пользователя")
    def test_login_existing_user_success_flag(self, create_test_user):
        user_data, _ = create_test_user
        response = UserActions.make_request(
            method="POST",
            endpoint="/auth/login",
            json=user_data
        )
        # Проверка флага успеха
        response_json = response.json()
        assert response_json.get("success") is True, "Поле 'success' должно быть True при успешном логине"

    @allure.title("Проверка статус-кода при неверных данных для логина")
    def test_login_invalid_credentials_status_code(self):
        user_data = {
            "email": "invalid_user@example.com",
            "password": "wrongpassword"
        }
        response = UserActions.make_request(
            method="POST",
            endpoint="/auth/login",
            json=user_data
        )
        # Проверка статус-кода
        assert response.status_code == 401, "Код ответа должен быть 401 при неверных данных"
        # Дополнительная проверка содержимого ответа
        response_json = response.json()
        assert isinstance(response_json, dict), "Response is not a valid JSON object"

    @allure.title("Проверка сообщения об ошибке при неверных данных для логина")
    def test_login_invalid_credentials_error_message(self):
        user_data = {
            "email": "invalid_user@example.com",
            "password": "wrongpassword"
        }
        response = UserActions.make_request(
            method="POST",
            endpoint="/auth/login",
            json=user_data
        )
        # Проверка сообщения об ошибке
        response_json = response.json()
        error_message = response_json.get("message")
        assert error_message == "email or password are incorrect", "Сообщение об ошибке должно быть корректным"



