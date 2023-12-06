import os
from hh_api_get import HH_api_get
from sj_api_get import SuperJob
from vacancies_class import Vacancies


def user_interaction():
    while True:
        search_query = str(input('Здравствуйте! Введите ключевое слово для поиска вакансий:\n'))
        profession = str(input('Введите наименование вакансий:\n'))
        try:
            platform_choise = int(input('''
Выберите платформу для предоставления вакансий:
1 --> HeadHanter
2 --> Superjob 
0 --> Выйти
Ввод данных: '''))
        except ValueError:
            print('Ошибка ввода, попробуйте еще раз!')
            continue
        if platform_choise == 0:
            quit()

        if platform_choise == 1:
            hh_api_get = HH_api_get(search_query)
            hh_api_get.get_vacancies()
            hh_api_get.sorted_vacancies()
            hh_api_get.get_and_save_sorted_vacancies()
            break
        if platform_choise == 2:
            sj_api_get = SuperJob(search_query)
            sj_api_get.get_vacancies()
            sj_api_get.sorted_vacancies()
            sj_api_get.get_and_save_sorted_vacancies()
            break
        else:
            print('Пожалуйста введите цифру из предложенных вариантов')
            continue

    vacancies = Vacancies(profession)
    vacancies.read_vacancies()
    vacancies.sort_by_profession()

    while True:
        try:
            vacancies_filter = int(input('''
Отбор вакансий:
1 --> Зарплата по возрастанию
2 --> Зарплата по убыванию
3 --> Зарплата от __ до __
0 --> Без фильтра
Ввод данных: '''))
        except ValueError:
            print('Ошибка ввода, попробуйте еще раз!')
            continue
        try:
            if vacancies_filter == 1:
                vacancies.sorted_by_salary_up()
                break
            if vacancies_filter == 2:
                vacancies.sorted_by_salary_down()
                break
            if vacancies_filter == 3:
                salary_from = int(input('Введите зарплата от '))
                salary_to = int(input('Введите зарплата до '))
                vacancies.sorted_by_salary_range(salary_from, salary_to)
                break
            if vacancies_filter == 0:
                vacancies.sorted_by_profession_print()
                break
        except TypeError:
            print("Ошибка типа данных, пожалуйста, проверьте ввод.")



#user_interaction()