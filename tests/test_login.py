import pytest
import allure

from config.environments import EnvironmentConfig
from helpers import UserData
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.register_page import RegisterPage

pytestmark = pytest.mark.skip(reason="Сайт недоступен")


@allure.feature("Авторизация")
class TestLogin:

    @pytest.mark.smoke
    @allure.title("Вход через кнопку 'Войти в аккаунт' на главной")
    def test_login_from_main_page(
        self,
        env_config: EnvironmentConfig,
        created_user: UserData,
        main_page: MainPage,
        login_page: LoginPage,
    ) -> None:
        with allure.step("Открыть главную страницу"):
            main_page.open(env_config.url)

        with allure.step("Нажать 'Войти в аккаунт'"):
            main_page.click_login_button()

        with allure.step("Авторизоваться"):
            login_page.login(created_user["email"], created_user["password"])

        with allure.step("Проверить успешный вход"):
            assert main_page.is_main_page_opened()

    @pytest.mark.smoke
    @allure.title("Вход через кнопку 'Личный кабинет'")
    def test_login_from_personal_account(
        self,
        env_config: EnvironmentConfig,
        created_user: UserData,
        main_page: MainPage,
        login_page: LoginPage,
    ) -> None:
        with allure.step("Открыть главную страницу"):
            main_page.open(env_config.url)

        with allure.step("Нажать 'Личный Кабинет'"):
            main_page.click_personal_account()

        with allure.step("Авторизоваться"):
            login_page.login(created_user["email"], created_user["password"])

        with allure.step("Проверить успешный вход"):
            assert main_page.is_main_page_opened()

    @pytest.mark.regression
    @allure.title("Вход через кнопку в форме регистрации")
    def test_login_from_register_form(
        self,
        env_config: EnvironmentConfig,
        created_user: UserData,
        register_page: RegisterPage,
        login_page: LoginPage,
        main_page: MainPage,
    ) -> None:
        with allure.step("Открыть страницу регистрации"):
            register_page.open(env_config.url)

        with allure.step("Нажать 'Войти'"):
            register_page.click_login_link()

        with allure.step("Авторизоваться"):
            login_page.login(created_user["email"], created_user["password"])

        with allure.step("Проверить успешный вход"):
            assert main_page.is_main_page_opened()

    @pytest.mark.regression
    @allure.title("Вход через кнопку в форме восстановления пароля")
    def test_login_from_forgot_password(
        self,
        env_config: EnvironmentConfig,
        created_user: UserData,
        forgot_password_page: ForgotPasswordPage,
        login_page: LoginPage,
        main_page: MainPage,
    ) -> None:
        with allure.step("Открыть страницу восстановления пароля"):
            forgot_password_page.open(env_config.url)

        with allure.step("Нажать 'Войти'"):
            forgot_password_page.click_login_link()

        with allure.step("Авторизоваться"):
            login_page.login(created_user["email"], created_user["password"])

        with allure.step("Проверить успешный вход"):
            assert main_page.is_main_page_opened()
