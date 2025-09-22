from random import random
from fasthtml.common import *
app,rt = fast_app( hdrs=[Script(src='example.js')])

@rt
def rnd(): return P(random())

@rt
def index(): return Titled( 'Hello', Div(P('click'), hx_post=rnd))

serve()

