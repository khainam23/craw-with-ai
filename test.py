from playwright.sync_api import sync_playwright

url = "https://quotes.toscrape.com/js/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # headless=True: không mở UI
    page = browser.new_page()
    page.goto(url)
    page.wait_for_selector(".quote")  # đợi JS render xong

    quotes = page.locator(".quote span.text").all_inner_texts()
    print("Quotes (Playwright):", quotes)

    browser.close()
