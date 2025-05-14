from typing import Any

from sfnttools.configs import SfntConfigs
from sfnttools.error import SfntError
from sfnttools.table import SfntTable
from sfnttools.utils.stream import Stream


class MaxpTable(SfntTable):
    @staticmethod
    def create_for_cff(num_glyphs: int = 0) -> 'MaxpTable':
        return MaxpTable(0, 5, num_glyphs)

    @staticmethod
    def create_for_truetype(
            num_glyphs: int = 0,
            max_points: int = 0,
            max_contours: int = 0,
            max_composite_points: int = 0,
            max_composite_contours: int = 0,
            max_zones: int = 0,
            max_twilight_points: int = 0,
            max_storage: int = 0,
            max_function_defs: int = 0,
            max_instruction_defs: int = 0,
            max_stack_elements: int = 0,
            max_size_of_instructions: int = 0,
            max_component_elements: int = 0,
            max_component_depth: int = 0,
    ) -> 'MaxpTable':
        return MaxpTable(
            1,
            0,
            num_glyphs,
            max_points,
            max_contours,
            max_composite_points,
            max_composite_contours,
            max_zones,
            max_twilight_points,
            max_storage,
            max_function_defs,
            max_instruction_defs,
            max_stack_elements,
            max_size_of_instructions,
            max_component_elements,
            max_component_depth,
        )

    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> 'MaxpTable':
        stream = Stream(data)

        major_version, minor_version = stream.read_version_16dot16()
        num_glyphs = stream.read_uint16()

        if (major_version, minor_version) == (0, 5):
            return MaxpTable.create_for_cff(num_glyphs)
        elif (major_version, minor_version) == (1, 0):
            max_points = stream.read_uint16()
            max_contours = stream.read_uint16()
            max_composite_points = stream.read_uint16()
            max_composite_contours = stream.read_uint16()
            max_zones = stream.read_uint16()
            max_twilight_points = stream.read_uint16()
            max_storage = stream.read_uint16()
            max_function_defs = stream.read_uint16()
            max_instruction_defs = stream.read_uint16()
            max_stack_elements = stream.read_uint16()
            max_size_of_instructions = stream.read_uint16()
            max_component_elements = stream.read_uint16()
            max_component_depth = stream.read_uint16()
            return MaxpTable.create_for_truetype(
                num_glyphs,
                max_points,
                max_contours,
                max_composite_points,
                max_composite_contours,
                max_zones,
                max_twilight_points,
                max_storage,
                max_function_defs,
                max_instruction_defs,
                max_stack_elements,
                max_size_of_instructions,
                max_component_elements,
                max_component_depth,
            )
        else:
            raise SfntError(f'[maxp] unsupported table version')

    major_version: int
    minor_version: int
    num_glyphs: int
    max_points: int
    max_contours: int
    max_composite_points: int
    max_composite_contours: int
    max_zones: int
    max_twilight_points: int
    max_storage: int
    max_function_defs: int
    max_instruction_defs: int
    max_stack_elements: int
    max_size_of_instructions: int
    max_component_elements: int
    max_component_depth: int

    def __init__(
            self,
            major_version: int = 0,
            minor_version: int = 0,
            num_glyphs: int = 0,
            max_points: int = 0,
            max_contours: int = 0,
            max_composite_points: int = 0,
            max_composite_contours: int = 0,
            max_zones: int = 0,
            max_twilight_points: int = 0,
            max_storage: int = 0,
            max_function_defs: int = 0,
            max_instruction_defs: int = 0,
            max_stack_elements: int = 0,
            max_size_of_instructions: int = 0,
            max_component_elements: int = 0,
            max_component_depth: int = 0,
    ):
        self.major_version = major_version
        self.minor_version = minor_version
        self.num_glyphs = num_glyphs
        self.max_points = max_points
        self.max_contours = max_contours
        self.max_composite_points = max_composite_points
        self.max_composite_contours = max_composite_contours
        self.max_zones = max_zones
        self.max_twilight_points = max_twilight_points
        self.max_storage = max_storage
        self.max_function_defs = max_function_defs
        self.max_instruction_defs = max_instruction_defs
        self.max_stack_elements = max_stack_elements
        self.max_size_of_instructions = max_size_of_instructions
        self.max_component_elements = max_component_elements
        self.max_component_depth = max_component_depth

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MaxpTable):
            return False
        return (self.major_version == other.major_version and
                self.minor_version == other. minor_version and
                self.num_glyphs == other. num_glyphs and
                self.max_points == other. max_points and
                self.max_contours == other. max_contours and
                self.max_composite_points == other. max_composite_points and
                self.max_composite_contours == other. max_composite_contours and
                self.max_zones == other. max_zones and
                self.max_twilight_points == other. max_twilight_points and
                self.max_storage == other. max_storage and
                self.max_function_defs == other. max_function_defs and
                self.max_instruction_defs == other. max_instruction_defs and
                self.max_stack_elements == other. max_stack_elements and
                self.max_size_of_instructions == other. max_size_of_instructions and
                self.max_component_elements == other. max_component_elements and
                self.max_component_depth == other. max_component_depth)

    def copy(self) -> 'MaxpTable':
        return MaxpTable(
            self.major_version,
            self.minor_version,
            self.num_glyphs,
            self.max_points,
            self.max_contours,
            self.max_composite_points,
            self.max_composite_contours,
            self.max_zones,
            self.max_twilight_points,
            self.max_storage,
            self.max_function_defs,
            self.max_instruction_defs,
            self.max_stack_elements,
            self.max_size_of_instructions,
            self.max_component_elements,
            self.max_component_depth,
        )

    def dump(self, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> tuple[bytes, dict[str, SfntTable]]:
        stream = Stream()

        stream.write_version_16dot16((self.major_version, self.minor_version))
        stream.write_uint16(self.num_glyphs)

        if (self.major_version, self.minor_version) == (0, 5):
            pass
        elif (self.major_version, self.minor_version) == (1, 0):
            stream.write_uint16(self.max_points)
            stream.write_uint16(self.max_contours)
            stream.write_uint16(self.max_composite_points)
            stream.write_uint16(self.max_composite_contours)
            stream.write_uint16(self.max_zones)
            stream.write_uint16(self.max_twilight_points)
            stream.write_uint16(self.max_storage)
            stream.write_uint16(self.max_function_defs)
            stream.write_uint16(self.max_instruction_defs)
            stream.write_uint16(self.max_stack_elements)
            stream.write_uint16(self.max_size_of_instructions)
            stream.write_uint16(self.max_component_elements)
            stream.write_uint16(self.max_component_depth)
        else:
            raise SfntError(f'[maxp] unsupported table version')

        return stream.get_value(), {}
