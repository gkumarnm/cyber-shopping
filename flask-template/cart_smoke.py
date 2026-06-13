from app import app, db, User, Book, Order

def smoke():
    client = app.test_client()
    with app.app_context():
        username = 'cart_user'
        password = 'CartPass123!'
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

        # login
        client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)

        # add first book to cart
        book = Book.query.first()
        rv = client.post(f'/cart/add/{book.id}', data={'quantity': 2}, follow_redirects=True)
        assert b'Added to cart' in rv.data

        # view cart
        rv = client.get('/cart')
        assert rv.status_code == 200
        assert book.title.encode() in rv.data

        # checkout
        rv = client.post('/checkout', follow_redirects=True)
        assert b'Checkout complete' in rv.data

        print('Cart smoke test passed')

if __name__ == '__main__':
    smoke()
