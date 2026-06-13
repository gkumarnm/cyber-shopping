import requests

base = 'http://127.0.0.1:5000'
with requests.Session() as s:
    r = s.post(base + '/login', data={'username': 'demo_user', 'password': 'DemoPass123!'}, allow_redirects=True)
    print('login status', r.status_code)
    print('history', [h.status_code for h in r.history])
    print('final url', r.url)
    r2 = s.get(base + '/shop')
    print('shop status', r2.status_code)
    print('redirect history', [h.status_code for h in r2.history])
    text = r2.text
    print('len', len(text))
    print('book-store', 'Book Store' in text)
    print('book-card count', text.count('class="book-card"'))
    print('img count', text.count('<img '))
    print('has for loop markup', '{% for book in books %}' in text)
    print('first 800 chars:')
    print(text[:800])
    with open('live_shop_dump.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('dump saved')
