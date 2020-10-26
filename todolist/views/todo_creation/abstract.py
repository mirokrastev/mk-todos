from abc import abstractmethod, ABC


class AbstractMakeTodos(ABC):
    @abstractmethod
    def make_todos(self, *args):
        pass
