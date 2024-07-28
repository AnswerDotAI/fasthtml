from fasthtml.common import *
from datetime import datetime

def render(room):
    return Li(A(room.name, href=f"/rooms/{room.id}"))

app,rt,rooms,Room = fast_app('data/drawapp.db', render=render, id=int, name=str, created_at=str, pk='id')

@rt("/")
def get():
    # The 'Input' id defaults to the same as the name, so you can omit it if you wish
    create_room = Form(Input(id="name", name="name", placeholder="New Room Name"),
                       Button("Create Room"),
                       hx_post="/rooms", hx_target="#rooms-list", hx_swap="afterbegin")
    rooms_list = Ul(*rooms(order_by='id DESC'), id='rooms-list')
    return Titled("QuickDraw", create_room, rooms_list)

@rt("/rooms")
async def post(room:Room):
    room.created_at = datetime.now().isoformat()
    return rooms.insert(room)

@rt("/rooms/{id}")
async def get(id:int):
    room = rooms[id]
    return Titled(f"Room: {room.name}", H1(f"Welcome to {room.name}"), A(Button("Leave Room"), href="/"))

serve()