import os
from local_storage_class import LocalStorage

class Vacancies:
    def __init__(self, profession, filename='all_vacancies.json'):
        self.storage = LocalStorage()
        self.profession = profession
        self.sort_vacancies = []
        self.sorted_profession_name = []

    def read_vacancies(self):
        self.sort_vacancies = self.storage.read_data()
        return self.sort_vacancies

    def sort_by_profession(self):
        try:
            for item in self.sort_vacancies:
                # if self.profession not in item['Вакансия']:
                #     self.sorted_profession_name = self.sort_vacancies
                #     print('--Вакансий не найдено--')
                #     print('--Отбор будет произведен по ключевому слову--')

                if self.profession in item['Вакансия']:
                    self.sorted_profession_name.append(item)
            return self.sorted_profession_name
        except TypeError:
            print('Не удалось найти вакансии по выбранным параметрам')


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



    @vacancies_in_console
    def sorted_by_salary_up(self):
        '''Сортировка зарплаты по возрастанию'''
        sorted_data_up = sorted(self.sorted_profession_name, key=lambda x: x['Зарплата от'])
        return sorted_data_up

    @vacancies_in_console
    def sorted_by_salary_down(self):
        '''Сортировка зарплаты по убыванию'''
        for i in self.sorted_profession_name:
            if i['Зарплата до'] == 0:
                i['Зарплата до'] = i['Зарплата от']
        sorted_data_down = sorted(self.sorted_profession_name, key=lambda x: x['Зарплата до'], reverse=True)
        return sorted_data_down

    @vacancies_in_console
    def sorted_by_salary_range(self, salary_from, salary_to):
        '''Сортировка зарплаты от____ до____'''
        sorted_salary_range = []
        for job in self.sorted_profession_name:
            if job['Зарплата от'] >= salary_from <= job['Зарплата до']:
                if job['Зарплата до'] <= salary_to >= job['Зарплата от']:
                    sorted_salary_range.append(job)

        return sorted_salary_range

    @vacancies_in_console
    def sorted_by_profession_print(self):
        '''Отфильтрованный список по профессии или без'''
        return self.sorted_profession_name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.sorted_profession_name}, {self.sorted_by_salary_up}, {self.sorted_by_salary_down})'

    def __str__(self):
        return f'{self.sort_vacancies}'



