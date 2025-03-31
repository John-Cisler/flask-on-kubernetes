from models import BookModel

class BookService:
    def __init__(self):
        self.model = BookModel()

    def create(self, params):
        return self.model.create(params)

    def update(self, book_id, params):
        return self.model.update(book_id, params)

    def delete(self, book_id):
        return self.model.delete(book_id)

    def list(self):
        return self.model.list_items()

    def get_by_id(self, book_id):
        return self.model.get_by_id(book_id)