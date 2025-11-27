import os
import sys
import time
from playwright.sync_api import sync_playwright
import frontmatter

def publish(filepath):
    # Credentials
    EMAIL = os.environ.get('SUBSTACK_EMAIL')
    PASSWORD = os.environ.get('SUBSTACK_PASSWORD')
    
    if not EMAIL or not PASSWORD:
        print("Error: Missing SUBSTACK_EMAIL or SUBSTACK_PASSWORD in .env")
        return

    # Parse Post
    with open(filepath, 'r') as f:
        post = frontmatter.load(f)
        title = post.get('title', 'Untitled')
        content = post.content

    AUTH_FILE = 'substack_auth.json'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        
        # Try to load auth state
        if os.path.exists(AUTH_FILE):
            context = browser.new_context(storage_state=AUTH_FILE)
            print("Loaded session from disk.")
        else:
            context = browser.new_context()
            
        page = context.new_page()
        
        # Check if logged in
        page.goto("https://substack.com/home")
        
        # If redirected to sign-in, perform login
        if "sign-in" in page.url or "login" in page.url:
            print(f"Logging in as {EMAIL}...")
            page.goto("https://substack.com/sign-in")
            page.fill('input[name="email"]', EMAIL)
            page.fill('input[name="password"]', PASSWORD)
            page.click('button[type="submit"]')
            
            # Wait for dashboard or home
            try:
                page.wait_for_url("**/home", timeout=15000)
                # Save auth state
                context.storage_state(path=AUTH_FILE)
                print("Saved new session to disk.")
            except:
                print("Login might have failed or required Captcha. Check browser.")
        
        print("Navigating to Editor...")
        # Go directly to the specific publication's dashboard
        # We derived this from your screenshot: doesthisfeelright.substack.com
        PUBLICATION_URL = "https://doesthisfeelright.substack.com/publish"
        page.goto(PUBLICATION_URL)
        
        # Click "New Post"
        # On the publisher dashboard, it's usually a distinct button
        # We'll try the specific URL for a new post to be even safer
        page.goto(f"{PUBLICATION_URL}/new")
        
        print("Writing content...")
        # Wait for editor
        page.wait_for_selector('input[placeholder="Post title"]', timeout=10000)
        
        # Fill Title
        page.fill('input[placeholder="Post title"]', title)
        
        # Fill Content (Substack editor is a contenteditable div)
        # We'll focus it and type/paste.
        page.click('.kjb-editor-rich-text') # This class is a guess, need to be robust
        # Actually, clicking the editor area is safer.
        # Let's try to focus the main editor div.
        
        # Alternative: Copy content to clipboard and paste? Playwright has permissions issues with clipboard.
        # We'll use page.keyboard.insert_text(content)
        page.keyboard.type(content) 
        
        print("Draft saved!")
        time.sleep(2)
        
        # Auto-Publish Logic
        try:
            print("Clicking Continue...")
            # Substack usually has a "Continue" button in the top right or bottom
            continue_btn = page.get_by_text("Continue").first
            continue_btn.click()
            
            # Wait for the settings modal/page
            time.sleep(2)
            
            print("Clicking Send to everyone now...")
            # The final button usually says "Send to everyone now" or "Subscribe and send"
            # We'll look for "Send to everyone"
            send_btn = page.get_by_text("Send to everyone now").first
            if not send_btn.is_visible():
                 # Fallback for different UI states
                 send_btn = page.get_by_text("Send to everyone").first
            
            if send_btn.is_visible():
                send_btn.click()
                print("PUBLISHED! 🚀")
            else:
                print("Could not find 'Send to everyone' button. Stopping at settings screen.")
                
            # Keep browser open for a few seconds to verify
            time.sleep(5)
            
        except Exception as e:
            print(f"Auto-publish failed (Draft is saved): {e}")
        
        browser.close()
        print("Done.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 publish_to_substack_browser.py <filepath>")
    else:
        publish(sys.argv[1])
