import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
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
        except Exception:
            return 0
    
    @allure.step("Кликнуть на кнопку 'Войти в аккаунт'")
    def click_login_button(self):
        self.click_element(MainPageLocators.LOGIN_BUTTON)
    
    @allure.step("Авторизоваться с email: {email}")
    def login(self, email, password):
        self.input_text(MainPageLocators.EMAIL_INPUT, email)
        self.input_text(MainPageLocators.PASSWORD_INPUT, password)
        self.click_element(MainPageLocators.LOGIN_SUBMIT)
    
    @allure.step("Переключиться на раздел 'Соусы'")
    def switch_to_sauces_section(self):
        self.click_element(MainPageLocators.SAUCE_TAB)
    
    @allure.step("Переключиться на раздел 'Булки'")
    def switch_to_buns_section(self):
        self.click_element(MainPageLocators.BUN_TAB)
    
    @allure.step("Перетащить ингредиент в конструктор")
    def drag_ingredient_to_constructor(self, ingredient_name):
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
        self.click_element(MainPageLocators.ORDER_BUTTON)
    
    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        self.click_element(MainPageLocators.ORDER_MODAL_CLOSE)
    
    @allure.step("Проверить что модальное окно заказа отображается")
    def is_order_modal_visible(self):
        return self.is_element_visible(MainPageLocators.ORDER_MODAL)
    
    @allure.step("Дождаться оформления заказа")
    def wait_for_order_creation(self, timeout=15):
        self.wait.until(EC.visibility_of_element_located(MainPageLocators.ORDER_MODAL))
    
    @allure.step("Проверить что пользователь авторизован")
    def is_authorized(self):
        return self.is_element_visible(MainPageLocators.ORDER_BUTTON)
    
    @allure.step("Получить номер заказа из модального окна")
    def get_order_number_from_modal(self):
        try:
            return self.get_element_text(MainPageLocators.ORDER_MODAL_NUMBER)
        except Exception:
            return "9999"
    
    @allure.step("Дождаться реального номера заказа")
    def wait_for_real_order_number(self, timeout=30):
        """Ожидает когда 9999 сменится на реальный номер"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: (
                    self.get_order_number_from_modal() != "9999" and
                    self.get_order_number_from_modal().isdigit() and
                    len(self.get_order_number_from_modal()) > 3
                )
            )
            return self.get_order_number_from_modal()
        except TimeoutException:
            return self.get_order_number_from_modal()