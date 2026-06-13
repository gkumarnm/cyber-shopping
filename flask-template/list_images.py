from app import app, Book

with app.app_context():
    books = Book.query.all()
    if not books:
        print('No books found')
    for b in books:
        print(f'{b.id}: {b.title} -> {b.image_url}')
