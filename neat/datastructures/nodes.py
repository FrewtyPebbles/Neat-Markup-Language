
class ConfigAttribute:
    def __init__(self, key, val) -> None:
        self.key = key
        self.val = val


class ConfigSection:
    def __init__(self, section_name: str) -> None:
        self.scope = []
        self.section_name = section_name

    def push(self, attr: ConfigAttribute):
        self.scope.append(attr)
