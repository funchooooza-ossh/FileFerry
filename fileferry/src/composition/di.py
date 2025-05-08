from typing import TYPE_CHECKING, Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from application.adapters.crud_adapter import FileApplicationAdapter
from application.adapters.system_adapter import SystemAdapter
from composition.containers.application import ApplicationContainer

if TYPE_CHECKING:
    from composition.containers.adapters import AdapterContainer


@inject
def provide_crud_adapter(
    container: Annotated[
        "AdapterContainer", Depends(Provide[ApplicationContainer.adapters])
    ],
) -> FileApplicationAdapter:
    return container.crud_adapter()


AdapterDI = Annotated["FileApplicationAdapter", Depends(provide_crud_adapter)]


@inject
def provide_system_adapter(
    contaniner: Annotated[
        "AdapterContainer", Depends(Provide[ApplicationContainer.adapters])
    ],
) -> SystemAdapter:
    return contaniner.system_adapter()


SystemAdapterDI = Annotated["SystemAdapter", Depends(provide_system_adapter)]
