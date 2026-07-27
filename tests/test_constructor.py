import pytest
import allure


@allure.feature("Конструктор")
class TestConstructor:

    @pytest.mark.smoke
    @allure.title("Переход к разделу 'Булки'")
    def test_open_buns_section(self, env_config, main_page):
        with allure.step("Открыть главную страницу"):
            main_page.open(env_config.url)

        with allure.step("Сначала открыть другой раздел"):
            main_page.click_sauces_tab()

        with allure.step("Нажать на 'Булки'"):
            main_page.click_buns_tab()

        with allure.step("Проверить, что активен раздел Булки"):
            assert "Булки" in main_page.get_current_tab_text()

    @pytest.mark.regression
    @allure.title("Переход к разделу 'Соусы'")
    def test_open_sauces_section(self, env_config, main_page):
        with allure.step("Открыть главную страницу"):
            main_page.open(env_config.url)

        with allure.step("Нажать на 'Соусы'"):
            main_page.click_sauces_tab()

        with allure.step("Проверить, что активен раздел Соусы"):
            assert "Соусы" in main_page.get_current_tab_text()

    @pytest.mark.regression
    @allure.title("Переход к разделу 'Начинки'")
    def test_open_fillings_section(self, env_config, main_page):
        with allure.step("Открыть главную страницу"):
            main_page.open(env_config.url)

        with allure.step("Нажать на 'Начинки'"):
            main_page.click_fillings_tab()

        with allure.step("Проверить, что активен раздел Начинки"):
            assert "Начинки" in main_page.get_current_tab_text()
