import os
from abc import ABC, abstractmethod


class APIget(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass
    def sorted_vacancies(self):
        pass

    def get_and_save_sorted_vacancies(self):
        pass
