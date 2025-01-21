import random
import string
import allure

class Helper:

    @staticmethod
    @allure.step("Генерация уникального email")
    def generate_unique_email():
        """Генерирует уникальный email"""
        return f"test_{''.join(random.choices(string.ascii_lowercase, k=8))}@example.com"

    @staticmethod
    @allure.step("Получение данных пользователя")
    def get_user_data():
        # Нужно создать новые данные пользователя с уникальным email
        return {
            "email": Helper.generate_unique_email(),
            "password": "testpass123",
            "name": "Test User"
        }
