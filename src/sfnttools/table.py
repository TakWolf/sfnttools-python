from abc import abstractmethod


class SfntTable:
    parse_dependencies: list[str] = []
    dump_dependencies: list[str] = []

    @staticmethod
    @abstractmethod
    def parse(data: bytes, dependencies: dict[str, 'SfntTable']) -> 'SfntTable':
        raise NotImplementedError()

    @abstractmethod
    def copy(self) -> 'SfntTable':
        raise NotImplementedError()

    @abstractmethod
    def dump(self, dependencies: dict[str, 'SfntTable']) -> tuple[bytes, dict[str, 'SfntTable']]:
        raise NotImplementedError()
