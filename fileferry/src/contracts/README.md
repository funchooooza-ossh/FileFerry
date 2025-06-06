# Contracts Layer

Этот слой отвечает за определение контрактов и интерфейсов между слоями приложения. Контракты позволяют изолировать бизнес-логику от инфраструктуры, обеспечивая гибкость и модульность системы.

## 🛠️ Назначение

Contracts Layer служит основой для взаимодействия между слоями:
- Определяет интерфейсы и протоколы для использования в других компонентах.
- Гарантирует стабильность архитектуры при замене реализации.
- Изолирует доменные и инфраструктурные слои через строгие типизации и контракты.

## 🧩 Архитектурные принципы

### 1. Инверсия зависимостей (DIP)
Контракты определяют интерфейсы для бизнес-логики и инфраструктуры, избегая прямой зависимости от конкретных реализаций.

### 2. Модульность
Каждый слой зависит только от абстракций, предоставляемых Contracts Layer. Это позволяет менять реализацию без изменений в юзкейсах и сервисах.

### 3. Единообразие
Все слои приложения следуют единой структуре контрактов, что упрощает поддержку и развитие системы.

## 🚀 Основные преимущества

- **Гибкость при рефакторинге**: Изменение реализации происходит без изменения бизнес-логики.
- **Тестируемость**: Контракты позволяют легко подменять инфраструктуру на моки в тестах.
- **Чистая архитектура**: Логика приложения не зависит от деталей реализации.

