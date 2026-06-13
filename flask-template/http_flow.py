import requests
from urllib.parse import urljoin

BASE = 'http://127.0.0.1:5000/'

def run():
    s = requests.Session()
    # create unique user
    import time
    username = f'http_user_{int(time.time())}'
    password = 'HttpPass123!'

    # register
    r = s.post(urljoin(BASE, 'register'), data={'username': username, 'password': password}, allow_redirects=True)
    print('POST /register ->', r.status_code)

    # login
    r = s.post(urljoin(BASE, 'login'), data={'username': username, 'password': password}, allow_redirects=True)
    print('POST /login ->', r.status_code)
    print('Final URL after login:', r.url)
    print('Contains Shop heading?', 'Book Store' in r.text)

    # Visit shop explicitly
    r2 = s.get(urljoin(BASE, 'shop'))
    print('GET /shop ->', r2.status_code)
    if 'Book Store' in r2.text:
        print('Shop page loaded successfully')
    else:
        print('Shop page did not show expected content; sample content snippet:')
        print(r2.text[:500])

if __name__ == '__main__':
    run()
