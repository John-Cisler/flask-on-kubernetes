from flask import Flask, request, jsonify
from service import BookService
from models import Schema

app = Flask(__name__)

# Allow CORS (Cross-Origin Resource Sharing) - if needed
@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response


# Basic route
@app.route("/")
def hello():
    return "Welcome to the Book Manager API!"


# 1) List all books
@app.route("/books", methods=["GET"])
def list_books():
    return jsonify(BookService().list())


# 2) Create a new book
@app.route("/books", methods=["POST"])
def create_book():
    return jsonify(BookService().create(request.get_json()))


# 3) Get details for a particular book
@app.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    return jsonify(BookService().get_by_id(book_id))


# 4) Update an existing book
@app.route("/books/<book_id>", methods=["PUT"])
def update_book(book_id):
    return jsonify(BookService().update(book_id, request.get_json()))


# 5) Delete a book
@app.route("/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    return jsonify(BookService().delete(book_id))


if __name__ == "__main__":
    # Initialize our database schema before running
    Schema()
    app.run(debug=True, host='0.0.0.0', port=5001)