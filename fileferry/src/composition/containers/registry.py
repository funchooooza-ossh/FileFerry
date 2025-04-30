from enum import StrEnum

from dependency_injector.containers import DeclarativeContainer

from composition.containers.application import ApplicationContainer


class Containers(StrEnum):
    PRIMARY = "primary"
    MONGO = "mongo"


CONTAINERS: dict[Containers, type[DeclarativeContainer]] = {
    Containers.PRIMARY: ApplicationContainer,
}


def get_container(profile: str) -> type[DeclarativeContainer]:
    try:
        profile = Containers(profile)
        return CONTAINERS[profile]
    except (KeyError, ValueError):
        raise ValueError(f"Unknown container profile: {profile}") from None
