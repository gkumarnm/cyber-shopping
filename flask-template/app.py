from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float)
    isbn = db.Column(db.String(32))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(1024))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    quantity = db.Column(db.Integer, default=1)
    # in a real app store price at time of order



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Ensure database tables exist (create on import within app context)
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Username and password are required', 'warning')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'warning')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('shop'))
        flash('Invalid username or password', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/shop')
@login_required
def shop():
    # search, filters, pagination
    q = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 6, type=int)

    query = Book.query
    if q:
        pattern = f"%{q}%"
        query = query.filter(or_(Book.title.ilike(pattern), Book.author.ilike(pattern)))

    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    if min_price is not None:
        query = query.filter(Book.price >= min_price)
    if max_price is not None:
        query = query.filter(Book.price <= max_price)

    pagination = query.order_by(Book.title).paginate(page=page, per_page=per_page, error_out=False)
    books = pagination.items
    return render_template('shop.html', books=books, pagination=pagination, q=q)


@app.route('/book/<int:book_id>')
@login_required
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


@app.route('/buy/<int:book_id>', methods=['POST'])
@login_required
def buy_book(book_id):
    book = Book.query.get_or_404(book_id)
    qty = int(request.form.get('quantity', 1))
    order = Order(user_id=current_user.id, book_id=book.id, quantity=qty)
    db.session.add(order)
    db.session.commit()
    flash(f'Order placed for {qty} x {book.title}', 'success')
    return redirect(url_for('shop'))


@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0.0
    for bid, qty in cart.items():
        book = Book.query.get(int(bid))
        if book:
            items.append({'book': book, 'quantity': qty})
            total += book.price * qty
    return render_template('cart.html', items=items, total=total)


@app.route('/cart/add/<int:book_id>', methods=['POST'])
@login_required
def add_to_cart(book_id):
    qty = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    cart[str(book_id)] = cart.get(str(book_id), 0) + qty
    session['cart'] = cart
    flash('Added to cart', 'success')
    return redirect(request.referrer or url_for('shop'))


@app.route('/cart/remove/<int:book_id>', methods=['POST'])
@login_required
def remove_from_cart(book_id):
    cart = session.get('cart', {})
    cart.pop(str(book_id), None)
    session['cart'] = cart
    flash('Removed from cart', 'info')
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('shop'))
    for bid, qty in cart.items():
        book = Book.query.get(int(bid))
        if book:
            order = Order(user_id=current_user.id, book_id=book.id, quantity=qty)
            db.session.add(order)
    db.session.commit()
    session['cart'] = {}
    flash('Checkout complete — thank you for your purchase', 'success')
    return redirect(url_for('shop'))


if __name__ == '__main__':
    # do not enable debug in production; control via FLASK_ENV
    debug_mode = os.environ.get('FLASK_ENV', '') == 'development'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=debug_mode)
