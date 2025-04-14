from typing import Callable, Dict, Type, TypeVar, Generic

from repositories.sqlalchemy.base import BaseSqlAlchemyRepository


T_reg = TypeVar("T_reg")


class Registry(Generic[T_reg]):
    def __init__(self):
        self._registry: Dict[str, Type[T_reg]] = {}

    def register(self, name: str) -> Callable[[Type[T_reg]], Type[T_reg]]:
        """Декоратор для регистрации класса по имени"""

        def wrapper(cls: Type[T_reg]) -> Type[T_reg]:
            self._registry[name] = cls
            return cls

        return wrapper

    def get(self, name: str) -> Type[T_reg]:
        """Получить класс по имени"""
        try:
            return self._registry[name]
        except KeyError:
            raise ValueError(f"'{name}' is not registered.")

    def all(self) -> Dict[str, Type[T_reg]]:
        """Получить все зарегистрированные классы"""
        return dict(self._registry)


SqlAlchemyRegistry = Registry[BaseSqlAlchemyRepository]()
