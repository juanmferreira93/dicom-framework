from abc import ABC, abstractmethod


class Transformation(ABC):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def execute(self, sql_statement):
        pass
