# parser-for-VERBA-group
тестовое задание

a. Что было сделано

В данном проекте был реализован скрипт на языке Python, который осуществляет сбор и сохранение цитат с веб-сайта. Скрипт выполняет следующие основные задачи:

• Получает HTML-код страниц с цитатами.

• Извлекает текст цитат, имена авторов и теги.

• Проверяет, встречались ли авторы ранее, и если нет, собирает дополнительную информацию о каждом авторе (дату рождения и описание), или дополняет информацию к автору(цитату)

• Сохраняет собранные данные в формате JSON.

b. Данные были получены с веб-сайта, содержащего коллекцию цитат. В коде используется базовая ссылка, которая хранится в конфигурационном файле config.ini.

c. 
    1. Запрос страницы: Используя библиотеку requests, скрипт отправляет HTTP-запрос на указанный URL и получает HTML-код страницы.
    2. Парсинг HTML: С помощью библиотеки BeautifulSoup HTML-код разбирается, и из него извлекаются необходимые элементы (цитаты, авторы, теги).
    3. Сбор информации об авторах: Для каждого нового автора производится дополнительный запрос для получения информации о дате рождения и описании.
    4. Обработка нескольких страниц: Скрипт обрабатывает все страницы с цитатами, пока есть кнопка "Следующая страница".
    5. Сохранение данных: Собранные данные сохраняются в файл data.json в формате JSON.

d.
    Первоначально я анализировал два возможных подхода:
        1. С помощью Selenium
        2. BeautifulSoup

    Выбор пал на второй вариант, так как:
        - легко поддается парсингу
        - менее ресурсозатратный
        - выигрываает по скорости