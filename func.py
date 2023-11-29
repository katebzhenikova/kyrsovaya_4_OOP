from hhvacancies import HH_api_get, VacanciesHH
from sjvacancies import SuperJob, VacanciesSJ


def user_interaction():
    while True:

        search_query = str(input('Введите ключевое слово для поиска вакансий:\n').title())

        platform_choise = int(input('''
Здравствуйте, выберите платформу для предоставления вакансий:
1 --> HeadHanter
2 --> Superjob 
0 --> Выйти
Ввод данных: '''))

        if platform_choise == 0:
            quit()

        hh_api_get = HH_api_get(search_query)
        vacancies_hh = VacanciesHH()
        hh_api_get.get_vacancies()
        hh_api_get.save_vacancies_to_file()
        vacancies_hh.read_vacancies()
        vacancies_hh.sorted_vacancies()
        sj = SuperJob(search_query)
        sj.get_vacancies()
        sj.save_vacancies_to_file()
        vacancies_sj = VacanciesSJ()
        vacancies_sj.read_vacancies()
        vacancies_sj.sorted_vacancies()

        if platform_choise == 1:
            vacancies = vacancies_hh
            break
        if platform_choise == 2:
            vacancies = vacancies_sj
            break
        else:
            print('Пожалуйста введите цифру из предложенных вариантов')
            continue

    while True:
        try:
            city_choise = int(input('Отбор по локации:\n1.Отбор по городу.\n2.Без отбора\nВвод данных: '))
        except ValueError:
            print("Ошибка типа данных, пожалуйста, проверьте ввод.")

        if city_choise == 1:
            city = str(input('Введите название локации ')).title()
            if vacancies.sorted_by_city(city):
                break
            else:
                print('-Такой локации не представлено-')
                continue
        if city_choise == 2:
            city = None
            vacancies.sorted_by_city(city)
            break

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
                vacancies.sorted_by_city_print()
                break
        except TypeError:
            print("Ошибка типа данных, пожалуйста, проверьте ввод.")



#user_interaction()