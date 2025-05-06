from prometheus_client import Gauge

# --- Метрики ---
important_tasks_active = Gauge(
    "fileferry_important_tasks_active_count",
    "Текущее количество активных задач",
)

important_tasks_total = Gauge(
    "fileferry_important_tasks_total_count",
    "Общее количество задач с момента запуска",
)

important_tasks_age = Gauge(
    "fileferry_important_tasks_age_seconds",
    "Возраст задачи в секундах",
    ["key"],
)
