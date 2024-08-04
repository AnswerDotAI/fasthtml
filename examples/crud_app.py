###
# Walkthrough of a FastHTML CRUD application for managing books
###


# Importing from `fasthtml.common` brings together key parts of fastcore, starlette, fastlite, and fasthtml.
from fasthtml.common import *
from dataclasses import dataclass

# Set up the database using FastLite, which supports the MiniDataAPI spec
db = database("books.db")
# The `t` attribute is the table collection. We're creating a 'books' table.
books = db.t.books

# Create the 'books' table if it doesn't exist
if books not in db.t:
    # You can pass a dict to the `create` method to define the table schema
    books.create(id=int, title=str, author=str, year=int, pk="id")

# Create a dataclass for the Book model
# This allows for easier type hinting and data manipulation
Book = books.dataclass()

# Create the FastHTML app
# FastHTML is a subclass of Starlette, so you can use any parameters that Starlette accepts
app = FastHTML()
# We add `rt` as a shortcut for `app.route`, which we'll use to decorate our route handlers
rt = app.route


# Helper function to create an `Li` element for a book
def book_to_li(book):
    return Li(
        f"{book.title} by {book.author} ({book.year})",
        # Use HTMX attributes for dynamic content loading
        A("View", hx_get=f"/books/{book.id}", target_id="book-details"),
        " | ",
        A("Edit", hx_get=f"/books/{book.id}/edit", target_id="book-details"),
        " | ",
        A(
            "Delete",
            hx_delete=f"/books/{book.id}",
            target_id=f"book-{book.id}",
            hx_swap="outerHTML",
        ),
        id=f"book-{book.id}",
    )


def clear_input_fields():
    """Generate empty input fields to clear the form after submission."""
    return (
        Input(id="title", value="", hx_swap_oob="true"),
        Input(id="author", value="", hx_swap_oob="true"),
        Input(id="year", value="", hx_swap_oob="true"),
    )


# Main page handler
@rt("/")
def get():
    title = "Book Management"
    # Create an unordered list of books, where each book is represented by an `Li` element
    book_list = Ul(*[book_to_li(book) for book in books()], id="book-list")
    # Create a form for adding new books
    add_form = Form(
        Input(id="title", placeholder="Title"),
        Input(id="author", placeholder="Author"),
        Input(id="year", placeholder="Year", type="number"),
        Button("Add Book"),
        # Use HTMX to handle form submission without a page reload
        hx_post="/books",
        target_id="book-list",
        hx_swap="beforeend",
    )
    # Return a tuple of FT objects, which FastHTML will compose into an HTML response
    return Title(title), Container(
        H1(title), Card(book_list, header=add_form), Div(id="book-details")
    )


# Handler for creating a new book
@rt("/books")
def post(book: Book):
    # Insert the new book into the database
    # The `insert` method is part of the MiniDataAPI spec
    new_book = books.insert(book)
    # Return the HTML for the new book, which will be added to the list
    return (
        book_to_li(new_book),
        *clear_input_fields(),
        Div(id="book-details", hx_swap_oob="true"),  # Clear details view
    )


# Handler for viewing a book's details
@rt("/books/{id}")
def get(id: int):
    # Query the book by its ID
    # Indexing into a MiniDataAPI table queries by primary key
    book = books[id]
    return Div(
        H2(book.title),
        P(f"Author: {book.author}"),
        P(f"Year: {book.year}"),
        A("Close", hx_get="/close-details", target_id="book-details"),
    )


# Handler for editing a book
@rt("/books/{id}/edit")
def get(id: int):
    book = books[id]
    # Create a form pre-filled with the book's current data
    return Form(
        Input(id="title", value=book.title),
        Input(id="author", value=book.author),
        Input(id="year", value=book.year, type="number"),
        Hidden(id="id", value=book.id),
        Button("Update"),
        # Use HTMX to handle form submission
        hx_put=f"/books/{id}",
        target_id=f"book-{id}",
    )


# Handler for updating a book
@rt("/books/{id}")
def put(book: Book):
    # Update the book in the database
    # The `update` method is part of the MiniDataAPI spec
    updated_book = books.update(book)
    # Return the updated book HTML, which will replace the old version in the list
    return (
        book_to_li(updated_book),
        *clear_input_fields(),
        Div(id="book-details", hx_swap_oob="true"),  # Clear details view
    )


# Handler for deleting a book
@rt("/books/{id}")
def delete(id: int):
    # Delete the book from the database
    # The `delete` method is part of the MiniDataAPI spec
    books.delete(id)
    return (
        "",  # Remove the book from the list
        Div(id="book-details", hx_swap_oob="true"),  # Clear details view after delete
    )


# Handler for closing the book details view
@rt("/close-details")
def get():
    # Return an empty div to clear the details
    return Div(id="book-details")


# Start the FastHTML application
serve()
