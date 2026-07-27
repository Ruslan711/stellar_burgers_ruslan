from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProfilePage(BasePage):
    """Личный кабинет"""

    profile_link = (By.LINK_TEXT, "Профиль")
    logout_button = (By.XPATH, "//button[text()='Выход']")

    def is_profile_opened(self):
        """Проверить, что открыт личный кабинет"""
        return self.find_element(self.profile_link).is_displayed()

    def click_logout(self):
        """Выйти из аккаунта"""
        self.click_element(self.logout_button)
