from sqlite3 import connect

conn = connect("library.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        year INTEGER DEFAULT NULL
    );
    """
)
conn.commit()
conn.close()

def insert_book(title, author, year=None):
    conn = connect("library.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO books (title, author, year) 
        VALUES (?, ?, ?);
        """,
        (title, author, year)
    )
    conn.commit()
    conn.close()

def get_all_books():
    conn = connect("library.db")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT * FROM books;"""
    )
    books = cursor.fetchall()
    conn.close()
    return books

def update_book(book_id, title, author, year=None):
    conn = connect("library.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE books
        SET title = ?, author = ?, year = ?
        WHERE id = ?
    """, (title, author, year, book_id))

    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = connect("library.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM books
        WHERE id = ?
    """, (book_id,))

    conn.commit()
    conn.close()

insert_book('Конец вечности', 'Айзек Азимов', 1955)
insert_book('Властелин колец', 'Джон Толкин', 1954)
insert_book('Автостопом по Галактике', 'Дуглас Адамс', 1979)

print(get_all_books())

update_book(2, 'Властелин колец', 'Д. Толкин', 1954)

delete_book(3)