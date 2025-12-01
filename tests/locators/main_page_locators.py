from selenium.webdriver.common.by import By

class MainPageLocators:
    """Локаторы для главной страницы (конструктор бургеров)"""
    
    # Навигация
    CONSTRUCTOR_TAB = (By.XPATH, "//p[text()='Конструктор']/parent::a")
    ORDER_FEED_TAB = (By.XPATH, "//p[text()='Лента Заказов']/parent::a")
    
    # Табы конструктора
    BUN_TAB = (By.XPATH, "//span[text()='Булки']/parent::div")
    SAUCE_TAB = (By.XPATH, "//span[text()='Соусы']/parent::div")
    FILLING_TAB = (By.XPATH, "//span[text()='Начинки']/parent::div")
    
    # Ингредиенты
    TRADITIONAL_GALACTIC_SAUCE = (By.XPATH, "//p[text()='Соус традиционный галактический']")
    
    # Счетчики ингредиентов
    TRADITIONAL_SAUCE_COUNTER = (By.XPATH, "//p[text()='Соус традиционный галактический']/../div[1]/p")
    
    # Модальное окно ингредиента
    MODAL = (By.XPATH, "//*[@id='root']/div/section[1]/div[1]")
    MODAL_CLOSE = (By.XPATH, "//*[@id='root']/div/section[1]/div[1]//button")
    MODAL_TITLE = (By.XPATH, "//*[@id='root']/div/section[1]/div[1]//h2")
    MODAL_INGREDIENT_NAME = (By.XPATH, "//*[@id='root']/div/section[1]/div[1]/div/p")
    
   # Конструктор заказа
    BASKET = (By.XPATH, "//*[contains(text(), 'Перетяните булочку сюда')]/ancestor::ul")
    CONSTRUCTOR_ELEMENT = (By.CSS_SELECTOR, ".constructor-element")
    ORDER_BUTTON = (By.XPATH, "//*[@id='root']/div/main/section[2]/div/button")
    
    # Авторизация
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    EMAIL_INPUT = (By.NAME, "name")
    PASSWORD_INPUT = (By.NAME, "Пароль")
    LOGIN_SUBMIT = (By.XPATH, "//button[text()='Войти']")

    # Модальное окно Идентификатор заказа
    ORDER_MODAL_CLOSE = (By.XPATH, "//*[@id='root']/div/section/div[1]/button")
    ORDER_MODAL = (By.XPATH, "//*[@id='root']/div/section/div[1]")
    ORDER_MODAL_NUMBER = (By.XPATH, "//*[@id='root']/div/section/div[1]/div/h2")