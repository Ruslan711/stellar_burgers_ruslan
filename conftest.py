import pytest
import allure
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from typing import Generator

from config.environments import Environment, EnvironmentConfig, environments, print_environment_info
from helpers import UserData, generate_user
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.profile_page import ProfilePage


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", default="chrome", help="chrome/firefox")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--env", default="dev", help="dev/stage")
    parser.addoption("--user-type", default=None)


def create_driver(browser: str, headless: bool) -> WebDriver:
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1280,800")
        return webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1280")
        options.add_argument("--height=800")
        return webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Browser {browser} not supported")


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    browser_driver = create_driver(browser, headless)
    yield browser_driver
    browser_driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,
    call: pytest.CallInfo[None],
) -> Generator[None, None, None]:
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass


def pytest_configure(config: pytest.Config) -> None:
    env_name = config.getoption("--env")
    user_type = config.getoption("--user-type")
    print_environment_info(env_name, user_type)


@pytest.fixture(scope="session")
def env_config(request: pytest.FixtureRequest) -> EnvironmentConfig:
    env_name = request.config.getoption("--env")
    return environments[Environment(env_name)]


@pytest.fixture
def main_page(driver: WebDriver) -> MainPage:
    return MainPage(driver)


@pytest.fixture
def login_page(driver: WebDriver) -> LoginPage:
    return LoginPage(driver)


@pytest.fixture
def register_page(driver: WebDriver) -> RegisterPage:
    return RegisterPage(driver)


@pytest.fixture
def forgot_password_page(driver: WebDriver) -> ForgotPasswordPage:
    return ForgotPasswordPage(driver)


@pytest.fixture
def profile_page(driver: WebDriver) -> ProfilePage:
    return ProfilePage(driver)


@pytest.fixture
def created_user(env_config: EnvironmentConfig) -> Generator[UserData, None, None]:
    """Создать пользователя через API и удалить его после теста"""
    api_url = f"{env_config.url}/api"
    user_data = generate_user()
    response = requests.post(
        f"{api_url}/auth/register",
        json=user_data,
        timeout=20,
    )

    # email из трёх цифр может уже существовать — пробуем другой
    for _ in range(5):
        if response.status_code == 200:
            break
        user_data = generate_user()
        response = requests.post(
            f"{api_url}/auth/register",
            json=user_data,
            timeout=20,
        )

    response.raise_for_status()
    user_data["access_token"] = response.json()["accessToken"]

    yield user_data

    requests.delete(
        f"{api_url}/auth/user",
        headers={"Authorization": user_data["access_token"]},
        timeout=20,
    )


@pytest.fixture
def authorized_user(
    created_user: UserData,
    login_page: LoginPage,
    main_page: MainPage,
    env_config: EnvironmentConfig,
) -> UserData:
    """Подготовить авторизованного пользователя для теста"""
    main_page.open(env_config.url)
    main_page.click_login_button()
    login_page.login(created_user["email"], created_user["password"])
    main_page.find_element(main_page.assemble_title)
    return created_user
