from abc import ABC, abstractmethod
import json


class SaveWorker(ABC):
    """
    Абстрактный класс, который обязывает реализовать методы
    для добавления вакансий в файл, получения данных из файла по указанным
    критериям и удаления информации о вакансиях.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_salary(self, salary):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONSaver(SaveWorker):
    """
    Класс для сохранения информации о вакансиях в JSON-файл.
    """

    def __init__(self, filename) -> None:
        """
        Создание экземпляра класса JSONSaver.

        :param filename: Файл с данными по вакансиям.
        """
        self.filename = filename
        self.data = []

    def load_data(self) -> None:
        """Загружает файл."""
        try:
            with open(self.filename, encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = []
        except json.JSONDecodeError:
            return None

    def save_data(self) -> None:
        """Сохраняет данные в файл."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=2, ensure_ascii=False)

    def add_vacancy(self, vacancies: list) -> None:
        """Добавляет вакансии в файл."""
        self.data.extend([vacancy.to_dict() for vacancy in vacancies])
        self.save_data()

    def get_requirement(self, criteria_list: list[str]) -> None:
        """
        Получает список со словами, фильтрует по ним критерий требований,
        сохраняет полученные вакансии в файл.
        """
        requirement_data = [item for item in self.data
                            if item['requirement'] is not None
                            if all(criteria in item['requirement']
                                   for criteria in criteria_list)]
        self.data = requirement_data
        self.save_data()

    def get_salary(self, salary: int) -> None:
        """
        Получает список со словами, фильтрует по ним критерий зарплаты,
        сохраняет полученные вакансии в файл.
        """
        salary_data = [item for item in self.data if item['salary'] >= salary]
        self.data = salary_data
        self.save_data()

    def delete_vacancy(self, vacancy_link: str) -> None:
        """Удаляет вакансии из файла."""
        self.data = [item for item in self.data if item['link'] != vacancy_link]
        self.save_data()
