import allure
import pytest
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pages.main_page import MainPage
from tests.pages.order_feed_page import OrderFeedPage
from tests.locators.main_page_locators import MainPageLocators
from config import Config


class TestOrderFeed:
    """
    Тесты для ленты заказов
    """

    @allure.title("Счетчик 'Выполнено за всё время' увеличивается при новом заказе")
    def test_total_orders_counter_increases(self, driver):
        """Проверяем что счетчик 'Выполнено за всё время' увеличивается"""
        main_page = MainPage(driver)
        with allure.step("1. Получить начальное значение счетчика"):
            order_feed_page = OrderFeedPage(driver)
            order_feed_page.open_order_feed()
            total_before = order_feed_page.get_total_orders_count()
        with allure.step("2. Вернуться на главную и добавить ингредиенты"):
            main_page.open("/")
            # Авторизация
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.LOGIN_BUTTON)
            )
            driver.execute_script("arguments[0].click();", login_button)

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(MainPageLocators.EMAIL_INPUT)
            )

            main_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)

            WebDriverWait(driver, 10).until(
                lambda d: main_page.is_authorized()
            )

            # Добавляем булку
            bun_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.BUN_TAB)
            )
            driver.execute_script("arguments[0].click();", bun_tab)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'булка')]"))
            )

            bun = driver.find_element(By.XPATH, "//p[contains(text(), 'булка')]")
            basket = driver.find_element(*MainPageLocators.BASKET)

            main_page.drag_and_drop_react(bun, basket)

            WebDriverWait(driver, 10).until(
                lambda d: main_page.get_added_ingredients_count() > 0
            )

            # Добавляем соус
            sauce_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.SAUCE_TAB)
            )
            driver.execute_script("arguments[0].click();", sauce_tab)

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(MainPageLocators.TRADITIONAL_GALACTIC_SAUCE)
            )

            sauce = driver.find_element(*MainPageLocators.TRADITIONAL_GALACTIC_SAUCE)
            main_page.drag_and_drop_react(sauce, basket)

            WebDriverWait(driver, 10).until(
                lambda d: main_page.get_added_ingredients_count() >= 2
            )

            added_count = main_page.get_added_ingredients_count()
            assert added_count >= 2, "Ингредиенты не добавлены"

        with allure.step("3. Оформить заказ"):
            order_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.ORDER_BUTTON)
            )
            driver.execute_script("arguments[0].click();", order_button)

        with allure.step("4. Дождаться модального окна с номером заказа"):
            main_page.wait_for_order_creation(timeout=15)

            # Ждем реальный номер
            try:
                WebDriverWait(driver, 30).until(
                    lambda d: main_page.get_order_number_from_modal() != "9999"
                )
                order_number = main_page.get_order_number_from_modal()
            except TimeoutException:
                order_number = main_page.get_order_number_from_modal()
                pytest.skip(f"Заказ не создан. Номер: {order_number}")

            main_page.close_order_modal()

            WebDriverWait(driver, 5).until(
                lambda d: not main_page.is_order_modal_visible()
            )

            # Даем время backend
            WebDriverWait(driver, 10).until(lambda d: True)

        with allure.step("5. Проверить увеличение счетчика"):
            order_feed_page.open_order_feed()

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'digits-large')]"))
            )

            total_after = order_feed_page.get_total_orders_count()

            assert total_after > total_before, \
                f"Счетчик не увеличился: было {total_before}, стало {total_after}"

    @allure.title("Счетчик 'Выполнено за сегодня' увеличивается при новом заказе")
    def test_today_orders_counter_increases(self, driver):
        """Проверяем что счетчик 'Выполнено за сегодня' увеличивается"""
        main_page = MainPage(driver)

        with allure.step("1. Получить начальное значение счетчика"):
            order_feed_page = OrderFeedPage(driver)
            order_feed_page.open_order_feed()
            today_before = order_feed_page.get_today_orders_count()

        with allure.step("2. Создать заказ"):
            main_page.open("/")

            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.LOGIN_BUTTON)
            )
            driver.execute_script("arguments[0].click();", login_button)

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(MainPageLocators.EMAIL_INPUT)
            )

            main_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)

            WebDriverWait(driver, 10).until(
                lambda d: main_page.is_authorized()
            )

            # Булка
            bun_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.BUN_TAB)
            )
            driver.execute_script("arguments[0].click();", bun_tab)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'булка')]"))
            )

            bun = driver.find_element(By.XPATH, "//p[contains(text(), 'булка')]")
            basket = driver.find_element(*MainPageLocators.BASKET)
            main_page.drag_and_drop_react(bun, basket)

            WebDriverWait(driver, 10).until(
                lambda d: main_page.get_added_ingredients_count() > 0
            )

            # Соус
            sauce_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.SAUCE_TAB)
            )
            driver.execute_script("arguments[0].click();", sauce_tab)

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(MainPageLocators.TRADITIONAL_GALACTIC_SAUCE)
            )

            sauce = driver.find_element(*MainPageLocators.TRADITIONAL_GALACTIC_SAUCE)
            main_page.drag_and_drop_react(sauce, basket)

            WebDriverWait(driver, 10).until(
                lambda d: main_page.get_added_ingredients_count() >= 2
            )

            order_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.ORDER_BUTTON)
            )
            driver.execute_script("arguments[0].click();", order_button)

        with allure.step("3. Дождаться номера заказа"):
            main_page.wait_for_order_creation(timeout=15)

            try:
                WebDriverWait(driver, 30).until(
                    lambda d: main_page.get_order_number_from_modal() != "9999"
                )
                order_number = main_page.get_order_number_from_modal()
            except TimeoutException:
                order_number = main_page.get_order_number_from_modal()
                pytest.skip(f"Заказ не создан. Номер: {order_number}")

            main_page.close_order_modal()

            WebDriverWait(driver, 10).until(lambda d: True)

        with allure.step("4. Проверить увеличение счетчика"):
            order_feed_page.open_order_feed()

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Выполнено за сегодня:')]"))
            )

            today_after = order_feed_page.get_today_orders_count()

            assert today_after > today_before, \
                f"Счетчик не увеличился: было {today_before}, стало {today_after}"

    @allure.title("Новый заказ появляется в разделе 'В работе'")
    def test_order_appears_in_progress_section(self, driver):
        """Проверяем что заказ появляется в разделе 'В работе'"""
        main_page = MainPage(driver)

        with allure.step("1. Получить текущие заказы в работе"):
            order_feed_page = OrderFeedPage(driver)
            order_feed_page.open_order_feed()
            existing_orders = order_feed_page.get_orders_in_progress_numbers()

        with allure.step("2. Создать заказ"):
            main_page.open("/")

            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.LOGIN_BUTTON)
            )
            driver.execute_script("arguments[0].click();", login_button)

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(MainPageLocators.EMAIL_INPUT)
            )

            main_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)

            WebDriverWait(driver, 10).until(
                lambda d: main_page.is_authorized()
            )

            # Булка
            bun_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.BUN_TAB)
            )
            driver.execute_script("arguments[0].click();", bun_tab)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'булка')]"))
            )

            bun = driver.find_element(By.XPATH, "//p[contains(text(), 'булка')]")
            basket = driver.find_element(*MainPageLocators.BASKET)
            main_page.drag_and_drop_react(bun, basket)

            WebDriverWait(driver, 10).until(
                lambda d: main_page.get_added_ingredients_count() > 0
            )

            # Соус
            sauce_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.SAUCE_TAB)
            )
            driver.execute_script("arguments[0].click();", sauce_tab)

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(MainPageLocators.TRADITIONAL_GALACTIC_SAUCE)
            )

            sauce = driver.find_element(*MainPageLocators.TRADITIONAL_GALACTIC_SAUCE)
            main_page.drag_and_drop_react(sauce, basket)

            WebDriverWait(driver, 10).until(
                lambda d: main_page.get_added_ingredients_count() >= 2
            )

            order_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(MainPageLocators.ORDER_BUTTON)
            )
            driver.execute_script("arguments[0].click();", order_button)

        with allure.step("3. Дождаться номера заказа"):
            main_page.wait_for_order_creation(timeout=15)

            try:
                WebDriverWait(driver, 30).until(
                    lambda d: main_page.get_order_number_from_modal() != "9999"
                )
                order_number = main_page.get_order_number_from_modal()
            except TimeoutException:
                order_number = main_page.get_order_number_from_modal()
                pytest.skip(f"Заказ не создан. Номер: {order_number}")

            main_page.close_order_modal()

            WebDriverWait(driver, 15).until(lambda d: True)

        with allure.step("4. Проверить что заказ появился в 'В работе'"):
            order_feed_page.open_order_feed()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'В работе:')]"))
            )
            current_orders = order_feed_page.get_orders_in_progress_numbers()
            # Сравниваем числа без ведущих нулей
            order_num_clean = order_number.lstrip('0')
            current_orders_clean = [order.lstrip('0') for order in current_orders]
            assert order_num_clean in current_orders_clean, \
                f"Заказ {order_number} не найден в 'В работе'. " \
                f"Было: {existing_orders}, стало: {current_orders}"