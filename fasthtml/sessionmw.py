from fasthtml.core import MiddlewareBase
from fasthtml.starlette import *
from starlette.types import Message
from typing import Optional, Callable


def _session_normalize(obj):
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif isinstance(obj, (list, dict)):
        return obj
    elif hasattr(obj, "__json__"):
        return obj.__json__()
    elif hasattr(obj, "__str__"):
        return str(obj)
    elif hasattr(obj, "__dict__"):
        return obj.__dict__
    else:
        raise TypeError(
            f"Object of type {obj.__class__.__name__} is not JSON serializable"
        )


class SessionNormalizerMiddleware(MiddlewareBase):
    def __init__(self, app, normalizer: Optional[Callable] = None):
        self.app = app
        self.normalizer = normalizer

    async def __call__(self, scope, receive, send) -> None:
        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                if scope["session"]:
                    for key, val in scope["session"].items():
                        scope["session"][key] = (
                            _session_normalize(val)
                            if not self.normalizer
                            else self.normalizer(val)
                        )
            await send(message)

        await self.app(scope, receive, send_wrapper)


def session_normalize(normalizer: Optional[Callable] = None) -> Middleware:
    """
    Attempts to convert stored data in the persisted session object to a format
    that can be serialized.
    """
    return Middleware(SessionNormalizerMiddleware, normalizer=normalizer)
