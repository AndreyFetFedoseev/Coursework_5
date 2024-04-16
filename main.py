import requests
from classes.class_DBManager import DBManager
from classes.class_HeadHunter import HH

# params = {
#     'per_page': 100,
#     # 'salary': '100000',
#     # 'experience': 'between1And3',
#     'currency': 'RUR',
#     'only_with_salary': True,
#     'employer_id': '9694561'
# }
# pages = 0
# params1 = {
#     'text': '',
#     'per_page': 20,
#     'page': pages,
#     'only_with_vacancies': True
# }
# response = requests.get('https://api.hh.ru/vacancies', params)
#
# print(response.json())
# params1['text'] = input('Введите ключнвое слово для поиска работодателя: ')
# while pages < 20:
#     response1 = requests.get('https://api.hh.ru/employers', params1)
#     pages += 1
#     print(response1.json())

headhunterAPI = HH()
headhunterAPI.load_data('employers', 'ЕВРАЗ')
print(headhunterAPI.data)
