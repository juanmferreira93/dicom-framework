from abc import ABC, abstractmethod

from logger.logger import Logger


class Transformation(ABC):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def execute(self, sql_statement):
        pass
