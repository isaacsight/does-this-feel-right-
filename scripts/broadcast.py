import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Configuration
API_SECRET = os.environ.get('CONVERTKIT_API_SECRET')
FEED_PATH = 'docs/feed.xml'
BROADCAST_URL = "https://api.convertkit.com/v3/broadcasts"

def get_latest_post():
    """Parses the RSS feed and returns the latest post details."""
    if not os.path.exists(FEED_PATH):
        raise FileNotFoundError(f"Feed file not found at {FEED_PATH}")
        
    tree = ET.parse(FEED_PATH)
    root = tree.getroot()
    # RSS items are usually order by date, so the first one is the latest
    item = root.find('./channel/item')
    
    if item is None:
        return None
        
    return {
        'title': item.find('title').text,
        'link': item.find('link').text,
        'description': item.find('description').text
    }

def broadcast_exists(title):
    """Checks if a broadcast with the same title already exists."""
    params = {'api_secret': API_SECRET}
    response = requests.get(BROADCAST_URL, params=params)
    response.raise_for_status()
    
    broadcasts = response.json().get('broadcasts', [])
    for b in broadcasts:
        if b['subject'] == title:
            return True
    return False

def create_broadcast(post):
    """Creates and sends a broadcast for the new post."""
    # Simple HTML template matching the blog's aesthetic
    content = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333; line-height: 1.6;">
        <h1 style="font-size: 24px; font-weight: 700; margin-bottom: 20px;">{post['title']}</h1>
        <p style="font-size: 16px; margin-bottom: 20px;">{post['description']}</p>
        <p style="margin-bottom: 30px;">
            <a href="{post['link']}" style="background-color: #000; color: #fff; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: 500; font-size: 16px; display: inline-block;">Read the full essay</a>
        </p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p style="font-size: 14px; color: #666;">
            Does This Feel Right? — A studio project by Isaac Hernandez.
        </p>
    </div>
    """
    
    data = {
        'api_secret': API_SECRET,
        'subject': post['title'],
        'content': content,
        'public': True,
        # Setting send_at to now to trigger immediate sending (or close to it)
        # If this causes issues, we can remove it to create a draft instead.
        # 'send_at': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ') 
    }
    
    # Note: To be safe, let's create it as a DRAFT first. 
    # The user can then just click "Send" in ConvertKit.
    # If they want it fully automated, we uncomment 'send_at'.
    # Given the user said "send the emails for me", I will try to send it.
    # However, without 'send_at', it defaults to draft.
    # Let's use 'send_at' for automation.
    data['send_at'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    response = requests.post(BROADCAST_URL, json=data)
    if not response.ok:
        print(f"Error: {response.status_code}")
        print(response.text)
    response.raise_for_status()
    return response.json()

def main():
    if not API_SECRET:
        print("Error: CONVERTKIT_API_SECRET not found.")
        exit(1)

    print("Checking for new posts...")
    post = get_latest_post()
    
    if not post:
        print("No posts found in feed.")
        return

    print(f"Latest post: {post['title']}")
    
    if broadcast_exists(post['title']):
        print("Broadcast already exists for this post. Skipping.")
    else:
        print("New post detected. Creating broadcast...")
        result = create_broadcast(post)
        print(f"Broadcast created successfully! ID: {result.get('broadcast', {}).get('id')}")

if __name__ == "__main__":
    main()
