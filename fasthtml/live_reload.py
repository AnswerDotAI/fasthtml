from starlette.routing import WebSocketRoute
from fasthtml.basics import FastHTML, Script

__all__ = ["FastHTMLWithLiveReload"]

def LiveReloadJs(reload_attempts:int=20, reload_interval:int=1000, **kwargs):
    src = """
    (() => {
        let attempts = 0;
        const connect = () => {
            const socket = new WebSocket(`ws://${window.location.host}/live-reload`);
            socket.onopen = async() => {
                const res = await fetch(window.location.href);
                if (res.ok) { 
                    attempts ? window.location.reload() : console.log('LiveReload connected'); 
                }};
            socket.onclose = () => {
                !attempts++ ? connect() : setTimeout(() => { connect() }, %d);
                if (attempts > %d) window.location.reload();
            }};
        connect();
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