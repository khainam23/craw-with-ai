from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False helps to debug
    page = browser.new_page()
    page.goto("http://127.0.0.1:5500/test/require-login.html")
    
    # Fill in login form
    page.fill("#username", "admin")
    page.fill("#password", "123")
    
    # Click login
    page.click("#login-form button")

    # Wait until all comments are loaded
    # Since there are 3 comments, we can wait until 3 elements exist
    page.wait_for_function(
        """() => document.querySelectorAll('.comment').length === 3"""
    )
    
    # Collect all comments
    comments = page.query_selector_all(".comment")
    for comment in comments:
        user = comment.query_selector(".username").inner_text()
        text = comment.query_selector(".text").inner_text()
        print(f"{user}: {text}")
    
    browser.close()