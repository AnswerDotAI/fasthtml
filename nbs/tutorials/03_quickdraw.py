from fasthtml.common import *
from datetime import datetime

def render(room):
    return Li(A(room.name, href=f"/rooms/{room.id}"))

app,rt,rooms,Room = fast_app('data/drawapp.db', render=render, id=int, name=str, created_at=str, canvas_data=str, pk='id')

@rt("/")
def get():
    create_room = Form(Input(id="name", name="name", placeholder="New Room Name"),
                       Button("Create Room"),
                       hx_post="/rooms", hx_target="#rooms-list", hx_swap="afterbegin")
    rooms_list = Ul(*rooms(order_by='id DESC'), id='rooms-list')
    return Titled("QuickDraw", 
                  create_room, rooms_list)

@rt("/rooms")
async def post(room:Room):
    room.created_at = datetime.now().isoformat()
    return rooms.insert(room)

@rt("/rooms/{id}")
async def get(id:int):
    room = rooms[id]
    canvas = Canvas(id="canvas", width="800", height="600")
    color_picker = Input(type="color", id="color-picker", value="#3CDD8C")
    brush_size = Input(type="range", id="brush-size", min="1", max="50", value="10")
    save_button = Button("Save Canvas", id="save-canvas", hx_post=f"/rooms/{id}/save", hx_vals="js:{canvas_data: JSON.stringify(canvas.toJSON())}")

    js = f"""
    var canvas = new fabric.Canvas('canvas');
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.color = '#3CDD8C';
    canvas.freeDrawingBrush.width = 10;

    // Load existing canvas data
    fetch(`/rooms/{id}/load`)
    .then(response => response.json())
    .then(data => {{
        if (data && Object.keys(data).length > 0) {{
            canvas.loadFromJSON(data, canvas.renderAll.bind(canvas));
        }}
    }});
    
    document.getElementById('color-picker').onchange = function() {{
        canvas.freeDrawingBrush.color = this.value;
    }};
    
    document.getElementById('brush-size').oninput = function() {{
        canvas.freeDrawingBrush.width = parseInt(this.value, 10);
    }};
    """
    
    return Titled(f"Room: {room.name}",
                  A(Button("Leave Room"), href="/"),
                  canvas,
                  Div(color_picker, brush_size, save_button),
                  Script(src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js"),
                  Script(js))

@rt("/rooms/{id}/save")
async def post(id:int, canvas_data:str):
    rooms.update({'canvas_data': canvas_data}, id)
    return "Canvas saved successfully"

@rt("/rooms/{id}/load")
async def get(id:int):
    room = rooms[id]
    return room.canvas_data if room.canvas_data else "{}"

serve()