from abc import ABC, abstractmethod
import psycopg2


class AbstractManager(ABC):
    """
    Абстрактный класс для управления БД
    """

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        """
         Метод получает список всех компаний и количество вакансий у каждой компании
        :return: БД
        """
        pass

    @abstractmethod
    def get_all_vacancies(self):
        """
        Метод получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        :return: БД
        """
        pass

    @abstractmethod
    def get_avg_salary(self):
        """
        Метод получает среднюю зарплату по вакансиям
        :return: БД
        """
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        """
        Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return: БД
        """
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):
        """
        Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        :return: БД
        """
        pass


class DBManager(AbstractManager):
    """
    Класс для запросов к БД
    """

    def create_database(self):
        pass

    def create_table(self):
        pass

    def filling_out_table(self):
        pass
