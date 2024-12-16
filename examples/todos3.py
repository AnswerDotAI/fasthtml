# Run with: python basic_app.py
from fasthtml.common import *  # Import all the necessary components from FastHTML

# A function that renders each to-do item as an HTML list item.
def render(todo):
    show = AX(todo.title, f'/todos/{todo.id}', 'current-todo')  
    edit = AX('edit', f'/edit/{todo.id}', 'current-todo')  
    dt = ' (done)' if todo.done else ''
    return Li(show, dt, ' | ', edit, id=f'todo-{todo.id}') 

# Initialize the FastHTML app with database `todos.db`, a render function for each to-do item, and the todo properties (id, title, done)
# This function connects to the database and performs operations on the todos data.
app, rt, todos, Todo = fast_app('data/todos.db', render, id=int, title=str, done=bool, pk='id')

# Route to show the todo list (GET request)
@rt("/")
def get():
    inp = Input(id="new-title", name="title", placeholder="New Todo")
    # Form to submit the new to-do item, with AJAX functionality to add the new todo to the list
    add = Form(Group(inp, Button("Add")), hx_post="/", target_id='todo-list', hx_swap="beforeend")
    # The card includes the form to add new todos, a list of current todos, and a footer for showing the current todo
    card = Card(Ul(*todos(), id='todo-list'), header=add, footer=Div(id='current-todo'))
    return Titled('Todo list', card)

# Route to handle the POST request for adding a new to-do item
@rt("/")
def post(todo: Todo):
    # Insert the new todo into the database and return an updated input field
    return todos.insert(todo), Input(id="new-title", name="title", placeholder="New Todo", hx_swap_oob='true')

# Route to edit an existing to-do item (GET request to load the form)
@rt("/edit/{id}")
def get(id: int):
    # Generate the form to edit the todo item, including fields for title, done status, and a hidden id
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), CheckboxX(id="done", label='Done'),
        hx_put="/", target_id=f'todo-{id}', id="edit")
    # Pre-fill the form with the current todo data
    return fill_form(res, todos[id])

# Route to handle PUT request to save the updated todo item
@rt("/")
def put(todo: Todo):
    # Update the todo in the database and clear the current todo display
    return todos.update(todo), clear('current-todo')

# Route to display a single to-do item (GET request)
@rt("/todos/{id}")
def get(id: int):
    # Retrieve the specific todo from the database
    todo = todos[id]
    # Create a button for deleting the todo with AJAX behavior
    btn = Button('delete', hx_delete=f'/todos/{todo.id}', target_id=f'todo-{id}', hx_swap="outerHTML")
    # Return the todo item and the delete button
    return Div(Div(todo.title), btn)

# Route to handle DELETE request to delete a todo item
@rt("/todos/{id}")
def delete(id: int):
    # Delete the specific todo from the database
    todos.delete(id)
    # Clear the current todo display (could be for an active edit or current todo view)
    return clear('current-todo')

# Start the FastHTML server
serve()


