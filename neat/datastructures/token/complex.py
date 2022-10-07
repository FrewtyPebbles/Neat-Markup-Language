from enum import Enum


class PTOK(Enum):
    NONE = 0
    END_SEC = 1
    AUTO_IND = 2
    END_L = 3
    S_LIST = 4
    E_LIST = 5


class ConfigSectionTitle:
    def __init__(self, title: str) -> None:
        self.title = title
