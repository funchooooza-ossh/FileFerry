from typing import TYPE_CHECKING, Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from application.adapter import FileApplicationAdapter
from composition.containers.application import ApplicationContainer

if TYPE_CHECKING:
    from composition.containers.adapters import AdapterContainer


@inject
def provide_adapter(
    container: Annotated[
        "AdapterContainer", Depends(Provide[ApplicationContainer.adapters])
    ],
) -> FileApplicationAdapter:
    return container.file_application_adapter()


AdapterDI = Annotated["FileApplicationAdapter", Depends(provide_adapter)]
