from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RegisterPage(BasePage):
    """Страница регистрации"""

    name_field = (By.XPATH, "//label[text()='Имя']/following-sibling::input")
    email_field = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    password_field = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")
    register_button = (By.XPATH, "//button[text()='Зарегистрироваться']")
    login_link = (By.LINK_TEXT, "Войти")
    error_message = (By.XPATH, "//p[contains(@class,'input__error')]")
    title = (By.XPATH, "//h2[text()='Регистрация']")

    def open(self, base_url):
        """Открыть страницу регистрации"""
        self.driver.get(f"{base_url}/register")

    def register(self, name, email, password):
        """Заполнить форму и зарегистрироваться"""
        self.input_text(self.name_field, name)
        self.input_text(self.email_field, email)
        self.input_text(self.password_field, password)
        self.click_element(self.register_button)

    def fill_name(self, name):
        """Заполнить поле Имя"""
        self.input_text(self.name_field, name)

    def fill_email(self, email):
        """Заполнить поле Email"""
        self.input_text(self.email_field, email)

    def fill_password(self, password):
        """Заполнить поле Пароль"""
        self.input_text(self.password_field, password)

    def click_register_button(self):
        """Нажать кнопку регистрации"""
        self.click_element(self.register_button)

    def click_login_link(self):
        """Перейти ко входу из формы регистрации"""
        self.click_element(self.login_link)

    def get_error_text(self):
        """Получить текст ошибки"""
        return self.get_text(self.error_message)

    def is_register_page_opened(self):
        """Проверить, что открыта страница регистрации"""
        return self.find_element(self.title).is_displayed()
