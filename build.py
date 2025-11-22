import os
import shutil
import datetime

# Configuration
CONTENT_DIR = 'content'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'docs'
STATIC_DIR = 'static'
BASE_URL = 'https://www.doesthisfeelright.com'
DEFAULT_IMAGE = 'https://www.doesthisfeelright.com/static/images/og-default.jpg' # Placeholder

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def parse_frontmatter(content):
    """
    Parses simple frontmatter bounded by ---
    Returns metadata dict and body content.
    """
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content # No frontmatter
    
    frontmatter = parts[1].strip()
    body = parts[2].strip()
    
    metadata = {}
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
            
    return metadata, body

def build():
    # 1. Prepare Output Directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    
    # 2. Copy Static Assets
    shutil.copytree(STATIC_DIR, os.path.join(OUTPUT_DIR, 'static'))
    # Also copy style.css to root css/ folder for compatibility if needed, 
    # but our templates use {{ root }}static/css so we should be good.
    # Wait, templates use {{ root }}css/style.css. 
    # Let's match the template expectation: static/css -> docs/css
    # Actually, let's just copy static/* to docs/*
    # So docs/css/style.css exists.
    
    # Re-copying to match structure
    # static/css -> docs/css
    # static/js -> docs/js
    for item in os.listdir(STATIC_DIR):
        s = os.path.join(STATIC_DIR, item)
        d = os.path.join(OUTPUT_DIR, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    # 3. Load Templates
    base_template = read_file(os.path.join(TEMPLATE_DIR, 'base.html'))
    post_template = read_file(os.path.join(TEMPLATE_DIR, 'post.html'))
    index_template = read_file(os.path.join(TEMPLATE_DIR, 'index.html'))

    # 4. Process Posts
    posts = []
    for filename in os.listdir(CONTENT_DIR):
        if not filename.endswith('.html') and not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(CONTENT_DIR, filename)
        raw_content = read_file(filepath)
        metadata, body = parse_frontmatter(raw_content)
        
        # Slug is filename without extension
        slug = os.path.splitext(filename)[0]
        metadata['slug'] = slug
        
        # Render Post
        # 1. Inject body into post_template
        post_html = post_template.replace('{{ title }}', metadata.get('title', 'Untitled'))
        post_html = post_html.replace('{{ category }}', metadata.get('category', 'General'))
        post_html = post_html.replace('{{ post_content }}', body)
        post_html = post_html.replace('{{ root }}', '../')
        post_html = post_html.replace('{{ slug }}', slug) # For save button
        
        # 2. Inject post_html into base_template
        full_page = base_template.replace('{{ title }}', metadata.get('title', 'Untitled'))
        full_page = full_page.replace('{{ content }}', post_html)
        full_page = full_page.replace('{{ root }}', '../')
        
        # Metadata injection
        full_page = full_page.replace('{{ description }}', metadata.get('excerpt', 'Thoughts on business, technology, and the human condition.'))
        full_page = full_page.replace('{{ url }}', f"{BASE_URL}/posts/{slug}.html")
        full_page = full_page.replace('{{ image }}', metadata.get('image', DEFAULT_IMAGE))
        
        write_file(os.path.join(OUTPUT_DIR, 'posts', f'{slug}.html'), full_page)
        
        posts.append(metadata)

    # 5. Generate Homepage
    # Sort posts by date (descending) if date exists
    # For now, just list them.
    
    # Generate Filter HTML
    categories = sorted(list(set(p.get('category', 'General') for p in posts if p.get('slug') != 'about')))
    filter_html = '<div class="filter-bar">'
    filter_html += '<button class="filter-btn active" data-filter="all">All</button>'
    for cat in categories:
        filter_html += f'<button class="filter-btn" data-filter="{cat}">{cat}</button>'
    filter_html += '</div>'
    
    posts_html = ""
    for post in posts:
        # Skip about page if it's in content
        if post['slug'] == 'about': 
            continue
            
        posts_html += f"""
            <a href="posts/{post['slug']}.html" class="post-card" data-category="{post.get('category', 'General')}">
                <span class="post-meta">{post.get('category', 'General')} • {post.get('read_time', '5 min read')}</span>
                <h2>{post.get('title', 'Untitled')}</h2>
                <p class="post-excerpt">{post.get('excerpt', '')}</p>
            </a>
        """
        
    index_content = index_template.replace('{{ posts_list }}', posts_html)
    index_content = index_content.replace('{{ filters }}', filter_html)
    
    full_index = base_template.replace('{{ title }}', 'Does This Feel Right?')
    full_index = full_index.replace('{{ content }}', index_content)
    full_index = full_index.replace('{{ root }}', '') # Root is empty for index
    full_index = full_index.replace('{{ description }}', 'Thoughts on business, technology, and the human condition.')
    full_index = full_index.replace('{{ url }}', f"{BASE_URL}/index.html")
    full_index = full_index.replace('{{ image }}', DEFAULT_IMAGE)
    
    write_file(os.path.join(OUTPUT_DIR, 'index.html'), full_index)

    # 6. Generate Login Page
    login_template = read_file(os.path.join(TEMPLATE_DIR, 'login.html'))
    full_login = base_template.replace('{{ title }}', 'Login - Does This Feel Right?')
    full_login = full_login.replace('{{ content }}', login_template)
    full_login = full_login.replace('{{ root }}', '')
    full_login = full_login.replace('{{ description }}', 'Login to your account.')
    full_login = full_login.replace('{{ url }}', f"{BASE_URL}/login.html")
    full_login = full_login.replace('{{ image }}', DEFAULT_IMAGE)
    write_file(os.path.join(OUTPUT_DIR, 'login.html'), full_login)

    # 7. Generate Library Page
    library_template = read_file(os.path.join(TEMPLATE_DIR, 'library.html'))
    full_library = base_template.replace('{{ title }}', 'My Library - Does This Feel Right?')
    full_library = full_library.replace('{{ content }}', library_template)
    full_library = full_library.replace('{{ root }}', '')
    full_library = full_library.replace('{{ description }}', 'Your saved essays.')
    full_library = full_library.replace('{{ url }}', f"{BASE_URL}/library.html")
    full_library = full_library.replace('{{ image }}', DEFAULT_IMAGE)
    write_file(os.path.join(OUTPUT_DIR, 'library.html'), full_library)

    # 8. Generate About Page (Special Case)
    # We can just have an about.md in content and treat it differently or just hardcode it.
    # Let's look for about.html in content
    if os.path.exists(os.path.join(CONTENT_DIR, 'about.html')):
        raw_about = read_file(os.path.join(CONTENT_DIR, 'about.html'))
        meta, body = parse_frontmatter(raw_about)
        
        # About page uses a simpler layout, usually just the article content
        # We can reuse post template logic but without the newsletter box if we wanted, 
        # but for now let's just use the generic page logic.
        
        # Actually, the about page in the design had a newsletter box too.
        # Let's just render it like a post but without the "Back to Home" link maybe?
        # Or just render it.
        
        about_html = f"""
            <article>
                <h1>{meta.get('title')}</h1>
                {body}
                <div class="newsletter-box">
                    <h3>Get the Signal.</h3>
                    <p>Smart analysis for curious minds. Unsubscribe anytime.</p>
                    <form class="newsletter-form">
                        <input type="email" placeholder="Your best email" required class="newsletter-input">
                        <button type="submit" class="newsletter-btn">Subscribe</button>
                    </form>
                    <p class="success-message">You're on the list. Welcome.</p>
                </div>
            </article>
        """
        
        full_about = base_template.replace('{{ title }}', meta.get('title'))
        full_about = full_about.replace('{{ content }}', about_html)
        full_about = full_about.replace('{{ root }}', '')
        full_about = full_about.replace('{{ description }}', meta.get('excerpt', 'About us.'))
        full_about = full_about.replace('{{ url }}', f"{BASE_URL}/about.html")
        full_about = full_about.replace('{{ image }}', DEFAULT_IMAGE)
        
        write_file(os.path.join(OUTPUT_DIR, 'about.html'), full_about)

    # 9. Generate RSS Feed
    import html
    
    rss_items = ""
    for post in posts:
        if post['slug'] == 'about':
            continue
        
        # Escape XML special characters
        title = html.escape(post.get('title', 'Untitled'))
        excerpt = html.escape(post.get('excerpt', ''))
        category = html.escape(post.get('category', 'General'))
        
        rss_items += f"""
        <item>
            <title>{title}</title>
            <link>{BASE_URL}/posts/{post['slug']}.html</link>
            <description>{excerpt}</description>
            <category>{category}</category>
            <guid>{BASE_URL}/posts/{post['slug']}.html</guid>
        </item>
        """
    
    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Does This Feel Right?</title>
    <link>{BASE_URL}</link>
    <description>Thoughts on business, technology, and the human condition.</description>
    <language>en-us</language>
    {rss_items}
</channel>
</rss>"""
    
    write_file(os.path.join(OUTPUT_DIR, 'feed.xml'), rss_feed)

    print("Build complete.")

if __name__ == "__main__":
    build()
