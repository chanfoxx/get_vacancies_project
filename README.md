# Парсер вакансий

Добро пожаловать!
Данный проект представляет собой парсер, которой извлекает информацию
о вакансиях с сайтов HeadHunter и SuperJob.

## Введение

Парсер вакансий предназначен для автоматического сбора информации о вакансиях
с сайтов HeadHunter и SuperJob. Он позволяет удобно настраивать параметры
парсинга, фильтровать вакансии по различным критериям и сохранять полученные 
данные в удобном формате.

## Особенности

- Позволяет парсить вакансии с сайтов HeadHunter и SuperJob.
- Фильтрует вакансии по зарплате, требованиям.
- Позволяет настраивать параметры парсинга, такие, как ключевые слова, город, 
зарплату, требования.
- Поддерживает сохранение извлеченных данных в формате JSON.
- Парсер использует взаимодействие с пользователем и вводимые им данные.

## Структура проекта

В файле README.md представлена общая информация о каждом файле и его 
назначении.

- 'jsonsaver.py' - класс для сохранения информации о вакансиях в JSON-файл
и работы с ними.
- 'main.py' - главный файл с запуском программы.
- 'main_utils.py' - функции для главного файла.
- 'pageapi.py' - классы для работы с API сайтов с вакансиями.
- 'vacancy.py' - класс для работы с вакансиями. 
- 'areas.json' - файл со словарями id городов.
- 'vacancies.json' - файл куда загружаются вакансии.

## Установка

1. Клонируйте данный репозиторий на свой локальный компьютер.
2. Установите Python если он еще не установлен.
3. Установите и активируйте виртуальное окружение.
4. Установите Poetry, если еще не установлено.
5. Перейдите в корневую папку проекта и установите все зависимости с помощью
Poetry:
poetry install
6. Запустите парсер:
main.py

## Пример вывода вакансий



## Ошибки и улучшения

Если вы обнаружили ошибки, у вас есть предложения по улучшению данного проекта
или у вас есть вопросы по использованию парсера, пожалуйста, пожалуйста, 
присылайте pull request.

