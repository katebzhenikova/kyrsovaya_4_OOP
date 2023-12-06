import os
from abstract_classes import *
from local_storage_class import *
import requests
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout
import json


class HH_api_get(APIget):
    def __init__(self, keyword, page=0):
        self._url = 'https://api.hh.ru/vacancies'
        self._params = {
            'text': keyword,
            'page': page
        }
        self.storage = LocalStorage()
        self.data = {}

    def get_vacancies(self):
        '''Запрос по параметрам в виде.json'''
        try:
            self.data = requests.get(self._url, params=self._params).json()
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
        self.sort_vacancies = []
        for i in self.data['items']:
            if i['salary'] is not None:
                self.salary_from = i['salary']['from']
                self.salary_to = i['salary']['to']
                if self.salary_from is None:
                    self.salary_from = 0
                if self.salary_to is None:
                    self.salary_to = 0
            if i['salary'] is None:
                self.salary_from = 0
                self.salary_to = 0
            vacancy = {'Вакансия': (i['name']).lower(), 'URL адрес': i['area']['url'],
                       'Место расположения': i['area']['name'], 'Зарплата от': self.salary_from,
                       'Зарплата до': self.salary_to,
                       'Опыт работы': i['experience']['name'], 'Требования': i['snippet']['requirement']}

            self.sort_vacancies.append(vacancy)

        return self.sort_vacancies

    def get_and_save_sorted_vacancies(self):
        self.get_vacancies()
        sorted_data = self.sorted_vacancies()
        self.storage.save_data(sorted_data)
        return sorted_data


