import os
import sys
import smtplib
import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def parse_frontmatter(content):
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    
    frontmatter = parts[1].strip()
    body = parts[2].strip()
    
    metadata = {}
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
            
    return metadata, body

def publish(filepath):
    # Configuration
    SMTP_SERVER = "smtp.gmail.com" # Or your provider
    SMTP_PORT = 587
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASS = os.environ.get('SMTP_PASS')
    SUBSTACK_EMAIL = os.environ.get('SUBSTACK_EMAIL')

    if not all([SMTP_USER, SMTP_PASS, SUBSTACK_EMAIL]):
        print("Error: Missing environment variables (SMTP_USER, SMTP_PASS, SUBSTACK_EMAIL)")
        return

    # Read File
    with open(filepath, 'r') as f:
        content = f.read()

    metadata, body = parse_frontmatter(content)
    title = metadata.get('title', 'Untitled Post')
    
    # Convert to HTML
    html_content = markdown.markdown(body)

    # Create Email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = SMTP_USER
    msg['To'] = SUBSTACK_EMAIL

    part1 = MIMEText(body, 'plain')
    part2 = MIMEText(html_content, 'html')

    msg.attach(part1)
    msg.attach(part2)

    # Send
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, SUBSTACK_EMAIL, msg.as_string())
        server.quit()
        print(f"Successfully sent '{title}' to Substack!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 publish_to_substack.py <path_to_markdown_file>")
    else:
        publish(sys.argv[1])
