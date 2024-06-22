from sqlite_minutils import Database
from fastlite import *
from fastlite.kw import *
from fastcore.parallel import threaded
from starlette.responses import FileResponse
from starlette.requests import Request
from fastcore.utils import *
from fastcore.xml import *
from fasthtml import *

import uuid
import requests
import replicate
from PIL import Image

# Replicate setup (for generating images)
replicate_api_token = open("replicate_key.txt", "r").read().strip()
client = replicate.Client(api_token=replicate_api_token)

# gens database for storing generated image details
tables = Database('gens.db').t
gens = tables.gens
if not gens in tables:
    gens.create(prompt=str, id=int, folder=str, pk='id')
Generation = gens.dataclass()


# Flexbox CSS (http://flexboxgrid.com/)
gridlink = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css")

# Our FastHTML app
app = FastHTML(hdrs=(picolink, gridlink))

# Main page
@app.get("/")
async def get(token:str):
    inp = Input(id="new-prompt", name="prompt", placeholder="Enter a prompt")
    add = Form(Group(inp, Button("Generate")), hx_post="/", target_id='gen-list', hx_swap="afterbegin")
    gen_containers = [generation_preview(g) for g in gens(limit=10)] # Start with last 10
    gen_list = Div(*gen_containers[::-1], id='gen-list', cls="row") # flexbox container: class = row
    return Title('Image Generation Demo'), Main(H1('Magic Image Generation'), add, gen_list, cls='container')

# Show the image (if available) and prompt for a generation
def generation_preview(g):
    grid_cls = "box col-xs-12 col-sm-6 col-md-4 col-lg-3"
    image_path = f"{g.folder}/{g.id}.png"
    if os.path.exists(image_path):
        return Div(Card(
                       Img(src=image_path, alt="Card image", cls="card-img-top"),
                       Div(P(B("Prompt: "), g.prompt, cls="card-text"),cls="card-body"),
                   ), id=f'gen-{g.id}', cls=grid_cls)
    return Div(f"Generating gen {g.id} with prompt {g.prompt}",
            id=f'gen-{g.id}', hx_get=f"/gens/{g.id}",
            hx_trigger="every 2s", hx_swap="outerHTML", cls=grid_cls)

# A pending preview keeps polling this route until we return the image preview
@app.get("/gens/{id}")
async def get(id:int):
    return generation_preview(gens.get(id))

# For images, CSS, etc.
@app.get("/{fname:path}.{ext:static}")
async def static(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

# Generation route
@app.post("/")
async def post(request:Request):
    form_data = await request.form()
    prompt = form_data['prompt']
    folder = f"gens/{str(uuid.uuid4())}"
    os.makedirs(folder, exist_ok=True)
    g = Generation(prompt=prompt, folder=folder)
    g = gens.insert(g)
    generate_and_save(g.prompt, g.id, g.folder)
    clear_input =  Input(id="new-prompt", name="prompt", placeholder="Enter a prompt", hx_swap_oob='true')
    return generation_preview(g), clear_input

# Generate an image and save it to the folder (in a separate thread)
@threaded
def generate_and_save(prompt, id, folder):
    output = client.run(
        "playgroundai/playground-v2.5-1024px-aesthetic:a45f82a1382bed5c7aeb861dac7c7d191b0fdf74d8d57c4a0e6ed7d4d0bf7d24",
        input={
            "width": 1024,"height": 1024,"prompt": prompt,"scheduler": "DPMSolver++",
            "num_outputs": 1,"guidance_scale": 3,"apply_watermark": True,
            "negative_prompt": "ugly, deformed, noisy, blurry, distorted",
            "prompt_strength": 0.8, "num_inference_steps": 25
        }
    )
    Image.open(requests.get(output[0], stream=True).raw).save(f"{folder}/{id}.png")
    return True

