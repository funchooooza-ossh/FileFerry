# ADR-0001: Архитектура микросервиса FileFerry

## Статус
Принято


## Контекст
Сервис изолирует хранение файлов. Требуется чистая архитектура, которая станет ядром, которое в будущем можно будет расширять в любом направлении.

## Решение
Используем около DDD:

- Domain Layer содержит бизнес-ядро (VO, сущности).
- Application Layer реализует UseCases и Adapters, предоставляет транспортному слою интерфейс получения того, что ему нужно.
- Infrastructure Layer реализует контракты(DataAccess, Storage).
- Transport Layer предоставляет HTTP API и Message broker in future.

Инжекция зависимостей реализована через `dependency-injector`. Все зависимости передаются через адаптеры. UseCases не зависят от FastAPI, SQLAlchemy и т.п.

## Альтернативы
- Service Layer без доменного слоя - слабо масштабируется, архитектурно грубое и грязное решение.
- Чистая MVC - отвергнуто, не дает ни изоляции, ни модульности.

## Последствия
- Около-высока, явно выше среднего модульность.
- Простота тестирования.
- Инфраструктура не имеет веса для остальных слоёв.

