import os
from app import app
from run_flow import create_demo_user

os.chdir(os.path.dirname(__file__))
create_demo_user()
with app.test_client() as client:
    resp = client.get('/shop')
    text = resp.get_data(as_text=True)
    print('status', resp.status_code)
    print('has book-card', 'class="book-card"' in text)
    print('img count', text.count('<img '))
    start = text.find('<div class="book-list"')
    end = text.find('</div>', start)
    print('snippet', text[start:end+6])
