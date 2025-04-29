import time
from typing import Annotated

from fastapi import Depends, Request


def get_uptime(request: Request) -> int:
    return int(time.time() - request.app.state.startup_time)


UptimeDI = Annotated["int", Depends(get_uptime)]
