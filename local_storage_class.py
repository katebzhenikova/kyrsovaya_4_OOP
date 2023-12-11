import os
import json

class LocalStorage:
    def __init__(self, filename='all_vacancies.json'):
        self.filename = filename

    def save_data(self, data, mode='w'):
        if not os.path.exists(self.filename):
            mode = 'a'
        with open(self.filename, mode, encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def read_data(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)