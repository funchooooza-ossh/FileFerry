import pytest
from infrastructure.types.health.component_health import ComponentStatus
from infrastructure.types.health.system_health import from_components


@pytest.mark.unit
def test_all_ok_with_aggregated():
    dao_status = ComponentStatus(
        status="ok",
        aggregated=True,
        details={"delegate": {"status": "ok"}, "cache": {"status": "ok"}},
    )

    storage_status = ComponentStatus(status="ok")

    report = from_components(dao_status, storage_status)

    assert report.get("overall") == "ok"
    assert report.get("db").get("status") == "ok"
    assert report.get("cache").get("status") == "ok"
    assert report.get("storage").get("status") == "ok"


@pytest.mark.unit
def test_degraded_when_one_component_down():
    dao_status = ComponentStatus(
        status="ok",
        aggregated=True,
        details={"delegate": {"status": "ok"}, "cache": {"status": "ok"}},
    )

    storage_status = ComponentStatus(status="down")

    report = from_components(dao_status, storage_status)

    assert report.get("overall") == "degraded"
    assert report.get("storage").get("status") == "down"


@pytest.mark.unit
def test_all_down():
    dao_status = ComponentStatus(
        status="down",
        aggregated=True,
        details={"delegate": {"status": "down"}, "cache": {"status": "down"}},
    )

    storage_status = ComponentStatus(status="down")

    report = from_components(dao_status, storage_status)

    assert report.get("overall") == "down"


@pytest.mark.unit
def test_non_aggregated_uses_fallback_cache_status():
    dao_status = ComponentStatus(status="ok")  # aggregated=False by omission

    storage_status = ComponentStatus(status="ok")

    report = from_components(dao_status, storage_status)

    assert report.get("overall") == "ok"
    assert report.get("db").get("status") == "ok"
    assert report.get("cache").get("status") == "ok"
    assert (
        report.get("cache").get("error") == "Cache status not included in healthcheck"
    )


@pytest.mark.unit
def test_partial_data_defaults_to_down():
    dao_status = ComponentStatus(
        status="degraded",
        aggregated=True,
        details={},  # no delegate or cache
    )

    storage_status = ComponentStatus()  # missing status

    report = from_components(dao_status, storage_status)

    assert report.get("overall") == "down"
    assert report.get("db").get("status") == "down"
    assert report.get("cache").get("status") == "down"
    assert report.get("storage").get("status", "down") == "down"
