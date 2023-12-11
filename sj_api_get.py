import os
from abstract_classes import *
from local_storage_class import *
import requests
import json



class SuperJob(APIget):
    def __init__(self, keyword, page=1):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.params = {
            'keywords': keyword,
            'page': page
        }
        self.storage = LocalStorage()
        self.data = {}

    def get_vacancies(self):
        try:
            headers = {'X-Api-App-Id': os.environ['API_SuperJob']}
            self.data = requests.get(self.url, headers=headers, params=self.params).json()
            self.storage.save_data(self.data)
            return self.data
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error")
            print(errh.args[0])
        except requests.exceptions.ReadTimeout as errrt:
            print("Time out")
        except requests.exceptions.ConnectionError as conerr:
            print("Connection error")
        except requests.exceptions.RequestException as errex:
            print("Exception request")



    def sorted_vacancies(self):
        '''Сортировка полученного файла .json'''
        try:
            sort_vacancies = [{'Вакансия': (i['profession']).lower(), 'URL адрес': i['client']['link'],
                                'Место расположения': i['client']['town']['title'], 'Зарплата от': i['payment_from'],
                                'Зарплата до': i['payment_to'], 'Опыт работы': i['experience']['title'], 'Требования': i['candidat']}
                                 for i in self.data['objects']]
            return sort_vacancies
        except KeyError:
            print('Не удалось найти вакансии по выбранным параметрам')

    def get_and_save_sorted_vacancies(self):
        self.get_vacancies()
        sorted_data = self.sorted_vacancies()
        self.storage.save_data(sorted_data)
        return sorted_data