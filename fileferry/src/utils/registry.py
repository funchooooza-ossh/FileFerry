from typing import Dict, Type
from enum import StrEnum
from repositories.base import BaseRepository


class DBType(StrEnum):
    SQLALCHEMY = "sqlalchemy"
    REDIS = "redis"


class RepositoryName(StrEnum):
    FILE = "file"
    USER = "user"


class Registrator:
    registry: Dict[DBType, Dict[RepositoryName, Type[BaseRepository]]] = {
        DBType.SQLALCHEMY: {},
        DBType.REDIS: {},
    }

    @classmethod
    def register(
        cls, db_type: DBType, name: RepositoryName, repo_class: Type[BaseRepository]
    ):
        """Регистрируем репозиторий для указанного типа базы данных"""
        if db_type not in cls.registry:
            raise ValueError(f"Unsupported database type: {db_type}")
        cls.registry[db_type][name] = repo_class

    @classmethod
    def get(cls, db_type: DBType, name: RepositoryName) -> Type[BaseRepository]:
        """Получаем репозиторий для указанного типа базы данных"""
        try:
            return cls.registry[db_type][name]
        except KeyError:
            raise ValueError(f"'{name.value}' is not registered for {db_type.value}.")

    @classmethod
    def all(cls, db_type: DBType) -> Dict[RepositoryName, Type[BaseRepository]]:
        """Получить все зарегистрированные классы для указанного типа базы данных"""
        return cls.registry.get(db_type, {})
