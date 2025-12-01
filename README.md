# Diplom_3
# Дипломный проект: Автоматизация тестирования сайта Stellar Burgers

## Описание проекта
Автоматизированные тесты для сайта [Stellar Burgers](https://stellarburgers.education-services.ru/) с использованием Python, Selenium WebDriver, Pytest и Allure.

## Структура проекта
Diplom_3/
├── tests/
│ ├── pages/ # Page Object классы
│ │ ├── base_page.py # Базовый класс с общими методами
│ │ ├── main_page.py # Главная страница (конструктор бургеров)
│ │ └── order_feed_page.py # Страница ленты заказов
│ ├── locators/ # Локаторы элементов
│ │ ├── main_page_locators.py
│ │ └── order_feed_locators.py
│ ├── conftest.py # Фикстуры Pytest
│ ├── test_constructor_navigation.py # Тесты навигации конструктора
│ ├── test_ingredient_counter.py # Тесты счетчиков ингредиентов
│ ├── test_ingredient_modal.py # Тесты модальных окон ингредиентов
│ ├── test_order_feed.py # Тесты ленты заказов (дипломные)
│ └── test_debug_api.py # Диагностические API-тесты
├── config.py # Конфигурация тестового окружения
├── requirements.txt # Зависимости проекта
├── .gitignore # Игнорируемые файлы Git
└── README.md # Документация проекта

## Установка зависимостей
pip install -r requirements.txt

## Конфигурация
Файл config.py содержит настройки:
BASE_URL - базовый URL тестируемого приложения
TEST_EMAIL и TEST_PASSWORD - учетные данные тестового пользователя
BROWSER - браузер по умолчанию (chrome/firefox)
Таймауты и другие параметры

## Запуск тестов
pytest tests/ -v -s
# Запуск тестов ленты заказов
pytest tests/test_order_feed.py -v -s
# Тесты навигации по конструктору
pytest tests/test_constructor_navigation.py -v -s --browser=chrome
# Тесты счетчиков ингредиентов
pytest tests/test_ingredient_counter.py -v -s --browser=chrome
# Тесты модальных окон ингредиентов
pytest tests/test_ingredient_modal.py -v -s --browser=chrome
# Все тесты кроме ленты заказов
pytest tests/ -k "not order_feed" -v -s --browser=chrome
# Запуск с указанием браузера
pytest tests/test_order_feed.py -v -s --browser=chrome
pytest tests/test_order_feed.py -v -s --browser=firefox
# Запуск с генерацией Allure-отчета
pytest tests/test_order_feed.py -v --alluredir=allure-results
allure serve allure-results

## Тестируемая функциональность
- переход по клику на «Конструктор»;
- переход по клику на раздел «Лента заказов»;
- если кликнуть на ингредиент, появится всплывающее окно с деталями;
- всплывающее окно закрывается кликом по крестику;
- при добавлении ингредиента в заказ счётчик этого ингредиента увеличивается.
Раздел «Лента заказов»
- при создании нового заказа счётчик «Выполнено за всё время» увеличивается;
- при создании нового заказа счётчик «Выполнено за сегодня» увеличивается;
- после оформления заказа его номер появляется в разделе «В работе».

## Обнаруженные проблемы
В процессе тестирования выявлены следующие проблемы в приложении:
Счетчики заказов не обновляются в реальном времени при создании заказа через UI
Модальное окно заказа показывает заглушку "9999", которя не меняется на реальный заказ (самое долгое время ожидания - 12 минут, но ID заказа не появилось)
Заказ не появляет в разделе в работе из-за проблем, которые описаны в пердыдущем пункте "В работе:" показывают одинаковые данные
Кросс-браузерные проблемы - не все функции работают одинаково в Chrome и Firefox
