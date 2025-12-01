import allure
import pytest
from tests.pages.main_page import MainPage


class TestIngredientCounter:
    """
    Тесты для счетчиков ингредиентов
    """
    
    @allure.title("При добавлении ингредиента в заказ счётчик увеличивается")
    def test_ingredient_counter_increases(self, driver):
        """Проверяем что счетчик ингредиента увеличивается при добавлении"""
        main_page = MainPage(driver)
        main_page.open("/")
        
        print("=== ТЕСТ СЧЕТЧИКА (БЕЗ АВТОРИЗАЦИИ) ===")
        
        # Шаг 1: Переходим в соусы (авторизация не нужна!)
        main_page.switch_to_sauces_section()
        print("Перешли в раздел соусов")
        
        # Шаг 2: Получаем начальное значение счетчика
        initial_counter = main_page.get_ingredient_counter_value("traditional_sauce")
        print(f"Начальный счетчик: {initial_counter}")
        
        # Шаг 3: Перетаскиваем ингредиент в конструктор
        print("Пытаемся перетащить...")
        main_page.drag_ingredient_to_constructor("traditional_sauce")
        print("Перетаскивание выполнено")
        
        # Шаг 4: Ждем обновления счетчика
        import time
        print("Ожидаем обновления счетчика...")
        
        for i in range(10):
            time.sleep(1)
            current_counter = main_page.get_ingredient_counter_value("traditional_sauce")
            print(f"Попытка {i+1}: счетчик = {current_counter}")
            
            if current_counter > 0:
                print(f"Счетчик обновился! Значение: {current_counter}")
                break
        else:
            print("Счетчик не обновился за 10 секунд")
        
        final_counter = main_page.get_ingredient_counter_value("traditional_sauce")
        print(f"Финальный счетчик: {final_counter}")
        
        # Шаг 5: Проверяем что счетчик увеличился
        assert final_counter > initial_counter, f"Счетчик не увеличился: было {initial_counter}, стало {final_counter}"
        print("ТЕСТ ПРОШЕЛ УСПЕШНО!")