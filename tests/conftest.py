import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config import Config


@pytest.fixture(params=["chrome", "firefox"], scope="function")
def driver(request):
    """Фикстура для создания драйвера с параметризацией браузеров"""
    browser_name = request.param
    driver = None
    
    if browser_name == "chrome":
        options = ChromeOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--window-size={Config.WINDOW_SIZE}")
        
        service = webdriver.ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        options.add_argument(f"--width={Config.WINDOW_SIZE.split(',')[0]}")
        options.add_argument(f"--height={Config.WINDOW_SIZE.split(',')[1]}")
        
        service = webdriver.FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    
    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser_name}")
    
    driver.implicitly_wait(Config.IMPLICIT_TIMEOUT)
    yield driver
    driver.quit()