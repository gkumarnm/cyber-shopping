import requests
from app import app, Book

BASE = 'http://127.0.0.1:5000'

with app.app_context():
    b = Book.query.first()
    if not b:
        print('No books in DB')
        raise SystemExit(1)
    img = b.image_url
    print('Book:', b.title)
    print('Image URL in DB:', img)
    if img.startswith('/'): 
        url = BASE + img
    elif img.startswith('http'):
        url = img
    else:
        url = BASE + '/static/images/' + img

    print('Requesting:', url)
    try:
        r = requests.get(url, timeout=15)
        print('Status:', r.status_code)
        print('Content-Type:', r.headers.get('Content-Type'))
        print('Content-Length:', len(r.content))
    except Exception as e:
        print('Request failed:', e)
