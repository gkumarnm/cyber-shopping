import os
from app import app
from run_flow import create_demo_user

os.chdir(os.path.dirname(__file__))
create_demo_user()
with app.test_client() as client:
    login_page = client.get('/login')
    print('login page status', login_page.status_code)
    r = client.post('/login', data={'username': 'demo_user', 'password': 'DemoPass123!'}, follow_redirects=True)
    print('login redirect status', r.status_code)
    print('login final path includes /shop', '/shop' in r.request.path)
    text = r.get_data(as_text=True)
    print('contains Book Store', 'Book Store' in text)
    print('book-card count', text.count('class="book-card"'))
    print('img count', text.count('<img '))
    start = text.find('<div class="book-list"')
    end = text.find('</div>', start)
    print('body-content snippet:', text[start:end+6])
    print('templates folder', app.template_folder)
    print('db uri', app.config['SQLALCHEMY_DATABASE_URI'])
