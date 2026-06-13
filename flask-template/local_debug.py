import urllib.request
from urllib.error import URLError, HTTPError

urls = [
    'http://127.0.0.1:5000/shop',
    'http://127.0.0.1:5000/static/images/9780735211292.jpg',
    'http://127.0.0.1:5000/static/images/9780743269513.jpg',
]

for url in urls:
    print('FETCH', url)
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = resp.read()
            print(' status', resp.status)
            ct = resp.headers.get('Content-Type')
            print(' content-type', ct)
            if url.endswith('/shop'):
                text = data.decode('utf-8', errors='replace')
                print(' contains book-card', 'class="book-card"' in text)
                print(' img count', text.count('<img '))
                # print image src snippets
                for marker in ['src="/static/images/', 'src="http', 'src="/static']: 
                    pos = text.find(marker)
                    if pos != -1:
                        print(' first src snippet', text[pos:pos+120])
                        break
            else:
                print(' length', len(data))
    except HTTPError as e:
        print(' HTTPError', e.code, e.reason)
    except URLError as e:
        print(' URLError', e.reason)
    except Exception as e:
        print(' ERROR', e)
