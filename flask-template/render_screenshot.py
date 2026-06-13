from playwright.sync_api import sync_playwright
import time

BASE = 'http://127.0.0.1:5000'
USERNAME = 'demo_user'
PASSWORD = 'DemoPass123!'

def run():
    print('Playwright: start')
    with sync_playwright() as p:
        print('Playwright: launching browser')
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()

        print('Playwright: navigating to login')
        page.goto(f"{BASE}/login")
        print('Playwright: filling credentials')
        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.click('button[type="submit"]')

        print('Playwright: waiting for shop URL')
        # wait for navigation to shop
        try:
            page.wait_for_url("**/shop", timeout=15000)
            print('Playwright: detected shop URL')
        except Exception:
            print('Playwright: shop URL not detected, navigating to /shop')
            # maybe redirect to home then shop link; navigate explicitly
            page.goto(f"{BASE}/shop")

        print('Playwright: waiting for book selectors')
        # wait for at least one book image or book card to be visible
        try:
            page.wait_for_selector('.book-cover img', timeout=20000)
            print('Playwright: found .book-cover img')
        except Exception:
            print('Playwright: .book-cover img not found, trying .book-card')
            try:
                page.wait_for_selector('.book-card', timeout=10000)
                print('Playwright: found .book-card')
            except Exception:
                print('Playwright: .book-card not found, trying any img')
                # fallback: wait for any image
                try:
                    page.wait_for_selector('img', timeout=7000)
                    print('Playwright: found an img element')
                except Exception as e:
                    print('Playwright: no images found, capturing diagnostic')
                    # capture diagnostic screenshot and HTML
                    diag = 'shop_diag.png'
                    page.screenshot(path=diag, full_page=True)
                    print('Diagnostic screenshot saved to', diag)
                    html = page.content()[:2000]
                    print('Page HTML snippet:', html)
                    raise

        # give images time to load
        time.sleep(1)

        out = 'shop_screenshot.png'
        page.screenshot(path=out, full_page=True)
        print('Saved screenshot to', out)

        context.close()
        browser.close()

if __name__ == '__main__':
    run()
