from hhvacancies import*

class SuperJob(APIget):
    def __init__(self, keyword, page=1):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.params = {
            'keywords': keyword,
            'page': page
        }

    def get_vacancies(self):
        '''Запрос по параметрам .json'''
        headers = {'X-Api-App-Id': os.environ['API_SuperJob']}
        return requests.get(self.url, headers=headers, params=self.params).json()

    def save_vacancies_to_file(self):
        '''Запись полученного запросав файл.json'''
        with open('all_SJ_vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(self.get_vacancies(), file, ensure_ascii=False, indent=4)


class VacanciesSJ(VacanciesHH):
    def __init__(self):
        super().__init__()

    def sorted_vacancies(self):
        '''Чтение и сортировка полученного файла .json'''
        with open('all_SJ_vacancies.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.sort_vacancies = [{'Вакансия': i['profession'], 'URL адрес': i['client']['link'],
                            'Место расположения': i['client']['town']['title'], 'Зарплата от': i['payment_from'],
                            'Зарплата до': i['payment_to'], 'Опыт работы': i['experience']['title'], 'Требования': i['candidat']}
                             for i in data['objects']]
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
    def sorted_by_salary_up(self):
        '''Сортировка зарплаты по возрастанию'''
        sorted_data_up = sorted(self.sorted_city_name, key=lambda x: x['Зарплата от'])
        return sorted_data_up

    @vacancies_in_console
    def sorted_by_salary_down(self):
        '''Сортировка зарплаты по убыванию'''
        for i in self.sorted_city_name:
            if i['Зарплата до'] == 0:
                i['Зарплата до'] = i['Зарплата от']
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

    @vacancies_in_console
    def sorted_by_city_print(self):
        '''Отфильтрованный список по городу или без'''
        return self.sorted_city_name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.sorted_city_name}, {self.sorted_by_salary_up}, {self.sorted_by_salary_down})'

    def __str__(self):
        return f'{self.sort_vacancies}'



#
# sj = SuperJob('python')
# sj.get_vacancies()
# sj.save_vacancies_to_file()
# vsj = VacanciesSJ()
# vsj.sorted_vacancies()
# vsj.sorted_by_city(None)
# vsj.sorted_by_salary_up()
# #vsj.sorted_by_salary_down()
# vsj.sorted_by_salary_range(0, 100000)



