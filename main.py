import json

from config import config
from classes.DBManager import DBManager
from classes.HeadHunter import HH

params = config()
employers_id = [
    # 1740,  # Яндекс
    # 9498112,  # Яндекс Крауд
    5008932  # Яндекс Практикум
]


def main():
    headhunter = HH()
    headhunter.load_data(employers_id)

    database_hh = DBManager()
    database_hh.create_database('headhunter', params)


if __name__ == '__main__':
    main()
