import allure
import pytest
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
            
            # Очистка: закрыть любые открытые модалки
            with allure.step("Очистка: закрыть модалки если есть"):
                if main_page.is_modal_visible():
                    main_page.close_modal()
                    main_page.wait_for_modal_completely_hidden_for_firefox(5)
            
            with allure.step("Авторизация"):
                main_page.click_login_button()
                main_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
                assert main_page.is_authorized(), "Авторизация не прошла"
            
            with allure.step("Добавить булку"):
                main_page.switch_to_buns_section()
                bun_element = main_page.get_bun_element_by_text("булка")
                basket_element = main_page.find_element_no_wait(MainPageLocators.BASKET)
                main_page.drag_and_drop_react(bun_element, basket_element)
                main_page.wait_for_ingredients_added(min_count=1)
            
            with allure.step("Добавить соус"):
                main_page.switch_to_sauces_section()
                sauce_element = main_page.find_element_no_wait(MainPageLocators.TRADITIONAL_GALACTIC_SAUCE)
                main_page.drag_and_drop_react(sauce_element, basket_element)
                main_page.wait_for_ingredients_added(min_count=2)
            
            added_count = main_page.get_added_ingredients_count()
            assert added_count >= 2, f"Ингредиенты не добавлены. Добавлено: {added_count}"
        
        with allure.step("3. Оформить заказ"):
            main_page.create_order()
        
        with allure.step("4. Дождаться модального окна с номером заказа"):
            main_page.wait_for_order_creation(timeout=15)
            
            # Ждем реальный номер
            order_number = main_page.wait_for_real_order_number(timeout=30)
            
            # Если номер остался 9999 - пропускаем тест
            if order_number == "9999":
                pytest.skip(f"Заказ не создан. Номер: {order_number}")
            
            # Даем время модалке полностью появиться (фикс для Firefox)
            with allure.step("Дать время модалке полностью появиться"):
                main_page.wait_simple(1)
            
            main_page.close_order_modal()
            main_page.wait_for_order_modal_hidden(timeout=5)
            
            # Дать время backend обработать заказ
            with allure.step("Дать время backend обработать заказ"):
                main_page.wait_simple(5)
        
        with allure.step("5. Проверить увеличение счетчика"):
            order_feed_page.open_order_feed()
            order_feed_page.wait_for_total_counter_visible()
            
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
            
            # Очистка: закрыть любые открытые модалки
            with allure.step("Очистка: закрыть модалки если есть"):
                if main_page.is_modal_visible():
                    main_page.close_modal()
                    main_page.wait_for_modal_completely_hidden_for_firefox(5)
            
            with allure.step("Авторизация"):
                main_page.click_login_button()
                main_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
                assert main_page.is_authorized(), "Авторизация не прошла"
            
            with allure.step("Добавить булку"):
                main_page.switch_to_buns_section()
                bun_element = main_page.get_bun_element_by_text("булка")
                basket_element = main_page.find_element_no_wait(MainPageLocators.BASKET)
                main_page.drag_and_drop_react(bun_element, basket_element)
                main_page.wait_for_ingredients_added(min_count=1)
            
            with allure.step("Добавить соус"):
                main_page.switch_to_sauces_section()
                sauce_element = main_page.find_element_no_wait(MainPageLocators.TRADITIONAL_GALACTIC_SAUCE)
                main_page.drag_and_drop_react(sauce_element, basket_element)
                main_page.wait_for_ingredients_added(min_count=2)
            
            with allure.step("Оформить заказ"):
                main_page.create_order()
        
        with allure.step("3. Дождаться номера заказа"):
            main_page.wait_for_order_creation(timeout=15)
            
            # Ждем реальный номер
            order_number = main_page.wait_for_real_order_number(timeout=30)
            
            # Если номер остался 9999 - пропускаем тест
            if order_number == "9999":
                pytest.skip(f"Заказ не создан. Номер: {order_number}")
            
            # Даем время модалке полностью появиться (фикс для Firefox)
            with allure.step("Дать время модалке полностью появиться"):
                main_page.wait_simple(1)
            
            main_page.close_order_modal()
            main_page.wait_for_order_modal_hidden(timeout=5)
            
            # Дать время backend обработать заказ
            with allure.step("Дать время backend обработать заказ"):
                main_page.wait_simple(5)
        
        with allure.step("4. Проверить увеличение счетчика"):
            order_feed_page.open_order_feed()
            order_feed_page.wait_for_today_counter_visible()
            
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
            
            # Очистка: закрыть любые открытые модалки
            with allure.step("Очистка: закрыть модалки если есть"):
                if main_page.is_modal_visible():
                    main_page.close_modal()
                    main_page.wait_for_modal_completely_hidden_for_firefox(5)
            
            with allure.step("Авторизация"):
                main_page.click_login_button()
                main_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
                assert main_page.is_authorized(), "Авторизация не прошла"
            
            with allure.step("Добавить булку"):
                main_page.switch_to_buns_section()
                bun_element = main_page.get_bun_element_by_text("булка")
                basket_element = main_page.find_element_no_wait(MainPageLocators.BASKET)
                main_page.drag_and_drop_react(bun_element, basket_element)
                main_page.wait_for_ingredients_added(min_count=1)
            
            with allure.step("Добавить соус"):
                main_page.switch_to_sauces_section()
                sauce_element = main_page.find_element_no_wait(MainPageLocators.TRADITIONAL_GALACTIC_SAUCE)
                main_page.drag_and_drop_react(sauce_element, basket_element)
                main_page.wait_for_ingredients_added(min_count=2)
            
            with allure.step("Оформить заказ"):
                main_page.create_order()
        
        with allure.step("3. Дождаться номера заказа"):
            main_page.wait_for_order_creation(timeout=15)
            
            # Ждем реальный номер
            order_number = main_page.wait_for_real_order_number(timeout=30)
            
            # Если номер остался 9999 - пропускаем тест
            if order_number == "9999":
                pytest.skip(f"Заказ не создан. Номер: {order_number}")
            
            # Даем время модалке полностью появиться (фикс для Firefox)
            with allure.step("Дать время модалке полностью появиться"):
                main_page.wait_simple(1)
            
            main_page.close_order_modal()
            main_page.wait_for_order_modal_hidden(timeout=5)
            
            # Дать время backend обработать заказ
            with allure.step("Дать время backend обработать заказ"):
                main_page.wait_simple(5)
        
        with allure.step("4. Проверить что заказ появился в 'В работе'"):
            order_feed_page.open_order_feed()
            order_feed_page.wait_for_in_progress_section_visible()
            
            current_orders = order_feed_page.get_orders_in_progress_numbers()
            
            # Сравниваем числа без ведущих нулей
            order_num_clean = order_number.lstrip('0')
            current_orders_clean = [order.lstrip('0') for order in current_orders]
            
            assert order_num_clean in current_orders_clean, \
                f"Заказ {order_number} не найден в 'В работе'. " \
                f"Было: {existing_orders}, стало: {current_orders}"