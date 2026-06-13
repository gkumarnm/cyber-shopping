import os
import requests
from app import app, Book

OUT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images')
os.makedirs(OUT_DIR, exist_ok=True)

def slugify(name):
    return ''.join(c for c in name.replace(' ', '_') if c.isalnum() or c == '_')

with app.app_context():
    books = Book.query.all()
    for b in books:
        src = b.image_url
        if not src:
            continue
        if src.startswith('/static/'):
            continue
        # download remote image
        try:
            resp = requests.get(src, timeout=15)
            if resp.status_code == 200:
                ext = 'jpg'
                if 'png' in resp.headers.get('Content-Type',''):
                    ext = 'png'
                name = b.isbn or slugify(b.title) or str(b.id)
                filename = f"{name}.{ext}"
                path = os.path.join(OUT_DIR, filename)
                with open(path, 'wb') as fh:
                    fh.write(resp.content)
                # update book image_url to local static path
                b.image_url = f"/static/images/{filename}"
                print('Saved', path)
        except Exception as e:
            print('Failed:', b.title, e)
    Book.query.session.commit()
    print('Done')
