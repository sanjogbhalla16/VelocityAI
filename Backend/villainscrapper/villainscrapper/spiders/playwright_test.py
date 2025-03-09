from playwright.sync_api import sync_playwright

def test_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to False to see browser
        page = browser.new_page()
        page.goto("https://villains.fandom.com/wiki/Category:Movie_Villains")
        page.wait_for_selector(".category-page__members-wrapper", timeout=10000)  # Wait for content

        html = page.content()
        with open("playwright_debug.html", "w", encoding="utf-8") as f:
            f.write(html)  # Save page content for inspection

        browser.close()

test_playwright()
