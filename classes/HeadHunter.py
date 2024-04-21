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
        # self.params = {'text': '', 'page': 0, 'per_page': 100, 'areas': 113, 'only_with_vacancies': True}
        self.params = {'page': 0, 'per_page': 100, 'areas': 113, 'only_with_vacancies': True}
        self.vacancies = []
        self.data = []

    def load_data(self, employers):
        for employer_id in employers:
            response_emp = requests.get(self.url + f'employers/{employer_id}', headers=self.headers)
            data_emp = {'id': response_emp.json().get('id'), 'name': response_emp.json().get('name'),
                        'open_vacancies': response_emp.json().get('open_vacancies')}
            self.vacancies = []
            self.params['page'] = 0
            self.params['employer_id'] = employer_id
            while self.params['page'] != 20:
                response_vac = requests.get(self.url + f'vacancies', headers=self.headers, params=self.params)
                self.params['page'] += 1
                data = response_vac.json()['items']
                self.vacancies.extend(data)
            self.data.append(
                {'employer': data_emp,
                 'vacancies': self.vacancies}
            )

    def load_data_employer(self, keyword):
        self.params_employers['text'] = keyword
        while self.params_employers['page'] != 20:
            response = requests.get(self.url + 'employers', headers=self.headers, params=self.params_employers)
            self.params_employers['page'] += 1
            for employer in response.json()['items']:
                if employer.get('name') == keyword:
                    self.data.append(employer)

    def load_data_vacancies(self, employer_id):
        # self.params['text'] = None
        self.params['employer_id'] = employer_id
        while self.params['page'] != 20:
            response = requests.get(self.url + 'vacancies', headers=self.headers, params=self.params)
            self.params['page'] += 1
            data = response.json()['items']
            self.data.extend(data)

    # def load_data_employer(self):
    #     self.params['text'] = keyword
