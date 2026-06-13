import time
from app import app, db, User, Book, Order


def test_full_purchase_flow():
    username = f"test_user_{int(time.time())}"
    password = "TestPass123!"

    client = app.test_client()

    with app.app_context():
        # ensure at least one book exists (seed may have run)
        if Book.query.count() == 0:
            # create a minimal book
            b = Book(title='Sample Book', author='Author', price=10.0)
            db.session.add(b)
            db.session.commit()

        # Register
        rv = client.post('/register', data={'username': username, 'password': password}, follow_redirects=True)
        assert rv.status_code == 200
        assert b'Registration successful' in rv.data or b'Username already exists' in rv.data

        # Login
        rv = client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)
        assert rv.status_code == 200
        assert b'Logged in successfully' in rv.data

        # Shop listing
        rv = client.get('/shop')
        assert rv.status_code == 200
        assert b'Book Store' in rv.data

        # Pick a book and view details
        book = Book.query.first()
        rv = client.get(f'/book/{book.id}')
        assert rv.status_code == 200
        assert book.title.encode() in rv.data

        # Buy book
        rv = client.post(f'/buy/{book.id}', data={'quantity': 2}, follow_redirects=True)
        assert rv.status_code == 200
        assert b'Order placed' in rv.data

        # Verify order created
        user = User.query.filter_by(username=username).first()
        assert user is not None
        orders = Order.query.filter_by(user_id=user.id, book_id=book.id).all()
        assert len(orders) >= 1
