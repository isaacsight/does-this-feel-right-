import os
import sys
import requests
import argparse
from datetime import datetime

# Configuration
API_SECRET = os.environ.get('CONVERTKIT_API_SECRET')
BROADCAST_URL = "https://api.convertkit.com/v3/broadcasts"

def send_broadcast(subject, content_path, is_draft=True):
    """Creates and sends (or drafts) a broadcast from a markdown file."""
    
    if not os.path.exists(content_path):
        print(f"Error: File not found at {content_path}")
        return

    with open(content_path, 'r') as f:
        body_markdown = f.read()

    # Simple HTML wrapper (matching the blog's aesthetic)
    # Note: In a real production script, we might want a proper MD->HTML parser here.
    # For now, we'll assume the user writes basic HTML or we wrap their text.
    # Let's do a simple replacement of newlines to <p> tags for basic text files.
    
    # Very basic "Markdown" to HTML for the email body
    body_html = ""
    for line in body_markdown.split('\n'):
        if line.strip():
            if line.startswith('# '):
                body_html += f'<h1 style="font-size: 24px; font-weight: 700; margin-bottom: 20px;">{line[2:]}</h1>'
            elif line.startswith('## '):
                body_html += f'<h2 style="font-size: 20px; font-weight: 600; margin-bottom: 15px;">{line[3:]}</h2>'
            elif line.startswith('- '):
                 body_html += f'<li style="margin-bottom: 10px;">{line[2:]}</li>'
            else:
                body_html += f'<p style="font-size: 16px; margin-bottom: 20px;">{line}</p>'

    full_content = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333; line-height: 1.6;">
        {body_html}
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        <p style="font-size: 14px; color: #666;">
            Does This Feel Right? — A studio project by Isaac Hernandez.
        </p>
    </div>
    """
    
    data = {
        'api_secret': API_SECRET,
        'subject': subject,
        'content': full_content,
        'public': True,
    }
    
    if not is_draft:
        data['send_at'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        print("Sending immediately...")
    else:
        print("Creating draft...")

    response = requests.post(BROADCAST_URL, json=data)
    
    if not response.ok:
        print(f"Error: {response.status_code}")
        print(response.text)
        return

    result = response.json()
    print(f"Success! Broadcast ID: {result.get('broadcast', {}).get('id')}")
    if is_draft:
        print("Draft created. Log in to ConvertKit to send.")
    else:
        print("Broadcast scheduled for immediate sending.")

def main():
    if not API_SECRET:
        print("Error: CONVERTKIT_API_SECRET not set.")
        print("Run: export CONVERTKIT_API_SECRET=your_secret_key")
        return

    parser = argparse.ArgumentParser(description='Send a broadcast via ConvertKit')
    parser.add_argument('subject', help='Email Subject Line')
    parser.add_argument('file', help='Path to markdown/text file with email content')
    parser.add_argument('--send', action='store_true', help='Send immediately (default is Draft)')

    args = parser.parse_args()

    send_broadcast(args.subject, args.file, not args.send)

if __name__ == "__main__":
    main()
