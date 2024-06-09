from starlette.routing import WebSocketRoute
from fasthtml import FastHTML, Script

__all__ = ["FastHTMLWithLiveReload"]

# TODO:
#  making a single attempt to reload the browser 1 second after the `onclose` event
#  is pretty basic. Let's look at some existing implementations and see if we can
#  make the reload more robust.
LIVE_RELOAD_SCRIPT = """
    (function() {
        var socket = new WebSocket(`ws://${window.location.host}/live-reload`);
        socket.onclose = function() {setTimeout(window.location.reload(), 1000)};
    })();
"""


async def live_reload_websocket(websocket):
    await websocket.accept()


class FastHTMLWithLiveReload(FastHTML):
    """
    `FastHTMLWithLiveReload` enables live reloading.
    This means that any code changes saved on the server will automatically
    trigger a reload of both the server and browser window.

    How does it work?
      - a websocket is creaetd at `/live-reload`
      - a small js snippet `LIVE_RELOAD_SCRIPT` is injected into each webpage
      - this snippet connects to the websocket at `/live-reload` and listens for an `onclose` event
      - when the onclose event is detected the browser reloads after 1 second

    Why do we listen for an `onclose` event?
      When code changes are saved the server automatically reloads if the --reload flag is set.
      The server reload kills the websocket connection. The `onclose` event serves as a proxy
      for "developer has saved some changes".

    Why do we wait for 1 second before reloading the browser?
      We need to allow some time for uvicorn to reload and start serving the latest changes.

    Usage
        >>> from fasthtml.all import *
        >>> app = FastHTMLWithLiveReload()

        Run:
            uvicorn main:app --reload
    """
    LIVE_RELOAD_HEADER = Script(f'{LIVE_RELOAD_SCRIPT}')
    LIVE_RELOAD_ROUTE = WebSocketRoute("/live-reload", endpoint=live_reload_websocket)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("hdrs", []).append(self.LIVE_RELOAD_HEADER)
        kwargs.setdefault("routes", []).append(self.LIVE_RELOAD_ROUTE)
        super().__init__(*args, **kwargs)
