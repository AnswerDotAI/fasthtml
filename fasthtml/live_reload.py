from starlette.routing import WebSocketRoute
from fasthtml.basics import FastHTML, Script

__all__ = ["FastHTMLWithLiveReload"]


def LiveReloadJs(reload_attempts:int=1, reload_interval:float=1000., **kwargs):
    src = """
    (function() {
        var socket = new WebSocket(`ws://${window.location.host}/live-reload`);
        var maxReloadAttempts = %s;
        var reloadInterval = %s; // time between reload attempts in ms
        socket.onclose = function() {
            let reloadAttempts = 0;
            const intervalFn = setInterval(function(){
                window.location.reload();
                reloadAttempts++;
                if (reloadAttempts === maxReloadAttempts) clearInterval(intervalFn);
            }, reloadInterval);
        }
    })();
"""
    return Script(src % (reload_attempts, reload_interval))

async def live_reload_ws(websocket): await websocket.accept()

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
            serve()
    """
    def __init__(self, *args, **kwargs):
        # "hdrs" and "routes" can be missing, None, a list or a tuple.
        kwargs["hdrs"] = [*(kwargs.get("hdrs") or []), LiveReloadJs(**kwargs)]
        kwargs["routes"] = [*(kwargs.get("routes") or []), WebSocketRoute("/live-reload", endpoint=live_reload_ws)]
        super().__init__(*args, **kwargs)
