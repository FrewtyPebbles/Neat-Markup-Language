from enum import Enum
from pathlib import Path


class PTOK(Enum):
    NONE = 0
    END_SEC = 1
    AUTO_IND = 2
    END_L = 3
    S_LIST = 4
    E_LIST = 5
    IL_DICT = 6
    IL_S_DICT = 7
    IL_E_DICT = 8


class ConfigSectionTitle:
    def __init__(self, title: str) -> None:
        self.title = title