import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config import Config  # ДОБАВИЛИ ИМПОРТ


def pytest_addoption(parser):
    """Добавляем опцию для выбора браузера"""
    parser.addoption("--browser", action="store", default=Config.BROWSER, help="browser: chrome or firefox")  # ИСПОЛЬЗУЕМ КОНФИГ


@pytest.fixture(scope="function")
def driver(request):
    """Фикстура для создания драйвера"""
    browser_name = request.config.getoption("--browser")
    driver = None
    
    if browser_name == "chrome":
        options = ChromeOptions()
        if Config.HEADLESS:  # ИСПОЛЬЗУЕМ КОНФИГ
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--window-size={Config.WINDOW_SIZE}")  # ИСПОЛЬЗУЕМ КОНФИГ
        
        service = webdriver.ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if Config.HEADLESS:  # ИСПОЛЬЗУЕМ КОНФИГ
            options.add_argument("--headless")
        options.add_argument(f"--width={Config.WINDOW_SIZE.split(',')[0]}")  # ИСПОЛЬЗУЕМ КОНФИГ
        options.add_argument(f"--height={Config.WINDOW_SIZE.split(',')[1]}")  # ИСПОЛЬЗУЕМ КОНФИГ
        
        service = webdriver.FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    
    else:
        raise pytest.UsageError("--browser should be chrome or firefox")
    
    driver.implicitly_wait(Config.IMPLICIT_TIMEOUT)  # ДОБАВИЛИ IMPLICIT WAIT
    yield driver
    driver.quit()

import random
import string

def generate_random_email():
    """Генерирует случайный email"""
    username = ''.join(random.choices(string.ascii_lowercase, k=10))
    return f"test_{username}@example.com"

def generate_random_password():
    """Генерирует случайный пароль"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

@pytest.fixture
def random_user():
    """Фикстура для случайного пользователя"""
    return {
        "email": generate_random_email(),
        "password": generate_random_password()
    }