from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    """Страница восстановления пароля"""

    login_link = (By.LINK_TEXT, "Войти")
    title = (By.XPATH, "//h2[text()='Восстановление пароля']")

    def open(self, base_url):
        """Открыть страницу восстановления пароля"""
        self.driver.get(f"{base_url}/forgot-password")

    def click_login_link(self):
        """Перейти ко входу из формы восстановления"""
        self.click_element(self.login_link)

    def is_forgot_password_page_opened(self):
        """Проверить, что открыта страница восстановления пароля"""
        return self.find_element(self.title).is_displayed()
