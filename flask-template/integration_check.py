#!/usr/bin/env python3
from app import app
import sys

def check():
    client = app.test_client()
    passed = True

    def GET(path):
        r = client.get(path)
        print(f'GET {path}: {r.status_code}')
        return r

    def POST(path, data):
        r = client.post(path, data=data, follow_redirects=True)
        print(f'POST {path}: {r.status_code}')
        return r

    # Basic page loads
    r = GET('/')
    if r.status_code != 200:
        passed = False

    r = GET('/login')
    if r.status_code != 200:
        passed = False

    r = GET('/register')
    if r.status_code != 200:
        passed = False

    # Register a user
    username = 'integration_user'
    password = 'testpassword'
    r = POST('/register', {'username': username, 'password': password})
    if b'Registration successful' not in r.data and b'Username already exists' not in r.data:
        print('Register response missing expected flash')
        passed = False

    # Login
    r = POST('/login', {'username': username, 'password': password})
    if b'Logged in successfully' not in r.data and r.status_code != 200:
        print('Login may have failed or missing flash')
        # continue to check home page presence

    # Check home page contains username when logged in
    r = GET('/')
    if username.encode() in r.data:
        print('Username present on home page after login.')
    else:
        print('Username not present on home page after login.')
        passed = False

    return passed


if __name__ == '__main__':
    ok = check()
    if ok:
        print('\nINTEGRATION CHECK PASSED')
        sys.exit(0)
    else:
        print('\nINTEGRATION CHECK FAILED')
        sys.exit(2)
