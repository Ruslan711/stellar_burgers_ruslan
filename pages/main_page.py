from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MainPage(BasePage):
    """Главная страница / конструктор"""

    login_button = (By.XPATH, "//button[normalize-space()='Войти в аккаунт']")
    personal_account_link = (By.XPATH, "//a[contains(@href,'/account')]")
    constructor_link = (By.XPATH, "//p[text()='Конструктор']/ancestor::a")
    logo_link = (By.XPATH, "//div[contains(@class,'AppHeader_header__logo')]/a")
    buns_tab = (By.XPATH, "//div[contains(@class,'tab_tab')]/span[text()='Булки']/..")
    sauces_tab = (By.XPATH, "//div[contains(@class,'tab_tab')]/span[text()='Соусы']/..")
    fillings_tab = (By.XPATH, "//div[contains(@class,'tab_tab')]/span[text()='Начинки']/..")
    current_tab = (By.XPATH, "//div[contains(@class,'tab_tab_type_current')]")
    ingredients_container = (
        By.XPATH,
        "//div[contains(@class,'BurgerIngredients_ingredients__menuContainer')]",
    )
    buns_title = (By.XPATH, "//h2[text()='Булки']")
    sauces_title = (By.XPATH, "//h2[text()='Соусы']")
    fillings_title = (By.XPATH, "//h2[text()='Начинки']")
    assemble_title = (By.XPATH, "//h1[text()='Соберите бургер']")

    def open(self, base_url: str) -> None:
        """Открыть главную страницу"""
        self.driver.get(base_url)
        self.wait_modal_closed()

    def click_login_button(self) -> None:
        """Нажать 'Войти в аккаунт'"""
        self.click_element(self.login_button)

    def click_personal_account(self) -> None:
        """Нажать 'Личный Кабинет'"""
        self.click_element(self.personal_account_link)

    def click_constructor(self) -> None:
        """Нажать 'Конструктор'"""
        self.click_element(self.constructor_link)

    def click_logo(self) -> None:
        """Нажать на логотип"""
        self.click_element(self.logo_link)

    def click_buns_tab(self) -> None:
        """Перейти к разделу Булки"""
        self.select_tab(self.buns_tab, self.buns_title)

    def click_sauces_tab(self) -> None:
        """Перейти к разделу Соусы"""
        self.select_tab(self.sauces_tab, self.sauces_title)

    def click_fillings_tab(self) -> None:
        """Перейти к разделу Начинки"""
        self.select_tab(self.fillings_tab, self.fillings_title)

    def select_tab(
        self,
        tab: tuple[str, str],
        section_title: tuple[str, str],
    ) -> None:
        """Нажать на вкладку и дождаться окончания прокрутки к разделу"""
        self.click_element(tab)
        self.wait.until(lambda driver: self.is_section_at_top(section_title))
        self.wait.until(
            lambda driver: "tab_tab_type_current"
            in driver.find_element(*tab).get_attribute("class")
        )

    def is_section_at_top(self, section_title: tuple[str, str]) -> bool:
        """Проверить, что заголовок раздела прокручен к верху списка ингредиентов"""
        container_top = self.find_element(self.ingredients_container).location["y"]
        title_top = self.find_element(section_title).location["y"]
        return abs(title_top - container_top) <= 2

    def get_current_tab_text(self) -> str:
        """Получить текст активного раздела"""
        return self.get_text(self.current_tab)

    def is_main_page_opened(self) -> bool:
        """Проверить, что открыта главная страница"""
        return self.find_element(self.assemble_title).is_displayed()
