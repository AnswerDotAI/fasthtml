from starlette.routing import WebSocketRoute
from fasthtml import FastHTML, Script

__all__ = ["FastHTMLWithLiveReload"]


LIVE_RELOAD_SCRIPT = """
    (function() {{
        var socket = new WebSocket(`ws://${{window.location.host}}/live-reload`);
        var maxReloadAttempts = {reload_attempts};
        var reloadInterval = {reload_interval}; // time between reload attempts in ms
        socket.onclose = function() {{
            let reloadAttempts = 0;
            const intervalFn = setInterval(function(){{
                window.location.reload();
                reloadAttempts++;
                if (reloadAttempts === maxReloadAttempts) clearInterval(intervalFn);
            }}, reloadInterval);
        }}
    }})();
"""


async def live_reload_websocket(websocket):
    await websocket.accept()


class FastHTMLWithLiveReload(FastHTML):
    """
    `FastHTMLWithLiveReload` enables live reloading.
    This means that any code changes saved on the server will automatically
    trigger a reload of both the server and browser window.

    How does it work?
      - a websocket is created at `/live-reload`
      - a small js snippet `LIVE_RELOAD_SCRIPT` is injected into each webpage
      - this snippet connects to the websocket at `/live-reload` and listens for an `onclose` event
      - when the `onclose` event is detected the browser is reloaded

    Why do we listen for an `onclose` event?
      When code changes are saved the server automatically reloads if the --reload flag is set.
      The server reload kills the websocket connection. The `onclose` event serves as a proxy
      for "developer has saved some changes".

    Usage
        >>> from fasthtml.common import *
        >>> app = FastHTMLWithLiveReload()

        Run:
            run_uv()
    """
    LIVE_RELOAD_ROUTE = WebSocketRoute("/live-reload", endpoint=live_reload_websocket)

    def __init__(self, *args, **kwargs):
        # Create the live reload script to be injected into the webpage
        self.LIVE_RELOAD_HEADER = Script(
            LIVE_RELOAD_SCRIPT.format(
                reload_attempts=kwargs.get("reload_attempts", 1),
                reload_interval=kwargs.get("reload_interval", 1000),
            )
        )
        
        # "hdrs" and "routes" can be missing, None, a list or a tuple.
        kwargs["hdrs"] = [*(kwargs.get("hdrs") or []), self.LIVE_RELOAD_HEADER]
        kwargs["routes"] = [*(kwargs.get("routes") or []), self.LIVE_RELOAD_ROUTE]
        super().__init__(*args, **kwargs)

