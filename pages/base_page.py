import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Базовый класс для всех страниц"""

    modal_overlay = (By.XPATH, "//div[contains(@class,'Modal_modal_overlay')]")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_modal_closed(self) -> None:
        """Дождаться закрытия оверлея модалки"""
        self.wait.until(EC.invisibility_of_element_located(self.modal_overlay))
        # Firefox: скрытый overlay может перехватывать клик
        self.driver.execute_script(
            """
            document.querySelectorAll('[class*="Modal_modal_overlay"]').forEach(function(el) {
                el.style.pointerEvents = 'none';
            });
            """
        )

    def find_element(self, locator: tuple[str, str]) -> WebElement:
        """Найти элемент с явным ожиданием"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click_element(self, locator: tuple[str, str]) -> None:
        """Нажать на элемент с явным ожиданием кликабельности"""
        self.wait_modal_closed()
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element,
        )
        element.click()

    def input_text(self, locator: tuple[str, str], text: str) -> None:
        """Ввести текст в элемент"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple[str, str]) -> str:
        """Получить текст элемента"""
        return self.find_element(locator).text

    def check_url_contains(self, text: str) -> None:
        """Проверка, что URL содержит текст"""
        self.wait.until(EC.url_contains(text))

    def attach_screenshot(self, name: str = "screenshot") -> None:
        """Сделать скриншот и прикрепить к отчету Allure."""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
