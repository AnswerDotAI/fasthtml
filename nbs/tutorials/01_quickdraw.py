from fasthtml.common import *
from datetime import datetime

db = database('data/drawapp.db')
rooms = db.t.rooms
if rooms not in db.t:
    rooms.create(id=int, name=str, created_at=str, pk='id')
Room = rooms.dataclass()

@patch
def __xt__(self:Room):
    return Li(A(self.name, href=f"/rooms/{self.id}"))

app = FastHTML(hdrs=(picolink,))
rt = app.route

@rt("/")
def get():
    create_room = Form(Input(id="room-name", name="name", placeholder="New Room Name"),
                       Button("Create Room"),
                       hx_post="/rooms", hx_target="#rooms-list", hx_swap="afterbegin")
    rooms_list = Ul(*rooms(order_by='id DESC'), id='rooms-list')
    return Titled("QuickDraw", create_room, rooms_list)

@rt("/rooms")
async def post(room:Room):
    room.created_at = datetime.now().isoformat()
    new_room = rooms.insert(room)
    return Li(A(new_room.name, href=f"/rooms/{new_room.id}"))

@rt("/rooms/{id}")
async def get(id:int):
    room = rooms[id]
    return Titled(f"Room: {room.name}", H1(f"Welcome to {room.name}"), A(Button("Leave Room"), href="/"))

if __name__ == "__main__": run_uv()