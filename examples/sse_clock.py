import asyncio
from datetime import datetime
from fasthtml.common import *
from starlette.responses import StreamingResponse

sselink = Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js")
app, rt = fast_app(hdrs=(sselink,))

@rt("/")
def get():
    return Titled("SSE Clock",
            P("XX:XX", sse_swap="TimeUpdateEvent",
            hx_ext="sse", sse_connect="/time-sender"))

async def time_generator():
    while True:
        yield f"""event: TimeUpdateEvent\ndata: {to_xml(P(datetime.now().strftime('%H:%M:%S'), sse_swap="TimeUpdateEvent"))}\n\n"""
        await asyncio.sleep(1)

@rt("/time-sender")
async def get():
    "Send time to all connected clients every second"
    return StreamingResponse(time_generator(), media_type="text/event-stream")

serve()
