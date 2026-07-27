from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница входа"""

    email_field = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    password_field = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")
    login_button = (By.XPATH, "//button[text()='Войти']")
    register_link = (By.LINK_TEXT, "Зарегистрироваться")
    forgot_password_link = (By.LINK_TEXT, "Восстановить пароль")
    title = (By.XPATH, "//h2[text()='Вход']")

    def login(self, email, password):
        """Авторизоваться по email и паролю"""
        self.input_text(self.email_field, email)
        self.input_text(self.password_field, password)
        self.click_element(self.login_button)

    def click_register_link(self):
        """Перейти к регистрации"""
        self.click_element(self.register_link)

    def click_forgot_password_link(self):
        """Перейти к восстановлению пароля"""
        self.click_element(self.forgot_password_link)

    def is_login_page_opened(self):
        """Проверить, что открыта страница входа"""
        return self.find_element(self.title).is_displayed()
