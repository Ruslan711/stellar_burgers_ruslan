from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница входа"""

    email_field = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    password_field = (By.XPATH, "//input[@type='password']")
    login_button = (By.XPATH, "//form//button")
    register_link = (By.XPATH, "//a[@href='/register']")
    forgot_password_link = (By.XPATH, "//a[@href='/forgot-password']")
    title = (By.XPATH, "//h2[text()='Вход']")

    def login(self, email: str, password: str) -> None:
        """Авторизоваться по email и паролю"""
        self.input_text(self.email_field, email)
        self.input_text(self.password_field, password)
        self.click_element(self.login_button)

    def click_register_link(self) -> None:
        """Перейти к регистрации"""
        self.click_element(self.register_link)

    def click_forgot_password_link(self) -> None:
        """Перейти к восстановлению пароля"""
        self.click_element(self.forgot_password_link)

    def is_login_page_opened(self) -> bool:
        """Проверить, что открыта страница входа"""
        return self.find_element(self.title).is_displayed()
