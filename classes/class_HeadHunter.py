import json
import requests
from abc import ABC, abstractmethod


class AbstractHH(ABC):
    """
    Абстрактный класс для получения данных с HeadHunter API
    """
    # @abstractmethod
    # def load_data_employer(self):
    #     """
    #     Метод получения данных о работодателях
    #     :return:
    #     """
    #     pass
    #
    # @abstractmethod
    # def load_data_vacancies(self):
    #     """
    #     Метод получения данных о вакансиях
    #     :return:
    #     """
    #     pass

class HH(AbstractHH):
    """
    Класс для получения данных с сайта HeadHunter.ru
    """

    def __init__(self):
        self.url = 'https://api.hh.ru/'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100, 'areas': 113, 'only_with_vacancies': True}
        self.data = []


    def load_data(self, search, keyword):
        self.params['text'] = keyword
        while self.params['page'] != 20:
            response = requests.get(self.url + f'{search}', headers=self.headers, params=self.params)
            self.params['page'] += 1
            data = response.json()['items']
            self.data.extend(data)




    # def load_data_employer(self):
    #     self.params['text'] = keyword