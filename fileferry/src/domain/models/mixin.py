from dataclasses import is_dataclass
from typing import Any


class AsDictMixin:
    __asdict_fields__: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        if not is_dataclass(self):
            raise TypeError("as_dict() доступен только для dataclass")

        result: dict[str, Any] = {}
        for name in self.__asdict_fields__:
            attr = getattr(self, name)
            key = name.lstrip("_")
            if hasattr(attr, "value"):
                result[key] = attr.value
            else:
                result[key] = attr
        return result
