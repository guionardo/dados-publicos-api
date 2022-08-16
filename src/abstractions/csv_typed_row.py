import inspect


class CSVTypedRow:

    def __init__(self):
        self._get_members()

    def from_row(self, row: str):
        args = row.split(';')
        if len(args) != len(self._members):
            raise ValueError(
                f'{self.__class__.__name__}.from_row() expected {len(self._members)} but received {len(args)}')
        index = 0
        for field_name, field_type in self._members.items():
            setattr(self, field_name, field_type(remove_quotes(args[index])))
            index += 1
        return self

    def _get_members(self):
        for n, v in inspect.getmembers(self):
            if n == '__annotations__':
                self._members = v
                return
        raise TypeError(f'{self.__class__.__name__} has no fields defined')


def remove_quotes(value: str) -> str:
    if value.startswith('"'):
        value = value[1:]
    if value.endswith('"'):
        value = value[:-1]
    return value
