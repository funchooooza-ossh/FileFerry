from typing import Callable, Dict, Type, TYPE_CHECKING, TypeVar, Generic

if TYPE_CHECKING:
    from repositories.sqlalchemy.base import BaseSqlAlchemyRepository

T_SQLAlchemy = TypeVar("T_SQLAlchemy", bound="BaseSqlAlchemyRepository")


T = TypeVar("T")  # Общий тип для любых классов


class Registry(Generic[T]):
    def __init__(self):
        self._registry: Dict[str, Type[T]] = {}

    def register(self, name: str) -> Callable[[Type[T]], Type[T]]:
        """Декоратор для регистрации класса по имени"""

        def wrapper(cls: Type[T]) -> Type[T]:
            self._registry[name] = cls
            return cls

        return wrapper

    def get(self, name: str) -> Type[T]:
        """Получить класс по имени"""
        try:
            return self._registry[name]
        except KeyError:
            raise ValueError(f"'{name}' is not registered.")

    def all(self) -> Dict[str, Type[T]]:
        """Получить все зарегистрированные классы"""
        return dict(self._registry)


SqlAlchemyRegistry = Registry[BaseSqlAlchemyRepository]()
