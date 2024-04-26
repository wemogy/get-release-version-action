from enum import IntEnum

class LevelBump(IntEnum):
    NO_RELEASE: int
    PRERELEASE_REVISION: int
    PATCH: int
    MINOR: int
    MAJOR: int
    @classmethod
    def from_string(cls, val: str) -> LevelBump: ...
