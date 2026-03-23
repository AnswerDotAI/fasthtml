from fasthtml.common import *
from starlette.testclient import TestClient
import contextlib

# Test basic app creation works (previously crashed with Starlette 1.0)
def test_basic_app():
    app, rt = fast_app()
    cli = TestClient(app)
    @rt('/')
    def get(): return P('hello')
    res = cli.get('/')
    assert 'hello' in res.text

def test_on_startup_shutdown():
    started, stopped = [], []
    app = FastHTML(on_startup=[lambda: started.append(1)], on_shutdown=[lambda: stopped.append(1)])
    cli = TestClient(app)
    with cli:
        assert started == [1]
    assert stopped == [1]

def test_lifespan_only():
    state = []
    @contextlib.asynccontextmanager
    async def lifespan(app):
        state.append('started')
        yield
        state.append('stopped')
    app = FastHTML(lifespan=lifespan)
    cli = TestClient(app)
    with cli:
        assert state == ['started']
    assert state == ['started', 'stopped']

def test_lifespan_with_startup_shutdown():
    order = []
    @contextlib.asynccontextmanager
    async def lifespan(app):
        order.append('lifespan_start')
        yield
        order.append('lifespan_stop')
    app = FastHTML(
        lifespan=lifespan,
        on_startup=[lambda: order.append('on_startup')],
        on_shutdown=[lambda: order.append('on_shutdown')],
    )
    cli = TestClient(app)
    with cli:
        assert order == ['on_startup', 'lifespan_start']
    assert order == ['on_startup', 'lifespan_start', 'lifespan_stop', 'on_shutdown']

def test_async_startup_shutdown():
    state = []
    async def astart(): state.append('async_start')
    async def astop(): state.append('async_stop')
    app = FastHTML(on_startup=[astart], on_shutdown=[astop])
    cli = TestClient(app)
    with cli:
        assert state == ['async_start']
    assert state == ['async_start', 'async_stop']

def test_shutdown_runs_on_lifespan_error():
    state = []
    @contextlib.asynccontextmanager
    async def lifespan(app):
        yield
        raise RuntimeError('lifespan error')
    app = FastHTML(
        lifespan=lifespan,
        on_shutdown=[lambda: state.append('shutdown')],
    )
    cli = TestClient(app, raise_server_exceptions=False)
    try:
        with cli: pass
    except RuntimeError: pass
    assert state == ['shutdown']
