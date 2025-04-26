import pytest
from api.rest.di_context import make_di_resolver
from application.orchestrators.retrieve_file_adapter import RetrieveFileAPIAdapter
from application.orchestrators.upload_file_adapter import UploadFileAPIAdapter
from contracts.composition import FileAction, ScenarioName


@pytest.mark.parametrize(
    "scenario, action, service_type",
    [
        (ScenarioName.MINIO_SQLA, FileAction.RETRIEVE, RetrieveFileAPIAdapter),
        (ScenarioName.MINIO_SQLA, FileAction.UPLOAD, UploadFileAPIAdapter),
    ],
)
@pytest.mark.asyncio
async def test_resolving(scenario: ScenarioName, action: FileAction, service_type):  # type: ignore
    """
    Мега важно дополнять эти тесты для проверки корректности резолва зависимостей
    """

    service = make_di_resolver(action=action)(
        x_scenario=scenario, x_bucket="default-bucket"
    )

    assert isinstance(service, service_type)
