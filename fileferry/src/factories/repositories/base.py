from __future__ import annotations
from typing import (
    Dict,
    TypeVar,
    Callable,
    AsyncGenerator,
    Any,
    Optional,
    Generic,
    Type,
    ClassVar,
)
from typing_extensions import Self
from contextlib import AbstractAsyncContextManager
from utils import Registry

T_repo = TypeVar("T_repo")
R = TypeVar("Registry", bound="Registry[Any]")
F = TypeVar("RepositoryFactoryType", bound="BaseRepositoryFactory")


class BaseRepositoryFactory(AbstractAsyncContextManager, Generic[T_repo]):
    registry: ClassVar[Registry] = None

    def __init__(
        self,
        session_ctx_factory: Callable[[], AsyncGenerator[Any, None]],
    ):
        self._session_ctx_factory = session_ctx_factory
        self._session: Optional[Any] = None
        self._instances: Dict[str, T_repo] = {}

    def __init_subclass__(cls):
        if cls.registry is None:
            raise TypeError(f"{cls.__name__} must define 'registry' class attribute")
        super().__init_subclass__()

    async def __aenter__(self) -> Self:
        self._session_ctx = self._session_ctx_factory()
        self._session = await self._session_ctx.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session_ctx.__aexit__(exc_type, exc_val, exc_tb)
        self._session = None
        self._instances.clear()

    def get(self, name: str) -> T_repo:
        if not self._session:
            raise RuntimeError("RepositoryFactory must be used within an async context")

        if name in self._instances:
            return self._instances[name]

        try:
            repo_cls = self.registry.get(name)
        except ValueError as exc:
            raise KeyError(
                f"Repository '{name}' is not registered in {self.__class__.__name__}"
            ) from exc

        repo = repo_cls(self._session)
        self._instances[name] = repo
        return repo

    def __contains__(self, name: str) -> bool:
        return name in self._instances or name in self.registry._registry

    def __iter__(self):
        return iter(self._instances.items())

    @classmethod
    async def with_session_factory(
        cls: Type[F], session_factory: Callable[[], AsyncGenerator[Any, None]]
    ) -> F:
        async def dependency_provider() -> F:
            return cls(session_factory)

        return await dependency_provider()
