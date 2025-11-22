import os
import json
import glob
from supabase import create_client, Client
import requests

# Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')  # Need service key for admin access
RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
FROM_EMAIL = 'Does This Feel Right <noreply@doesthisfeelright.com>'
SITE_URL = 'https://www.doesthisfeelright.com'

def parse_frontmatter(file_content):
    """Extract frontmatter from content files"""
    if not file_content.startswith('---'):
        return {}, file_content
    
    parts = file_content.split('---', 2)
    if len(parts) < 3:
        return {}, file_content
    
    frontmatter_text = parts[1].strip()
    body = parts[2].strip()
    
    metadata = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
    
    return metadata, body

def get_all_posts():
    """Get all posts from content directory"""
    posts = []
    for filepath in glob.glob('content/*.html'):
        filename = os.path.basename(filepath)
        if filename == 'about.html':
            continue
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        metadata, _ = parse_frontmatter(content)
        slug = filename.replace('.html', '')
        
        posts.append({
            'slug': slug,
            'title': metadata.get('title', 'Untitled'),
            'excerpt': metadata.get('excerpt', ''),
            'category': metadata.get('category', 'General')
        })
    
    return posts

def get_emailed_posts(supabase: Client):
    """Get posts that have already been emailed"""
    response = supabase.table('email_notifications').select('post_slug').execute()
    return set(row['post_slug'] for row in response.data)

def get_all_user_emails(supabase: Client):
    """Get all user emails from Supabase Auth"""
    # Note: This requires Supabase service key (admin access)
    response = supabase.auth.admin.list_users()
    return [user.email for user in response if user.email]

def send_email(to_email, post):
    """Send email using Resend API"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Georgia, serif; line-height: 1.6; color: #1a1a1a; max-width: 600px; margin: 0 auto; padding: 20px; }}
            h1 {{ font-family: -apple-system, sans-serif; font-size: 24px; margin-bottom: 10px; }}
            .category {{ color: #666; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }}
            .excerpt {{ color: #444; margin: 20px 0; }}
            .cta {{ display: inline-block; background: #1a1a1a; color: white; padding: 12px 24px; text-decoration: none; margin-top: 20px; }}
            .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; }}
        </style>
    </head>
    <body>
        <div class="category">{post['category']}</div>
        <h1>{post['title']}</h1>
        <div class="excerpt">{post['excerpt']}</div>
        <a href="{SITE_URL}/posts/{post['slug']}.html" class="cta">Read Now</a>
        <div class="footer">
            <p>You're receiving this because you have an account at Does This Feel Right?</p>
            <p><a href="{SITE_URL}/library.html">Manage your library</a></p>
        </div>
    </body>
    </html>
    """
    
    response = requests.post(
        'https://api.resend.com/emails',
        headers={
            'Authorization': f'Bearer {RESEND_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'from': FROM_EMAIL,
            'to': to_email,
            'subject': f'New: {post["title"]}',
            'html': html_content
        }
    )
    
    return response.status_code == 200

def mark_post_as_emailed(supabase: Client, post_slug, recipient_count):
    """Mark post as having been emailed"""
    supabase.table('email_notifications').insert({
        'post_slug': post_slug,
        'recipient_count': recipient_count
    }).execute()

def main():
    # Initialize Supabase
   supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Get all posts and find new ones
    all_posts = get_all_posts()
    emailed_posts = get_emailed_posts(supabase)
    new_posts = [p for p in all_posts if p['slug'] not in emailed_posts]
    
    if not new_posts:
        print("No new posts to email")
        return
    
    # Get all user emails
    user_emails = get_all_user_emails(supabase)
    
    if not user_emails:
        print("No users to email")
        return
    
    # Send emails for each new post
    for post in new_posts:
        print(f"Sending emails for: {post['title']}")
        success_count = 0
        
        for email in user_emails:
            if send_email(email, post):
                success_count += 1
        
        # Mark as emailed
        mark_post_as_emailed(supabase, post['slug'], success_count)
        print(f"Sent to {success_count}/{len(user_emails)} users")

if __name__ == '__main__':
    main()
