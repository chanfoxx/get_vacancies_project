from abc import ABC, abstractmethod
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class ErrorResponse(Exception):
    """Класс исключения для ошибки запроса."""

    def __init__(self, *args) -> None:
        """
        Конструктор класса ErrorResponse.

        :param args: Произвольное количество позиционных аргументов,
        используемых для установки сообщения об ошибке.
        """
        self.message = args[0] if args else "Ошибка выполнения запроса"

    def __str__(self) -> str:
        """Возвращает строковое сообщение об ошибке."""
        return self.message


class PageAPI(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями."""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self, search_query, search_area):
        pass


class HeadHunterAPI(PageAPI):
    """
    Класс, наследующийся от абстрактного класса,
    для работы с платформой HeadHunter.
    """

    def __init__(self) -> None:
        """
        Создание экземпляра класса HeadHunterAPI.
        Устанавливает базовый URL для работы с API HeadHunter.
        """
        self.url = 'https://api.hh.ru'

    def get_vacancies(self, search_query: str, search_area: int) -> list[dict]:
        """
        Производит поиск вакансий по пользовательскому запросу,
        и получает список словарей с данными о вакансиях.

        Параметры запроса:
        'text' - поисковой запрос,
        'area' - регион поиска,
        'per_page' - количество элементов (вакансий),
        'only_with_salary' - вывод вакансий с указанием зарплаты (True).
        """
        url = f"{self.url}/vacancies"
        params = {
            "text": search_query,
            "area": search_area,
            "per_page": 100,
            "only_with_salary": True,
            "search_fields": "name"
        }

        # Отправляем запрос с установленными параметрами.
        response = requests.get(url, params=params)

        # Если запрос выполнен успешно, возвращается список словарей,
        # в противном случае выбрасывает ошибку.
        if response.status_code == 200:
            data_vacancy = response.json()['items']
            return self.data_organize(data_vacancy)
        else:
            raise ErrorResponse("Ошибка при выполнении запроса: ",
                                response.status_code)

    @staticmethod
    def data_organize(data_vacancy) -> list[dict]:
        """
        Организация данных по вакансиям.
        Возвращает сформированный список словарей.
        """
        vacancies = []
        for vacancy in data_vacancy:
            title = vacancy['name']
            link = vacancy['alternate_url']
            requirement = vacancy['snippet'].get('requirement', None)
            salary_from = vacancy['salary'].get('from', None)
            salary_to = vacancy['salary'].get('to', None)

            # Устанавливаем значение зарплаты.
            # Если есть обе границы - устанавливаем минимальное значение.
            # В ином случае, устанавливаем то значение, которое существует.
            if salary_from and salary_to:
                salary = min(salary_from, salary_to)
            else:
                salary = salary_from or salary_to

            # Устанавливаем значение требований.
            # Если значение есть - приводим его к нижнему регистру.
            # В ином случае, устанавливаем значение, что данных нет.
            if requirement:
                requirement = requirement.lower()
            else:
                requirement = 'Нет данных.'

            # Добавляем сформированные данные в список.
            vacancies.append({
                'title': title,
                'link': link,
                'salary': salary,
                'requirement': requirement
            })

        return vacancies


class SuperJobAPI(PageAPI):
    """
    Класс, наследующийся от абстрактного класса,
    для работы с платформой SuperJob.
    """

    def __init__(self):
        """
        Создание экземпляра класса SuperJobAPI.
        Устанавливает базовый URL для работы с API SuperJob.
        """
        self.url = "https://api.superjob.ru"

    def get_vacancies(self, search_query: str, search_area: int) -> list[dict]:
        """
        Производит поиск вакансий по пользовательскому запросу,
        и получает список словарей с данными о вакансиях

        Параметры запроса:
        'keyword' - поисковой запрос,
        'page' - номер страницы поиска,
        'count' - количество элементов (вакансий),
        'town' - регион поиска (город).
        """
        url = f"{self.url}/2.0/vacancies/"
        params = {
            "keyword": search_query,
            "page": 0,
            "count": 10,
            "town": search_area
        }
        headers = {'X-Api-App-Id': os.getenv("SJ_SECURE_CODE")}

        # Отправляем запрос с установленными параметрами.
        response = requests.get(url, headers=headers, params=params)

        # Если запрос выполнен успешно, возвращается список словарей,
        # в противном случае выбрасывает ошибку.
        if response.status_code == 200:
            data_vacancy = response.json()['objects']
            return self.data_organize(data_vacancy)
        else:
            raise ErrorResponse(f"Ошибка при выполнении запроса: {response.status_code}")

    @staticmethod
    def data_organize(data_vacancy) -> list[dict]:
        """
        Организация данных по вакансиям.
        Возвращает сформированный список словарей.
        """
        vacancies = []
        for vacancy in data_vacancy:
            title = vacancy['profession']
            link = vacancy['link']
            salary_from = vacancy.get('payment_from', None)
            salary_to = vacancy.get('payment_to', None)
            requirement = vacancy.get('candidat', None)

            # Устанавливаем значение зарплаты.
            # Если есть обе границы - устанавливаем минимальное значение.
            # В ином случае, устанавливаем то значение, которое существует.
            if salary_from and salary_to:
                salary = min(salary_from, salary_to)
            else:
                salary = salary_from or salary_to

            # Устанавливаем значение требований.
            # Если значение есть - приводим его к нижнему регистру.
            # В ином случае, устанавливаем значение, что данных нет.
            if requirement:
                requirement = requirement.lower()
            else:
                requirement = 'Нет данных.'

            # Проводим проверку, чтобы добавлялись лишь те вакансии, у которых
            # значение зарплаты больше 1000.
            # Добавляем сформированные данные в список.
            if salary > 1000:
                vacancies.append({
                    'title': title,
                    'link': link,
                    'salary': salary,
                    'requirement': requirement
                })

        return vacancies
