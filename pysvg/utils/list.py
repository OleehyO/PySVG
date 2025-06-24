from typing import Any


def change_list_type(data: list | Any, new_type: type) -> list | type:
    if isinstance(data, list):
        return [change_list_type(item, new_type) for item in data]
    else:
        return new_type(data)


def get_list_elem(data: list | Any) -> set:
    result = set()
    if isinstance(data, list):
        for item in data:
            result.update(get_list_elem(item))
    else:
        result.add(data)
    return result
