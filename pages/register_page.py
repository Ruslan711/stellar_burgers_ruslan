from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegisterPage(BasePage):
    """Страница регистрации"""

    name_field = (By.XPATH, "//label[text()='Имя']/following-sibling::input")
    email_field = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    password_field = (By.XPATH, "//input[@type='password']")
    register_button = (By.XPATH, "//form//button")
    login_link = (By.XPATH, "//a[@href='/login']")
    title = (By.XPATH, "//h2[text()='Регистрация']")

    def open(self, base_url: str) -> None:
        """Открыть страницу регистрации"""
        self.driver.get(f"{base_url}/register")
        self.wait_modal_closed()

    def register(self, name: str, email: str, password: str) -> None:
        """Заполнить форму и зарегистрироваться"""
        self.input_text(self.name_field, name)
        self.input_text(self.email_field, email)
        self.input_text(self.password_field, password)
        self.click_register_button()

    def fill_name(self, name: str) -> None:
        """Заполнить поле Имя"""
        self.input_text(self.name_field, name)

    def fill_email(self, email: str) -> None:
        """Заполнить поле Email"""
        self.input_text(self.email_field, email)

    def fill_password(self, password: str) -> None:
        """Заполнить поле Пароль"""
        self.input_text(self.password_field, password)

    def click_register_button(self) -> None:
        """Нажать кнопку регистрации"""
        self.click_element(self.register_button)

    def click_login_link(self) -> None:
        """Перейти ко входу из формы регистрации"""
        self.click_element(self.login_link)

    def is_register_page_opened(self) -> bool:
        """Проверить, что открыта страница регистрации"""
        return self.find_element(self.title).is_displayed()
