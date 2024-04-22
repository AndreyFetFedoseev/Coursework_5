import requests
from abc import ABC, abstractmethod


class AbstractHH(ABC):
    """
    Абстрактный класс для получения данных с HeadHunterAPI
    """

    @abstractmethod
    def load_data(self, employer_id: list) -> None:
        """
        Метод получения данных о работодателях и их вакансиях
        :return: Сохраняет в классе полученные данные c сайта HeadHunter.ru
        """
        pass


class HH(AbstractHH):
    """
    Класс для получения данных с сайта HeadHunter.ru
    """

    def __init__(self):
        self.url = 'https://api.hh.ru/'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'page': 0, 'per_page': 100, 'areas': 113, 'only_with_vacancies': True}
        self.vacancies = []
        self.data = []

    def load_data(self, employers: list) -> None:
        """
        Метод получения данных о работодателях и их вакансиях c сайта HeadHunter.ru
        :param employers: Список ID работодателей
        :return: Сохраняет в классе полученные данные c сайта HeadHunter.ru
        """
        for employer_id in employers:
            response_emp = requests.get(self.url + f'employers/{employer_id}', headers=self.headers)
            data_emp = {'id': response_emp.json().get('id'), 'name': response_emp.json().get('name'),
                        'open_vacancies': response_emp.json().get('open_vacancies'),
                        'url': response_emp.json().get('alternate_url')}
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
