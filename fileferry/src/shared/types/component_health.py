from __future__ import annotations

from typing import Literal, Optional, TypedDict

ComponentState = Literal["ok", "degraded", "down"]


class ComponentStatus(TypedDict, total=False):
    status: ComponentState  # ← основное состояние
    latency_ms: float  # ← опционально, полезно для алертов
    error: Optional[str]  # ← текст ошибки, если есть
    details: dict[
        str, str | list[str] | ComponentStatus
    ]  # ← версия, кластер, endpoint и т.д.
    aggregated: Literal[True]
