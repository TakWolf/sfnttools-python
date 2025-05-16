from __future__ import annotations

from abc import abstractmethod

from sfnttools.configs import SfntConfigs


class SfntTable:
    parse_dependencies: list[str] = []
    update_dependencies: list[str] = []
    dump_dependencies: list[str] = []
    dump_generates: list[str] = []

    @staticmethod
    @abstractmethod
    def parse(data: bytes, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> SfntTable:
        raise NotImplementedError()

    @abstractmethod
    def copy(self) -> SfntTable:
        raise NotImplementedError()

    def update(self, configs: SfntConfigs, dependencies: dict[str, SfntTable]):
        pass

    @abstractmethod
    def dump(self, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> tuple[bytes, dict[str, SfntTable]]:
        raise NotImplementedError()
