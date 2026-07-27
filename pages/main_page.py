from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MainPage(BasePage):
    """Главная страница / конструктор"""

    login_button = (By.XPATH, "//button[text()='Войти в аккаунт']")
    personal_account_link = (By.LINK_TEXT, "Личный Кабинет")
    constructor_link = (By.LINK_TEXT, "Конструктор")
    logo_link = (By.XPATH, "//div[contains(@class,'AppHeader_header__logo')]/a")
    buns_tab = (By.XPATH, "//div[contains(@class,'tab_tab')]/span[text()='Булки']/..")
    sauces_tab = (By.XPATH, "//div[contains(@class,'tab_tab')]/span[text()='Соусы']/..")
    fillings_tab = (By.XPATH, "//div[contains(@class,'tab_tab')]/span[text()='Начинки']/..")
    current_tab = (By.XPATH, "//div[contains(@class,'tab_tab_type_current')]")
    assemble_title = (By.XPATH, "//h1[text()='Соберите бургер']")

    def open(self, base_url):
        """Открыть главную страницу"""
        self.driver.get(base_url)

    def click_login_button(self):
        """Нажать 'Войти в аккаунт'"""
        self.click_element(self.login_button)

    def click_personal_account(self):
        """Нажать 'Личный Кабинет'"""
        self.click_element(self.personal_account_link)

    def click_constructor(self):
        """Нажать 'Конструктор'"""
        self.click_element(self.constructor_link)

    def click_logo(self):
        """Нажать на логотип"""
        self.click_element(self.logo_link)

    def click_buns_tab(self):
        """Перейти к разделу Булки"""
        self.click_element(self.buns_tab)

    def click_sauces_tab(self):
        """Перейти к разделу Соусы"""
        self.click_element(self.sauces_tab)

    def click_fillings_tab(self):
        """Перейти к разделу Начинки"""
        self.click_element(self.fillings_tab)

    def get_current_tab_text(self):
        """Получить текст активного раздела"""
        return self.get_text(self.current_tab)

    def is_main_page_opened(self):
        """Проверить, что открыта главная страница"""
        return self.find_element(self.assemble_title).is_displayed()
