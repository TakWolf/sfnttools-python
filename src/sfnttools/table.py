from __future__ import annotations

from abc import abstractmethod

from sfnttools.configs import SfntConfigs


class SfntTable:
    parse_dependencies: list[str] = []

    @staticmethod
    @abstractmethod
    def parse(data: bytes, configs: SfntConfigs, tables: dict[str, SfntTable]) -> SfntTable:
        raise NotImplementedError()

    @abstractmethod
    def copy(self) -> SfntTable:
        raise NotImplementedError()

    def update(self, configs: SfntConfigs, tables: dict[str, SfntTable]):
        pass

    @abstractmethod
    def dump(self, configs: SfntConfigs, tables: dict[str, SfntTable]) -> bytes:
        raise NotImplementedError()
