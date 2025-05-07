import contextvars

request_id_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)
scope_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "scope", default="unknown"
)


def get_request_id() -> str:
    return request_id_ctx_var.get()


def get_scope() -> str:
    return scope_ctx_var.get()


def set_request_id(request_id: str) -> None:
    request_id_ctx_var.set(request_id)


def set_scope(scope: str) -> None:
    scope_ctx_var.set(scope)
