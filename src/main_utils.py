import json
from settings import PATH_AREA_FILE
from pageapi import HeadHunterAPI, SuperJobAPI
from vacancy import Vacancy
from jsonsaver import JSONSaver


def get_selected_platforms(platforms: list) -> list:
    """
    Возвращает список с экземпляром платформы
    по API классов HeadHunterAPI или SuperJobAPI.
    """
    api_list = []
    valid_input = False

    # Создаем цикл while с флагом valid_input, он работает до тех пор,
    # пока пользователь не введет нужную платформу.
    while not valid_input:
        selected_platforms = input('Укажите платформу для получения вакансий '
                                   '(например, HeadHunter или SuperJob): '
                                   ).split()

        # Создаем цикл for, чтобы сравнивать введенный пользователем текст
        # со значениями в списке платформ. В зависимости от ввода
        # проводится выбор платформы и создается нужный экземпляр класса с API.
        for platform in selected_platforms:
            if platform.strip() in platforms:
                if platform.strip() == 'HeadHunter' or \
                        platform.strip() == 'headhunter' or \
                        platform.strip() == 'hh':
                    api_list.append(HeadHunterAPI())
                    valid_input = True
                elif platform.strip() == 'SuperJob' or \
                        platform.strip() == 'superjob' or \
                        platform.strip() == 'sj':
                    api_list.append(SuperJobAPI())
                    valid_input = True
            else:
                print("Платформа не поддерживается или Вы не ввели ее.")
                break

    return api_list


def load_area_dicts() -> tuple[dict, dict]:
    """Загружает json файл со словарями городов для API."""
    try:
        with open(PATH_AREA_FILE, encoding='utf-8') as file:
            areas = json.load(file)
    except FileNotFoundError:
        pass

    return areas['area_hh'], areas['area_sj']


def get_search_query_and_area(area_hh: dict,
                              area_sj: dict) -> tuple[str, int, int]:
    """
    Возвращает значение введенные пользователем для осуществления
    поиска по API по критериям:
    поиска - search_query,
    города - search_city (поиск ведется по словарю hh, т.к.
    словари обеих платформ одинаковы, различаются лишь значения(int)).
    """
    # Просим пользователя ввести поисковый запрос.
    search_query = input("Введите поисковый запрос (Например, Python): ")

    # Создаем цикл while с флагом valid_search, он работает до тех пор,
    # пока пользователь не введет запрос.
    valid_search = False
    while not valid_search:
        if search_query:
            valid_search = True
        else:
            print("Вы не ввели поисковый запрос.")
            search_query = input("Введите поисковый запрос (Например, Python): ")

    # Просим пользователя ввести город поиска.
    search_city = input("Введите название города (Например, Москва): "
                        "").title()

    # Создаем цикл while, до тех пор пока пользователь
    # не введет существующий город в словаре.
    while search_city not in area_hh:
        print('Такого города нет в базе или неверный ввод.')
        search_city = input("Введите название города (Например, Москва): "
                            "").title()

    search_area_hh = area_hh[search_city]  # сохраняем значение введенного города hh.
    search_area_sj = area_sj[search_city]  # сохраняем значение введенного города sj.

    return search_query, search_area_hh, search_area_sj


def get_vacancies(json_saver: JSONSaver, api_list: list, search_query: str,
                  search_area_hh: int, search_area_sj: int) -> None:
    """
    Создает экземпляры класса Vacancy по запрашиваемому поиску (слово, город)
    и добавляет их в файл с вакансиями. Далее обращается к функциям
    фильтрации по критериям salary и requirement.
    """
    # Создаем цикл for и выбираем работу с вакансиями
    # на основе выбранной пользователем платформы.
    for api in api_list:
        # Получаем вакансии по запросам (слово, город).
        hh_data = api.get_vacancies(search_query, search_area_hh)
        sj_data = api.get_vacancies(search_query, search_area_sj)

        # Создаем экземпляры класса Vacancy.
        hh_vacancies = [Vacancy(v['title'], v['link'], v['salary'],
                                v['requirement']) for v in hh_data]

        sj_vacancies = [Vacancy(v['title'], v['link'], v['salary'],
                                v['requirement']) for v in sj_data]

        # Добавляем вакансии в файл.
        json_saver.add_vacancy(hh_vacancies)
        json_saver.add_vacancy(sj_vacancies)

        # Фильтруем вакансии по критериям salary и requirement.
        filter_by_salary(json_saver)
        filter_by_requirement(json_saver)


def filter_by_salary(json_saver: JSONSaver) -> None:
    """Фильтруем вакансии по зарплате (критерий salary)."""
    # Создаем цикл while с флагом valid_salary, он работает до тех пор,
    # пока пользователь не введет запрос.
    valid_salary = False
    while not valid_salary:
        try:
            # Просим пользователя ввести минимальное значение зарплаты.
            min_salary = int(input("Введите минимальную зарплату для "
                                   "фильтрации (Например, 110000): "))
        except ValueError:
            print('Вы не ввели значение зарплаты.')
        else:
            # Фильтруем по минимальному значению.
            json_saver.get_salary(min_salary)
            valid_salary = True
            # Если файл с вакансиями пуст после фильтрации выводим сообщение.
            if len(json_saver.data) == 0:
                print("Нет вакансий, соответствующих заданным критериям.")


def filter_by_requirement(json_saver: JSONSaver) -> None:
    """Фильтруем вакансии по зарплате (критерий requirement)."""
    # Просим пользователя ввести ключевое слово для фильтрации.
    keyword_list = input("Введите ключевые слова для фильтрации вакансий "
                         "по требованиям (через пробел): ").lower().split()

    # Делаем проверку ввода данных пользователя,
    # в ином случае выводим сообщение.
    if keyword_list:
        # Фильтруем по ключевым словам
        json_saver.get_requirement(keyword_list)
        # Если файл с вакансиями пуст после фильтрации выводим сообщение.
        if len(json_saver.data) == 0:
            print("Нет вакансий, соответствующих заданным критериям.")
    else:
        print("Вы отказались от фильтрации по требованиям.")


def sort_vacancies(filtered_vacancies: list, order: str, top_n) -> list:
    """
    Сортирует вакансии в зависимости от выбора.
    Имеет возможность выводить конкретное количество вакансий
    (если такое количество имеется).
    """
    # По возрастанию.
    if order.lower() == '1':
        sorted_vacancies = sorted(filtered_vacancies,
                                  key=lambda x: x['salary'])
    # По убыванию.
    elif order.lower() == '2':
        sorted_vacancies = sorted(filtered_vacancies,
                                  key=lambda x: x['salary'], reverse=True)
    else:
        print("Некорректный выбор порядка сортировки.")
        return []

    # Проверяем наличие ввода значения - если оно есть выводим срез вакансий.
    if top_n:
        sorted_vacancies = sorted_vacancies[:int(top_n)]

    return sorted_vacancies


def print_vacancies(vacancies: list) -> None:
    """Печатает количество найденных вакансий, название, ссылку и зарплату."""
    print(f"Нашлось {len(vacancies)}:")
    # Создаем цикл по вакансиям и выводим их пронумерованными.
    for index, vacancy in enumerate(vacancies, start=1):
        print(f"{index}. {vacancy['title']} -> ссылка на вакансию:",
              vacancy['link'], f"<- зарплата: {vacancy['salary']} руб.")


def delete_vacancies(json_saver: JSONSaver, vacancies: list) -> None:
    """Удаляет вакансии с помощью функции из класса JSONSaver."""
    for vacancy in vacancies:
        json_saver.delete_vacancy(vacancy['link'])
