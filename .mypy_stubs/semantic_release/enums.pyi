from enum import IntEnum

class LevelBump(IntEnum):
    NO_RELEASE = 0
    PRERELEASE_REVISION = 1
    PATCH = 2
    MINOR = 3
    MAJOR = 4
    @classmethod
    def from_string(cls, val: str) -> LevelBump: ...
