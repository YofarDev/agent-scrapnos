from playwright.sync_api import sync_playwright


def run_playwright(url:str)->str:
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=False opens a visible browser
        context = browser.new_context(user_agent=ua)
        page = context.new_page() 
        page.goto(url)
        # Wait for the page to load
        page.wait_for_timeout(2123) 
        content = page.locator("body").inner_text()
        browser.close()
        return content
        
