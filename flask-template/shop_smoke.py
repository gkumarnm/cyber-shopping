from app import app

def smoke():
    client = app.test_client()
    with app.app_context():
        # register
        client.post('/register', data={'username': 'smoke_user', 'password': 'pw'}, follow_redirects=True)
        # login
        client.post('/login', data={'username': 'smoke_user', 'password': 'pw'}, follow_redirects=True)
        # get shop
        r = client.get('/shop')
        print('GET /shop ->', r.status_code)
        text = r.get_data(as_text=True)
        found = 'Atomic Habits' in text
        print('Contains sample book title (Atomic Habits):', found)

if __name__ == '__main__':
    smoke()
