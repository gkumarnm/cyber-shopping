from app import app, db, User, Book
from seed_books import seed


def create_demo_user():
    username = 'demo_user'
    password = 'DemoPass123!'
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
        else:
            user.set_password(password)
        db.session.commit()

        # ensure books seeded
        seed()

        print('Demo user created/updated:')
        print('  username:', username)
        print('  password:', password)
        print('  user_id:', user.id)


if __name__ == '__main__':
    create_demo_user()
