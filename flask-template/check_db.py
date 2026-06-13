import os
from app import app, Book

os.chdir(os.path.dirname(__file__))
print('cwd', os.getcwd())
print('app db exists', os.path.exists('app.db'))
print('db file size', os.path.getsize('app.db') if os.path.exists('app.db') else 'missing')
with app.app_context():
    books = Book.query.all()
    print('book count', len(books))
    for book in books:
        print(book.id, book.title, book.image_url)
