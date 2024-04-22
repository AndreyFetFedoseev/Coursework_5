from config import config
from classes.DBManager import DBManager
from classes.HeadHunter import HH

params = config()
employers_id = [
    1740,  # Яндекс
    9498112,  # Яндекс Крауд
    5008932,  # Яндекс Практикум
    78638,  # Тинькофф
    19989,  # ЕВРАЗ
    692517,  # Смартком
    1092837,  # S7 IT
    1122462,  # Skyeng
    2774067,  # Сибэлектро
    10641663  # Buyer
]
db_name = 'headhunter'


def main():
    headhunter = HH()
    headhunter.load_data(employers_id)
    data = headhunter.data

    database_hh = DBManager(params)
    database_hh.create_database(db_name)
    database_hh.params.update({'dbname': db_name})
    database_hh.add_data_table_database(data)

    print(database_hh.get_companies_and_vacancies_count())
    print(database_hh.get_all_vacancies())
    print(database_hh.get_avg_salary())
    print(database_hh.get_vacancies_with_higher_salary())
    print(database_hh.get_vacancies_with_keyword('Python'))


if __name__ == '__main__':
    main()
