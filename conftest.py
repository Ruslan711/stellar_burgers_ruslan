import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.environments import Environment, environments, common_users, print_environment_info
from helpers import generate_user
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.profile_page import ProfilePage


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="chrome/firefox")
    parser.addoption("--headless", action="store_true")
    parser.addoption("--env", default="dev", help="dev/stage")
    parser.addoption("--user-type", default=None)


def create_driver(browser: str, headless: bool):
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
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1280, 800)
        return driver
    else:
        raise ValueError(f"Browser {browser} not supported")


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    driver = create_driver(browser, headless)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )


def pytest_configure(config):
    env_name = config.getoption("--env")
    user_type = config.getoption("--user-type")
    print_environment_info(env_name, user_type)


@pytest.fixture(scope="session")
def env_config(request):
    env_name = request.config.getoption("--env")
    return environments[Environment(env_name)]


@pytest.fixture(scope="function")
def user(request, env_config):
    user_type = request.config.getoption("--user-type") or env_config.default_user
    return common_users[user_type]


@pytest.fixture
def main_page(driver):
    return MainPage(driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def register_page(driver):
    return RegisterPage(driver)


@pytest.fixture
def forgot_password_page(driver):
    return ForgotPasswordPage(driver)


@pytest.fixture
def profile_page(driver):
    return ProfilePage(driver)


@pytest.fixture
def created_user(driver, env_config, register_page, login_page):
    """Создать нового пользователя через UI"""
    user_data = generate_user()
    register_page.open(env_config.url)
    register_page.register(user_data["name"], user_data["email"], user_data["password"])
    assert login_page.is_login_page_opened(), "После регистрации должна открыться страница входа"
    return user_data


@pytest.fixture
def authorized_user(driver, env_config, created_user, login_page, main_page):
    """Авторизованный пользователь"""
    login_page.login(created_user["email"], created_user["password"])
    assert main_page.is_main_page_opened(), "Не удалось авторизоваться"
    return created_user
