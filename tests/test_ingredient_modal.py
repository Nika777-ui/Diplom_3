import allure
import pytest
from tests.pages.main_page import MainPage


class TestIngredientModal:
    """
    Тесты для модальных окон ингредиентов
    """
    
    @allure.title("Клик на ингредиент открывает модальное окно с деталями")
    def test_click_ingredient_opens_modal(self, driver):
        """Проверяем что клик на ингредиент открывает детали"""
        main_page = MainPage(driver)
        main_page.open("/")
        
        # Кликаем на ингредиент
        main_page.click_ingredient("traditional_sauce")
        
        # Проверяем что модальное окно открылось
        assert main_page.is_modal_visible(), "Модальное окно не открылось"
        
        # Проверяем заголовок модалки
        modal_title = main_page.get_modal_title()
        assert "Детали ингредиента" in modal_title, f"Заголовок модалки неверный: {modal_title}"
        
        # Проверяем название ингредиента в модалке
        ingredient_name = main_page.get_modal_ingredient_name()
        assert "Соус традиционный галактический" in ingredient_name, f"Название ингредиента неверное: {ingredient_name}"
    
    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_close_modal_by_cross(self, driver):
        """Проверяем закрытие модального окна"""
        main_page = MainPage(driver)
        main_page.open("/")
        
        # Открываем модальное окно
        main_page.click_ingredient("traditional_sauce")
        assert main_page.is_modal_visible(), "Модальное окно не открылось"
        
        # Закрываем модальное окно
        main_page.close_modal()
        
        # Проверяем что модальное окно закрылось
        assert main_page.is_modal_closed(), "Модальное окно не закрылось"