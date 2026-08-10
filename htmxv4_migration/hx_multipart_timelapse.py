from fasthtml.common import *
import asyncio
from asyncio import Event
from multipart_response.fasthtml import MultipartResponse, Part
from starlette.requests import Request


app, rt = fast_app(htmx=False, htmx4=True, exts="multipart")

stop_event = Event()
count = 0
@rt("/")
def home():
    return Div(
        Div(
            hx_multipart_connect="/tick", 
            hx_multipart_close="stop",
            ),
        Button("Stop", hx_get="/stop", hx_swap="none"),
        P("d1: ", id="d1"), 
        P("d2: ", id="d2"), 
        P("d4: ", id="d4"),
    )

@rt("/stop")
def stop(): 
    stop_event.set()

async def parts(start=0):
    global count
    count = max(count,start)
    while not stop_event.is_set():
        count += 1
        yield Part(P(f"d1: {count}"), hx_target="#d1", hx_part_id=str(count))
        if count % 2 == 0: yield Part(P(f"d2: {count//2}"), hx_target="#d2", hx_part_id=str(count))
        if count % 4 == 0: yield Part(P(f"d4: {count//4}"), hx_target="#d4", hx_part_id=str(count))
        await asyncio.sleep(1)
    stop_event.clear()
    yield Part(hx_trigger="stop")


@rt
def tick(hx_last_part_id:str=None):
    return MultipartResponse(parts(int(hx_last_part_id) if hx_last_part_id else 0))

serve()
