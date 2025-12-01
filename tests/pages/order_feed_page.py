import allure
from .base_page import BasePage
from tests.locators.order_feed_locators import OrderFeedLocators


class OrderFeedPage(BasePage):
   
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/feed"
    
    @allure.step("Открыть страницу ленты заказов")
    def open_order_feed(self):
        """Открывает страницу ленты заказов"""
        self.open(self.url)
    
    @allure.step("Получить счетчик 'Выполнено за всё время'")
    def get_total_orders_count(self):
        """Возвращает счетчик 'Выполнено за всё время'"""
        count_text = self.get_element_text(OrderFeedLocators.TOTAL_ORDERS_COUNT)
        return int(count_text)

    @allure.step("Получить счетчик 'Выполнено за сегодня'")
    def get_today_orders_count(self):
        """Возвращает счетчик 'Выполнено за сегодня'"""
        count_text = self.get_element_text(OrderFeedLocators.TODAY_ORDERS_COUNT)
        return int(count_text)
    
    @allure.step("Проверить есть ли заказы в работе")
    def has_orders_in_progress(self):
        """Проверяет есть ли заказы в разделе 'В работе'"""
        try:
            elements = self.find_elements(OrderFeedLocators.ORDER_NUMBERS_IN_PROGRESS)
            if not elements:
                return False
            
            # Берем первый элемент
            text = elements[0].text.strip()
            
            # Если это текст "Все текущие заказы готовы" - значит нет заказов
            if "Все текущие заказы готовы" in text:
                return False
            
            # Если это номер заказа
            if text.isdigit():
                return True
            
            return False
        except:
            return False
    
    @allure.step("Получить количество заказов в работе")
    def get_orders_in_progress_count(self):
        """Возвращает количество заказов в работе"""
        if not self.has_orders_in_progress():
            return 0
        
        elements = self.find_elements(OrderFeedLocators.ORDER_NUMBERS_IN_PROGRESS)
        count = 0
        for element in elements:
            if element.text.strip().isdigit():
                count += 1
        return count
    
    @allure.step("Получить номера заказов в работе")
    def get_orders_in_progress_numbers(self):
        """Возвращает список номеров заказов в работе"""
        if not self.has_orders_in_progress():
            return []
        
        elements = self.find_elements(OrderFeedLocators.ORDER_NUMBERS_IN_PROGRESS)
        orders = []
        
        for element in elements:
            text = element.text.strip()
            if text.isdigit():
                orders.append(text)
        
        return orders
    
    @allure.step("Проверить что раздел 'В работе' отображается")
    def is_orders_in_progress_visible(self):
        """Проверяет что раздел 'В работе' отображается"""
        return self.is_element_visible(OrderFeedLocators.ORDERS_IN_PROGRESS_SECTION)
    
    @allure.step("Дождаться обновления счетчиков")
    def wait_for_counters_update(self, previous_total_count, timeout=10):
        """Ожидает пока счетчики обновятся"""
        from selenium.common.exceptions import TimeoutException
        
        try:
            self.wait.until(
                lambda driver: self.get_total_orders_count() > previous_total_count
            )
        except TimeoutException:
            # Если счетчик не обновился за timeout, продолжаем
            pass