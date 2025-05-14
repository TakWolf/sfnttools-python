from abc import abstractmethod


class SfntFlags:
    @staticmethod
    @abstractmethod
    def parse(value: int) -> 'SfntFlags':
        raise NotImplementedError()

    def __repr__(self) -> str:
        return repr(self.value)

    @property
    @abstractmethod
    def value(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def copy(self) -> 'SfntFlags':
        raise NotImplementedError()
