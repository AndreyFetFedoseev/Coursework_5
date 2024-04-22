from abc import ABC, abstractmethod
import psycopg2


class AbstractManager(ABC):
    """
    Абстрактный класс для управления БД
    """

    @staticmethod
    @abstractmethod
    def get_companies_and_vacancies_count(params):
        """
         Метод получает список всех компаний и количество вакансий у каждой компании
        :return: БД
        """
        pass

    @staticmethod
    @abstractmethod
    def get_all_vacancies(params):
        """
        Метод получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты
        и ссылки на вакансию
        :return: БД
        """
        pass

    @staticmethod
    @abstractmethod
    def get_avg_salary(params):
        """
        Метод получает среднюю зарплату по вакансиям
        :return: БД
        """
        pass

    @staticmethod
    @abstractmethod
    def get_vacancies_with_higher_salary(params):
        """
        Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return: БД
        """
        pass

    @staticmethod
    @abstractmethod
    def get_vacancies_with_keyword(params, keyword):
        """
        Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        :return: БД
        """
        pass


class DBManager(AbstractManager):
    """
    Класс для запросов к БД
    """

    @staticmethod
    def get_companies_and_vacancies_count(params):

        conn = psycopg2.connect(**params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT company_name, open_vacancies FROM employers
            """)
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    @staticmethod
    def get_all_vacancies(params):

        conn = psycopg2.connect(**params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT employers.company_name, name, salary_to, url 
                FROM vacancies
                INNER JOIN employers ON employers.employer_id=vacancies.employer_id
            """)
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    @staticmethod
    def get_avg_salary(params):
        conn = psycopg2.connect(**params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(salary_to) FROM vacancies
                WHERE salary_to IS NOT NULL
            """)
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    @staticmethod
    def get_vacancies_with_higher_salary(params):
        """
        Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return: БД
        :param params:
        :return:
        """
        conn = psycopg2.connect(**params)
        with conn.cursor() as cur:
            cur.execute("""
                   SELECT * FROM vacancies
                   WHERE salary_to > (SELECT AVG(salary_to) FROM vacancies
                                      WHERE salary_to IS NOT NULL AND salary_to > 0)
                   ORDER BY salary_to DESC 
            """)
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    @staticmethod
    def get_vacancies_with_keyword(params, keyword):
        """
        Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        :param keyword:
        :param params:
        :return:
        """
        conn = psycopg2.connect(**params)
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM vacancies
                WHERE name LIKE '%{keyword}%'
            """)
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

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
                    salary_currency VARCHAR(100),
                    published_at DATE,
                    schedule VARCHAR(255),
                    experience VARCHAR,
                    requirement TEXT,
                    url TEXT
                )
            """)
        conn.commit()
        conn.close()

    @staticmethod
    def add_data_table_database(params, database):
        conn = psycopg2.connect(**params)
        with conn.cursor() as cur:
            for data in database:
                employer = data['employer']
                cur.execute("""
                    INSERT INTO employers (company_name, open_vacancies, employer_url)
                    VALUES (%s, %s, %s)
                    RETURNING employer_id
                """, (
                    employer.get('name'), employer.get('open_vacancies'),
                    employer.get('alternate_url'))
                            )
                employer_id = cur.fetchone()
                vacancies = data['vacancies']
                for vacancy in vacancies:
                    if vacancy['salary'] is None:
                        vacancy['salary'] = {'from': 0, 'to': 0, 'currency': 'RUR'}
                    cur.execute("""
                        INSERT INTO vacancies (employer_id, name, area, salary_from, salary_to, salary_currency, 
                        published_at, schedule, experience, requirement, url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (employer_id, vacancy.get('name'), vacancy.get('area').get('name'),
                          vacancy['salary'].get('from'), vacancy['salary'].get('to'),
                          vacancy['salary'].get('currency'), vacancy.get('published_at'),
                          vacancy.get('schedule').get('name'), vacancy.get('experience').get('name'),
                          vacancy.get('snippet').get('requirement'), vacancy.get('alternate_url'))
                                )
        conn.commit()
        conn.close()
