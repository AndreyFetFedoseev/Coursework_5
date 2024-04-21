from abc import ABC, abstractmethod
import psycopg2


# class AbstractManager(ABC):
#     """
#     Абстрактный класс для управления БД
#     """
#
#     @abstractmethod
#     def get_companies_and_vacancies_count(self):
#         """
#          Метод получает список всех компаний и количество вакансий у каждой компании
#         :return: БД
#         """
#         pass
#
#     @abstractmethod
#     def get_all_vacancies(self):
#         """
#         Метод получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
#         :return: БД
#         """
#         pass
#
#     @abstractmethod
#     def get_avg_salary(self):
#         """
#         Метод получает среднюю зарплату по вакансиям
#         :return: БД
#         """
#         pass
#
#     @abstractmethod
#     def get_vacancies_with_higher_salary(self):
#         """
#         Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
#         :return: БД
#         """
#         pass
#
#     @abstractmethod
#     def get_vacancies_with_keyword(self):
#         """
#         Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
#         :return: БД
#         """
#         pass


class DBManager:
    """
    Класс для запросов к БД
    """

    # def create_database(self):
    #     pass

    def create_table(self):
        pass

    def filling_out_table(self):
        pass

    @staticmethod
    def create_database(database_name: str, params: dict) -> None:
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
        cur.execute(f'CREATE DATABASE {database_name}')

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=f'{database_name}', **params)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    employer_id SERIAL PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL,
                    open_vacancies INT,
                    description TEXT,
                    employer_url TEXT
                )
            """)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    name VARCHAR NOT NULL,
                    area VARCHAR(255),
                    salary_from INT,
                    salary_to INT,
                    salary_currency VARCHAR(10),
                    published_at DATE,
                    schedule VARCHAR(255),
                    experience VARCHAR,
                    requirement TEXT,
                    url TEXT
                )
            """)
        conn.commit()
        conn.close()
