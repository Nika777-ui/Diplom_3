import allure
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from tests.locators.main_page_locators import MainPageLocators


class MainPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Кликнуть на вкладку 'Конструктор'")
    def click_constructor_tab(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_TAB)
    
    @allure.step("Кликнуть на вкладку 'Лента заказов'")
    def click_order_feed_tab(self):
        self.click_element(MainPageLocators.ORDER_FEED_TAB)
    
    @allure.step("Кликнуть на ингредиент: {ingredient_name}")
    def click_ingredient(self, ingredient_name):
        if ingredient_name == "traditional_sauce":
            self.click_element(MainPageLocators.TRADITIONAL_GALACTIC_SAUCE)
    
    @allure.step("Закрыть модальное окно ингредиента")
    def close_modal(self):
        self.click_element(MainPageLocators.MODAL_CLOSE)
    
    @allure.step("Проверить видимость модального окна ингредиента")
    def is_modal_visible(self):
        return self.is_element_visible(MainPageLocators.MODAL)
    
    @allure.step("Проверить что модальное окно ингредиента закрыто")
    def is_modal_closed(self):
        return self.is_element_not_visible(MainPageLocators.MODAL)
    
    @allure.step("Получить текст заголовка модального окна ингредиента")
    def get_modal_title(self):
        return self.get_element_text(MainPageLocators.MODAL_TITLE)
    
    @allure.step("Получить название ингредиента в модальном окне")
    def get_modal_ingredient_name(self):
        return self.get_element_text(MainPageLocators.MODAL_INGREDIENT_NAME)
    
    @allure.step("Получить значение счетчика ингредиента")
    def get_ingredient_counter_value(self, ingredient_name="traditional_sauce"):
        try:
            if ingredient_name == "traditional_sauce":
                counter_text = self.get_element_text(MainPageLocators.TRADITIONAL_SAUCE_COUNTER)
                return int(counter_text) if counter_text else 0
            return 0
        except:
            return 0
    
    @allure.step("Кликнуть на кнопку 'Войти в аккаунт'")
    def click_login_button(self):
        self.click_element(MainPageLocators.LOGIN_BUTTON)
    
    @allure.step("Авторизоваться с email: {email} и паролем")
    def login(self, email, password):
        self.input_text(MainPageLocators.EMAIL_INPUT, email)
        self.input_text(MainPageLocators.PASSWORD_INPUT, password)
        self.click_element(MainPageLocators.LOGIN_SUBMIT)
    
    @allure.step("Переключиться на раздел 'Соусы'")
    def switch_to_sauces_section(self):
        self.click_element(MainPageLocators.SAUCE_TAB)
    
    @allure.step("Перетащить ингредиент в конструктор")
    def drag_ingredient_to_constructor(self, ingredient_name):
        """Перетаскивает ингредиент в конструктор (React-версия)"""
        if ingredient_name == "traditional_sauce":
            source_element = self.find_element(MainPageLocators.TRADITIONAL_GALACTIC_SAUCE)
            target_element = self.find_element(MainPageLocators.BASKET)
            self.drag_and_drop_react(source_element, target_element)
    
    @allure.step("Получить количество добавленных ингредиентов")
    def get_added_ingredients_count(self):
        elements = self.find_elements(MainPageLocators.CONSTRUCTOR_ELEMENT)
        return len(elements)
    
    @allure.step("Оформить заказ")
    def create_order(self):
        """Нажимает кнопку 'Оформить заказ'"""
        self.click_element(MainPageLocators.ORDER_BUTTON)
    
    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        """Закрывает модальное окно с номером заказа"""
        self.click_element(MainPageLocators.ORDER_MODAL_CLOSE)
    
    @allure.step("Проверить что модальное окно заказа отображается")
    def is_order_modal_visible(self):
        """Проверяет видимость модального окна заказа"""
        return self.is_element_visible(MainPageLocators.ORDER_MODAL)
    
    @allure.step("Дождаться оформления заказа")
    def wait_for_order_creation(self, timeout=10):
        """Ожидает появления модального окна заказа"""
        self.wait.until(EC.visibility_of_element_located(MainPageLocators.ORDER_MODAL))
    
    @allure.step("Проверить что пользователь авторизован")
    def is_authorized(self):
        """Проверяет что пользователь авторизован (кнопка 'Оформить заказ' доступна)"""
        return self.is_element_visible(MainPageLocators.ORDER_BUTTON)
    
    @allure.step("Получить номер заказа из модального окна")
    def get_order_number_from_modal(self):
        """Возвращает номер заказа из модального окна"""
        return self.get_element_text(MainPageLocators.ORDER_MODAL_NUMBER)

    @allure.step("Проверить номер заказа в модальном окне")
    def check_order_number_in_modal(self, wait_time=60):
        """Проверяет номер заказа в модальном окне, ждет смены 9999"""
        import time
    
        print(f"Проверяем номер заказа в модальном окне (ждать до {wait_time} секунд)...")
    
        try:
            # Получаем начальный номер
            initial_number = self.get_order_number_from_modal()
        except:
            initial_number = "9999"  # Если элемент не найден
    
        print(f"Начальный номер в модальном окне: '{initial_number}'")
    
        # Если уже не 9999 - возвращаем
        if initial_number != "9999":
            print(f"Номер заказа уже реальный: {initial_number}")
            return initial_number
    
        # Ждем смены номера
        for i in range(wait_time):
            try:
                current_number = self.get_order_number_from_modal()
            except:
                current_number = "9999"  # Если элемент не найден
        
            if current_number != "9999":
                print(f"Номер заказа изменился на реальный: {current_number} (через {i+1} секунд)")
                return current_number
        
            if (i + 1) % 10 == 0:  # Логируем каждые 10 секунд
                print(f"Все еще ждем... текущий номер: '{current_number}' ({i+1} секунд)")
        
            time.sleep(1)
    
        # Если не дождались
        print(f"Не дождались реального номера заказа за {wait_time} секунд. Осталось: '{initial_number}'")
        return initial_number  # Вернет "9999"