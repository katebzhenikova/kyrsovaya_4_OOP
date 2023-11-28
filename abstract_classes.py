import os
from abc import ABC, abstractmethod


class APIget(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass
    def save_vacancies_to_file(self):
        pass