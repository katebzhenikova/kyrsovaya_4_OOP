import os
from abc import ABC, abstractmethod
import requests
import json

class APIget(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass
    def save_vacancies_to_file(self):
        pass

class HH_api_get(APIget):
    def __init__(self, keyword, page=0):
        self._url = 'https://api.hh.ru/vacancies'
        self._params = {
            'text': keyword,
            'page': page
        }

    def get_vacancies(self):
        all_vacancies = requests.get(self._url, params=self._params).json()
        return all_vacancies

    def save_vacancies_to_file(self):
        with open('all_HH_vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(self.get_vacancies(), file, ensure_ascii=False, indent=4)



class VacanciesHH:

    def __init__(self):
        self.sort_vacancies = []
        self.sorted_city_name = []
        self.data_with_salary = []
        self.non_zero_salary_jobs = []
        self.zero_salary_jobs = []




    def sorted_vacancies(self):
        with open('all_HH_vacancies.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.sort_vacancies = [
            {'Вакансия': i['name'], 'URL адрес': i['area']['url'],
             'Место расположения': i['area']['name'], 'Зарплата': i['salary'],
             'Опыт работы': i['experience']['name'], 'Требования': i['snippet']['requirement']}
            for i in data['items']]
        for item in self.sort_vacancies:
            if item['Зарплата'] is None:
                item['Зарплата'] = 'не указано'
            if item['Зарплата'] != 'не указано':
                if item['Зарплата']['to'] is None:
                    item['Зарплата']['to'] = 0
                if item['Зарплата']['from'] is None:
                    item['Зарплата']['from'] = 0

        return self.sort_vacancies

    def vacancies_in_console(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            for dictionary in result:
                if isinstance(dictionary, dict):
                    print('---------------')
                    for k in dictionary:
                        print(f'{k}: {dictionary[k]}')
            return result
        return wrapper

    #@vacancies_in_console
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
        return self.sorted_city_name

    @vacancies_in_console
    def salary_none(self):
        '''Значения ключа зарплата равно "не указано"'''
        self.zero_salary_jobs = [i for i in self.sorted_city_name if i['Зарплата'] == 'не указано']
        return self.zero_salary_jobs


    def no_salary(self):
        '''Значения ключа зарплата не равно 'не указано' для использования внутри класса, чтобы сортировать зарплату'''
        self.non_zero_salary_jobs = [i for i in self.sorted_city_name if i.get('Зарплата') and i['Зарплата'] != 'не указано']
        return self.non_zero_salary_jobs


    @vacancies_in_console
    def sorted_by_salary_up(self):
        '''Сортировка зарплаты по возрастанию'''
        sorted_data_up = sorted(self.non_zero_salary_jobs, key=lambda x: x['Зарплата']['from'])
        return sorted_data_up

    @vacancies_in_console
    def sorted_by_salary_down(self):
        '''Сортировка зарплаты по убыванию'''
        sorted_data_down = sorted(self.non_zero_salary_jobs, key=lambda x: x['Зарплата']['from'], reverse=True)
        return sorted_data_down

    @vacancies_in_console
    def sorted_by_salary_range(self, salary_from, salary_to):
        '''Сортировка зарплаты от____ до____'''
        sorted_salary_range = [
            job for job in self.non_zero_salary_jobs
            if job['Зарплата']['from'] and job['Зарплата']['to']
               and salary_from <= job['Зарплата']['from'] <= salary_to
               and salary_from <= job['Зарплата']['to'] <= salary_to
        ]
        return sorted_salary_range



# hh_api_get = HH_api_get('python')
# v = VacanciesHH()
# hh_api_get.get_vacancies()
# hh_api_get.save_vacancies_to_file()
# v.sorted_vacancies()
# v.sorted_by_city('Москва')
# v.sort_vacancies
# v.sorted_by_city('Москва')
# v.no_salary()
# v.sorted_by_salary_up()
# #v.sorted_by_salary_down()
#v.sorted_by_salary_range(10000, 80000)


