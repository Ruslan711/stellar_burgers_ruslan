import pytest
import allure

from config.environments import EnvironmentConfig
from helpers import generate_user
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

pytestmark = pytest.mark.skip(reason="Сайт недоступен")


@allure.feature("Регистрация")
class TestRegistration:

    @pytest.mark.smoke
    @allure.title("Успешная регистрация")
    def test_successful_registration(
        self,
        env_config: EnvironmentConfig,
        register_page: RegisterPage,
        login_page: LoginPage,
    ) -> None:
        user = generate_user()

        with allure.step("Открыть страницу регистрации"):
            register_page.open(env_config.url)

        with allure.step("Заполнить форму валидными данными"):
            register_page.register(user["name"], user["email"], user["password"])

        with allure.step("Проверить переход на страницу входа"):
            assert login_page.is_login_page_opened()

    @pytest.mark.regression
    @allure.title("Регистрация с пустым именем")
    def test_registration_empty_name(
        self,
        env_config: EnvironmentConfig,
        register_page: RegisterPage,
    ) -> None:
        user = generate_user()

        with allure.step("Открыть страницу регистрации"):
            register_page.open(env_config.url)

        with allure.step("Оставить имя пустым и отправить форму"):
            register_page.fill_email(user["email"])
            register_page.fill_password(user["password"])
            register_page.click_register_button()

        with allure.step("Остаёмся на странице регистрации"):
            assert register_page.is_register_page_opened()
            assert "/register" in register_page.driver.current_url

    @pytest.mark.regression
    @pytest.mark.parametrize("bad_email", [
        "plainemail",
        "test@",
        "test@@yandex.ru",
    ])
    @allure.title("Регистрация с невалидным email: {bad_email}")
    def test_registration_invalid_email(
        self,
        env_config: EnvironmentConfig,
        register_page: RegisterPage,
        bad_email: str,
    ) -> None:
        user = generate_user()

        with allure.step("Открыть страницу регистрации"):
            register_page.open(env_config.url)

        with allure.step(f"Ввести невалидный email: {bad_email}"):
            register_page.fill_name(user["name"])
            register_page.fill_email(bad_email)
            register_page.fill_password(user["password"])
            register_page.click_register_button()

        with allure.step("Остаёмся на странице регистрации"):
            assert register_page.is_register_page_opened()
            assert "/register" in register_page.driver.current_url

    @pytest.mark.regression
    @pytest.mark.parametrize("short_password", ["1", "12345"])
    @allure.title("Регистрация с коротким паролем: {short_password}")
    def test_registration_short_password(
        self,
        env_config: EnvironmentConfig,
        register_page: RegisterPage,
        short_password: str,
    ) -> None:
        user = generate_user()

        with allure.step("Открыть страницу регистрации"):
            register_page.open(env_config.url)

        with allure.step("Ввести пароль меньше 6 символов"):
            register_page.register(user["name"], user["email"], short_password)

        with allure.step("Остаёмся на странице регистрации"):
            assert register_page.is_register_page_opened()
            assert "/register" in register_page.driver.current_url
