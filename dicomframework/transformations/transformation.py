from abc import ABC, abstractmethod


class Transformation(ABC):
    @abstractmethod
    def run(self):
        print("Parent method: RUN")
        pass

    @abstractmethod
    def execute(self, sql_statement):
        print("Parent method: EXECUTE")
        pass
