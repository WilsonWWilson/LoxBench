from enum import IntEnum, IntFlag


class MsVersion(IntEnum):
    pass


class Permission(IntFlag):
    NONE = 0
    ANON = 1
    USER = 2
    ADMIN = 4
    ALL = ANON | USER | ADMIN


class Protocol(IntFlag):
    NONE = 0
    HTTP = 1
    WS = 2
    ALL = HTTP | WS
