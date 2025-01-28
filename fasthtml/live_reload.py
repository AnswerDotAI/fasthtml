from starlette.routing import WebSocketRoute
from fasthtml.basics import FastHTML, Script

__all__ = ["FastHTMLWithLiveReload"]

def LiveReloadJs(reload_attempts:int=10, reload_interval:float=1000., server_check_attempts:int=20, **kwargs):
    src = """
    (() => {
        const checkServer = () => 
            fetch(window.location.href)
                .then(r => r.ok)
                .catch(() => false);

        const connect = () => {
            const ws = new WebSocket(`ws://${window.location.host}/live-reload`);
            let attempts = 0;
            
            ws.onclose = () => {
                console.log('LiveReload disconnected, checking server...');
                const check = setInterval(async () => {
                    if (attempts++ >= %d) {
                        clearInterval(check);
                        fetch('/live-reload-failed', {method: 'POST'})
                            .then(() => location.reload());
                        return;
                    }
                    
                    if (await checkServer()) {
                        clearInterval(check);
                        location.reload();
                    } else {
                        console.log('Server not ready, retrying...');
                    }
                }, %d);
            };
        };
        
        connect();
    })();
    """
    return Script(src % (server_check_attempts, reload_interval))

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
