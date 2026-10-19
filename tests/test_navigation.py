import pytest
import allure

from config.environments import EnvironmentConfig
from helpers import UserData
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.profile_page import ProfilePage

pytestmark = pytest.mark.skip(reason="Сайт недоступен")


@allure.feature("Навигация")
class TestNavigation:

    @pytest.mark.smoke
    @allure.title("Переход в Личный кабинет")
    def test_open_personal_account(
        self,
        env_config: EnvironmentConfig,
        authorized_user: UserData,
        main_page: MainPage,
        profile_page: ProfilePage,
    ) -> None:
        with allure.step("Нажать 'Личный Кабинет'"):
            main_page.click_personal_account()

        with allure.step("Проверить открытие личного кабинета"):
            profile_page.check_url_contains("/account")
            assert profile_page.is_profile_opened()

    @pytest.mark.regression
    @allure.title("Переход в конструктор по клику на 'Конструктор'")
    def test_go_to_constructor(
        self,
        env_config: EnvironmentConfig,
        authorized_user: UserData,
        main_page: MainPage,
        profile_page: ProfilePage,
    ) -> None:
        with allure.step("Перейти в личный кабинет"):
            main_page.click_personal_account()
            assert profile_page.is_profile_opened()

        with allure.step("Нажать 'Конструктор'"):
            main_page.click_constructor()

        with allure.step("Проверить открытие главной страницы"):
            assert main_page.is_main_page_opened()

    @pytest.mark.regression
    @allure.title("Переход в конструктор по клику на логотип")
    def test_go_to_constructor_by_logo(
        self,
        env_config: EnvironmentConfig,
        authorized_user: UserData,
        main_page: MainPage,
        profile_page: ProfilePage,
    ) -> None:
        with allure.step("Перейти в личный кабинет"):
            main_page.click_personal_account()
            assert profile_page.is_profile_opened()

        with allure.step("Нажать на логотип"):
            main_page.click_logo()

        with allure.step("Проверить открытие главной страницы"):
            assert main_page.is_main_page_opened()

    @pytest.mark.smoke
    @allure.title("Выход через кнопку 'Выход' в личном кабинете")
    def test_logout(
        self,
        env_config: EnvironmentConfig,
        authorized_user: UserData,
        main_page: MainPage,
        profile_page: ProfilePage,
        login_page: LoginPage,
    ) -> None:
        with allure.step("Перейти в личный кабинет"):
            main_page.click_personal_account()
            assert profile_page.is_profile_opened()

        with allure.step("Нажать кнопку выхода"):
            profile_page.click_logout()

        with allure.step("Проверить переход на страницу входа"):
            assert login_page.is_login_page_opened()
