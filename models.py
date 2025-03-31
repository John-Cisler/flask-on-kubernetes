import sqlite3

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('books.db')
        # Create tables needed by the application
        self.create_books_table()
        self.create_authors_table()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_books_table(self):
        """
        Create a table named 'Book' if it doesn't already exist.
        """
        query = """
        CREATE TABLE IF NOT EXISTS "Book" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            AuthorId INTEGER,
            YearPublished INT,
            IsRead BOOLEAN DEFAULT 0,
            CreatedOn DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY(AuthorId) REFERENCES Author(id)
        );
        """
        self.conn.execute(query)

    def create_authors_table(self):
        """
        Create a table named 'Author' if it doesn't already exist.
        """
        query = """
        CREATE TABLE IF NOT EXISTS "Author" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Country TEXT,
            CreatedOn DATE DEFAULT CURRENT_DATE
        );
        """
        self.conn.execute(query)


class BookModel:
    TABLENAME = "Book"

    def __init__(self):
        self.conn = sqlite3.connect('books.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def list_items(self):
        """
        List all books that are not marked deleted. 
        (Adjust if you want a "deleted" column.)
        """
        query = f"SELECT * FROM {self.TABLENAME}"
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()

        # Convert each row into a dict
        results = []
        for row in rows:
            results.append(dict(row))
        return results

    def get_by_id(self, book_id):
        query = f"SELECT * FROM {self.TABLENAME} WHERE id = {book_id}"
        cursor = self.conn.execute(query)
        row = cursor.fetchone()
        return dict(row) if row else {}

    def create(self, params):
        """
        params should contain keys like Title, AuthorId, YearPublished, IsRead, etc.
        """
        title = params.get('Title', '')
        author_id = params.get('AuthorId', None)
        year_published = params.get('YearPublished', 0)
        is_read = params.get('IsRead', 0)

        query = f"""
        INSERT INTO {self.TABLENAME} 
        (Title, AuthorId, YearPublished, IsRead)
        VALUES ("{title}", {author_id}, {year_published}, {is_read})
        """
        cursor = self.conn.execute(query)
        return self.get_by_id(cursor.lastrowid)

    def update(self, book_id, update_dict):
        """
        update_dict might look like:
        {
            'Title': 'My Updated Book Title',
            'IsRead': 1
        }
        """
        set_clause = []
        for col, val in update_dict.items():
            # For strings, wrap in double quotes
            if isinstance(val, str):
                set_clause.append(f'{col}="{val}"')
            else:
                set_clause.append(f'{col}={val}')

        set_clause = ", ".join(set_clause)

        query = f"""
        UPDATE {self.TABLENAME}
        SET {set_clause}
        WHERE id={book_id}
        """
        self.conn.execute(query)
        return self.get_by_id(book_id)

    def delete(self, book_id):
        """
        Deletes a book from the table. Alternatively, you could
        set a 'deleted' flag if you prefer a soft delete.
        """
        query = f"DELETE FROM {self.TABLENAME} WHERE id={book_id}"
        self.conn.execute(query)

        # Return remaining books or a message
        return {"message": f"Book with id {book_id} deleted.", "books": self.list_items()}