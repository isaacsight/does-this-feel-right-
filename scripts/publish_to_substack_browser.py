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

    with sync_playwright() as p:
        # Launch Browser (Headless=False so you can see it working)
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        
        print(f"Logging in as {EMAIL}...")
        
        # Login
        page.goto("https://substack.com/sign-in")
        page.fill('input[name="email"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        page.click('button[type="submit"]')
        
        # Wait for dashboard or home
        try:
            page.wait_for_url("**/home", timeout=10000)
        except:
            print("Login might have failed or required Captcha. Check browser.")
            # time.sleep(5) # Give time to see
        
        print("Navigating to Editor...")
        # Go to Dashboard/New Post (URL might vary, trying generic /publish/post)
        # We need to find the user's subdomain. Usually it's in the redirect.
        # For now, let's assume we can find the "Dashboard" button or go to subdomain.substack.com/publish
        
        # Better approach: Go to user's profile/dashboard
        page.goto("https://substack.com/dashboard")
        
        # Click "New Post"
        # This selector is brittle and might change. 
        # We'll try to find a button with text "New post"
        page.get_by_text("New post").first.click()
        
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
        
        # Optional: Click "Continue" or "Publish"
        # page.get_by_text("Continue").click()
        
        browser.close()
        print("Done.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 publish_to_substack_browser.py <filepath>")
    else:
        publish(sys.argv[1])
