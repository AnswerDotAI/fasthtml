from fasthtml.common import *
from datetime import datetime

db = database('data/drawapp.db')
rooms = db.t.rooms
if rooms not in db.t:
    rooms.create(id=int, name=str, created_at=str, pk='id', canvas_data=str)
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
    save_button = Button("Save Canvas", id="save-canvas", hx_post=f"/rooms/{id}/save", hx_vals="js:{canvas_data: JSON.stringify(canvas.toJSON())}")

    js = f"""
    var canvas = new fabric.Canvas('canvas');
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.color = '#000000';
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
    print(canvas_data)
    rooms.update({'canvas_data': canvas_data}, id)
    return "Canvas saved successfully"

@rt("/rooms/{id}/load")
async def get(id:int):
    room = rooms[id]
    print(room.canvas_data)
    return room.canvas_data if room.canvas_data else "{}"

if __name__ == "__main__": run_uv()