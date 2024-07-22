from fasthtml.common import *
from datetime import datetime

def render(room):
    return Li(A(room.name, href=f"/rooms/{room.id}"))

app,rt,rooms,Room = fast_app('data/drawapp.db', hdrs=(picolink,), render=render, id=int, name=str, created_at=str, pk='id')

@rt("/")
def get():
    create_room = Form(Input(id="room-name", name="name", placeholder="New Room Name"),
                       Button("Create Room"),
                       hx_post="/rooms", hx_target="#rooms-list", hx_swap="afterbegin")
    rooms_list = Ul(*rooms(order_by='id DESC'), id='rooms-list')
    return Titled("QuickDraw",
                  create_room, rooms_list)

@rt("/rooms")
async def post(room:Room):
    room.created_at = datetime.now().isoformat()
    new_room = rooms.insert(room)
    return Li(A(new_room.name, href=f"/rooms/{new_room.id}"))

@rt("/rooms/{id}")
async def get(id:int):
    room = rooms[id]
    canvas = Canvas(id="canvas", width="800", height="600")
    color_picker = Input(type="color", id="color-picker", value="#000000")
    brush_size = Input(type="range", id="brush-size", min="1", max="50", value="10")
    
    js = """
    var canvas = new fabric.Canvas('canvas');
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.color = '#000000';
    canvas.freeDrawingBrush.width = 10;
    
    document.getElementById('color-picker').onchange = function() {
        canvas.freeDrawingBrush.color = this.value;
    };
    
    document.getElementById('brush-size').oninput = function() {
        canvas.freeDrawingBrush.width = parseInt(this.value, 10);
    };
    """
    
    return Titled(f"Room: {room.name}",
                  A(Button("Leave Room"), href="/"),
                  canvas,
                  Div(color_picker, brush_size),
                  Script(src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js"),
                  Script(js))

run_uv()