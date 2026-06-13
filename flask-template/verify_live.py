import requests

base = 'http://127.0.0.1:5000'

with requests.Session() as s:
    r = s.get(f'{base}/login')
    print('login page status', r.status_code)
    if '<form' in r.text:
        print('login form found')
    payload = {'username': 'demo_user', 'password': 'DemoPass123!'}
    r = s.post(f'{base}/login', data=payload, allow_redirects=True)
    print('post login status', r.status_code)
    print('final url', r.url)
    print('login response contains shop?', '/shop' in r.text[:500])
    r2 = s.get(f'{base}/shop')
    print('shop status', r2.status_code)
    print('shop title snippet', r2.text[:400])
    print('book-card count', r2.text.count('class="book-card"'))
    print('img count', r2.text.count('<img '))
    pos = r2.text.find('src="/static/images/')
    print('src snippet', r2.text[pos:pos+120] if pos != -1 else 'none')
