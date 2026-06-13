from app import db, Book, app

BOOKS = [
    {
        'title': 'Atomic Habits',
        'author': 'James Clear',
        'publisher': 'Avery',
        'price': 16.20,
        'rating': 4.8,
        'isbn': '9780735211292',
        'image_url': 'https://covers.openlibrary.org/b/isbn/9780735211292-L.jpg',
        'description': 'An easy & proven way to build good habits and break bad ones.'
    },
    {
        'title': 'The 7 Habits of Highly Effective People',
        'author': 'Stephen R. Covey',
        'publisher': 'Free Press',
        'price': 14.99,
        'rating': 4.7,
        'isbn': '9780743269513',
        'image_url': 'https://covers.openlibrary.org/b/isbn/9780743269513-L.jpg',
        'description': 'Powerful lessons in personal change.'
    },
    {
        'title': 'How to Win Friends and Influence People',
        'author': 'Dale Carnegie',
        'publisher': 'Pocket Books',
        'price': 9.99,
        'rating': 4.6,
        'isbn': '9780671027032',
        'image_url': 'https://covers.openlibrary.org/b/isbn/9780671027032-L.jpg',
        'description': 'A timeless guide to interpersonal skills.'
    },
    {
        'title': 'The Power of Habit',
        'author': 'Charles Duhigg',
        'publisher': 'Random House',
        'price': 12.50,
        'rating': 4.5,
        'isbn': '9780812981605',
        'image_url': 'https://covers.openlibrary.org/b/isbn/9780812981605-L.jpg',
        'description': 'Why we do what we do in life and business.'
    },
    {
        'title': 'Think and Grow Rich',
        'author': 'Napoleon Hill',
        'publisher': 'The Ralston Society',
        'price': 7.95,
        'rating': 4.3,
        'isbn': '9781937879506',
        'image_url': 'https://covers.openlibrary.org/b/isbn/9781937879506-L.jpg',
        'description': 'Classic book on the psychology of success.'
    }
]


def seed():
    for b in BOOKS:
        exists = Book.query.filter_by(title=b['title']).first()
        if not exists:
            book = Book(
                title=b['title'],
                author=b['author'],
                publisher=b.get('publisher'),
                price=b.get('price', 0.0),
                rating=b.get('rating'),
                isbn=b.get('isbn'),
                description=b.get('description'),
                image_url=b.get('image_url')
            )
            db.session.add(book)
        else:
            # update missing fields on existing records
            updated = False
            if not exists.author:
                exists.author = b['author']; updated = True
            if not exists.publisher and b.get('publisher'):
                exists.publisher = b.get('publisher'); updated = True
            if not exists.price and b.get('price'):
                exists.price = b.get('price'); updated = True
            if not exists.rating and b.get('rating'):
                exists.rating = b.get('rating'); updated = True
            if not exists.isbn and b.get('isbn'):
                exists.isbn = b.get('isbn'); updated = True
            if not exists.description and b.get('description'):
                exists.description = b.get('description'); updated = True
            if not exists.image_url and b.get('image_url'):
                exists.image_url = b.get('image_url'); updated = True
            if updated:
                db.session.add(exists)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        seed()
        print('Seeding complete')
