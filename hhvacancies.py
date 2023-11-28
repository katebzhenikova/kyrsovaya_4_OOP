import os
from abstract_classes import *
import requests
import json


class HH_api_get(APIget):
    def __init__(self, keyword, page=0):
        self._url = 'https://api.hh.ru/vacancies'
        self._params = {
            'text': keyword,
            'page': page
        }

    def get_vacancies(self):
        '''Запрос по параметрам в виде.json'''
        all_vacancies = requests.get(self._url, params=self._params).json()
        return all_vacancies

    def save_vacancies_to_file(self):
        '''Запись полученного запросав файл.json'''
        with open('all_HH_vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(self.get_vacancies(), file, ensure_ascii=False, indent=4)

    def __repr__(self):
        return f'{self.__class__.__name__}({self._url}, {self._params})'

    def __str__(self):
        return f'{self._url}'



class VacanciesHH:

    def __init__(self):
        self.salary_from = 0
        self.salary_to = 0
        self.sort_vacancies = []
        self.sorted_city_name = []


    def sorted_vacancies(self):
        '''Чтение и сортировка полученного файла .json'''
        with open('all_HH_vacancies.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.sort_vacancies = []
        for i in data['items']:
            if i['salary'] is not None:
                self.salary_from = i['salary']['from']
                self.salary_to = i['salary']['to']
                if self.salary_from is None:
                    self.salary_from = 0
                if self.salary_to is None:
                    self.salary_to = 0
            if i['salary'] is None:
                i['salary'] = 'не указано'

            vacancy = {'Вакансия': i['name'], 'URL адрес': i['area']['url'],
                       'Место расположения': i['area']['name'], 'Зарплата от': self.salary_from, 'Зарплата до': self.salary_to,
                       'Опыт работы': i['experience']['name'], 'Требования': i['snippet']['requirement']}

            self.sort_vacancies.append(vacancy)

        return self.sort_vacancies


    def vacancies_in_console(func):
        def wrapper(self, *args, **kwargs):
            '''Обертка для вывода информации пользователю'''
            result = func(self, *args, **kwargs)
            for dictionary in result:
                if isinstance(dictionary, dict):
                    print('---------------')
                    for k in dictionary:
                        print(f'{k}: {dictionary[k]}')
            return result
        return wrapper


    def sorted_by_city(self, city):
        '''Отбор по городу'''
        self.sorted_city_name = []
        if city is None:
             self.sorted_city_name = self.sort_vacancies
        else:
            for item in self.sort_vacancies:
                if item['Место расположения'] == city:
                    self.sorted_city_name.append(item)
        return self.sorted_city_name

    @vacancies_in_console
    def sorted_by_city_print(self):
        '''Отфильтрованный список по городу или без'''
        return self.sorted_city_name



    @vacancies_in_console
    def sorted_by_salary_up(self):
        '''Сортировка зарплаты по возрастанию'''
        sorted_data_up = sorted(self.sorted_city_name, key=lambda x: x['Зарплата от'])
        return sorted_data_up

    @vacancies_in_console
    def sorted_by_salary_down(self):
        '''Сортировка зарплаты по убыванию'''
        sorted_data_down = sorted(self.sorted_city_name, key=lambda x: x['Зарплата от'], reverse=True)
        return sorted_data_down

    @vacancies_in_console
    def sorted_by_salary_range(self, salary_from, salary_to):
        '''Сортировка зарплаты от____ до____'''
        sorted_salary_range = [
            job for job in self.sorted_city_name
            if job['Зарплата от'] and job['Зарплата до']
               and salary_from <= job['Зарплата от'] <= salary_to
               and salary_from <= job['Зарплата до'] <= salary_to
        ]
        return sorted_salary_range

    def __repr__(self):
        return f'{self.__class__.__name__}({self.sorted_city_name}, {self.sorted_by_salary_up}, {self.sorted_by_salary_down})'

    def __str__(self):
        return f'{self.sorted_city_name}'




# hh_api_get = HH_api_get('python')
# v = VacanciesHH()
# hh_api_get.get_vacancies()
# hh_api_get.save_vacancies_to_file()
# v.sorted_vacancies()
# #
# v.sorted_by_city('Москва')
#
# #v.sorted_by_salary_up()
# v.sorted_by_salary_down()
#v.sorted_by_salary_range(10000, 80000)


