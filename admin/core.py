import os
import datetime
import frontmatter
import subprocess
import google.generativeai as genai
import openai
import anthropic
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Configuration
CONTENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../content'))
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

# Supabase Setup
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key) if url and key else None

def get_leads():
    if not supabase:
        return []
    try:
        response = supabase.table('leads').select("*").order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching leads: {e}")
        return []

def get_posts():
    posts = []
    if os.path.exists(CONTENT_DIR):
        for filename in os.listdir(CONTENT_DIR):
            if filename.endswith('.html') or filename.endswith('.md'):
                filepath = os.path.join(CONTENT_DIR, filename)
                with open(filepath, 'r') as f:
                    try:
                        post = frontmatter.load(f)
                        posts.append({
                            'filename': filename,
                            'title': post.get('title', 'Untitled'),
                            'date': post.get('date', 'No Date'),
                            'category': post.get('category', 'Uncategorized'),
                            'status': 'Published', # Simplified
                            'content': post.content,
                            'metadata': post.metadata
                        })
                    except:
                        continue
    
    # Sort by date desc
    posts.sort(key=lambda x: str(x['date']), reverse=True)
    return posts

def save_post(filename, title, date, category, tags, content):
    if not filename:
        # Generate filename from title
        slug = title.lower().replace(' ', '-').replace('?', '').replace(':', '')
        filename = f"{slug}.html"
    
    filepath = os.path.join(CONTENT_DIR, filename)
    print(f"Saving to: {filepath}")
    
    # Create post object
    post = frontmatter.Post(content)
    post['title'] = title
    post['date'] = date
    post['category'] = category
    post['tags'] = tags
    post['read_time'] = '5 min read' 
    
    # Write to file
    with open(filepath, 'w') as f:
        f.write(frontmatter.dumps(post))
        
    return filename

def generate_ai_post(topic, provider='gemini'):
    if provider == 'gemini':
        return _generate_gemini(topic)
    elif provider == 'openai':
        return _generate_openai(topic)
    elif provider == 'anthropic':
        return _generate_anthropic(topic)
    else:
        raise ValueError(f"Unknown provider: {provider}")

def _generate_gemini(topic):
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
            raise Exception('Missing GEMINI_API_KEY environment variable.')
            
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Write a blog post about "{topic}".
    The tone should be personal, reflective, and slightly philosophical, matching the style of "Does This Feel Right?".
    Format the output as a Markdown file with frontmatter.
    
    Frontmatter example:
    ---
    title: The Title of the Post
    date: {datetime.date.today().strftime('%Y-%m-%d')}
    category: Reflections
    tags: [tag1, tag2]
    ---
    
    Content here...
    """
    
    response = model.generate_content(prompt)
    return _save_generated_content(response.text, topic)

def _generate_openai(topic):
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise Exception('Missing OPENAI_API_KEY environment variable.')
    
    client = openai.OpenAI(api_key=api_key)
    
    prompt = f"""
    Write a blog post about "{topic}".
    The tone should be personal, reflective, and slightly philosophical, matching the style of "Does This Feel Right?".
    Format the output as a Markdown file with frontmatter.
    
    Frontmatter example:
    ---
    title: The Title of the Post
    date: {datetime.date.today().strftime('%Y-%m-%d')}
    category: Reflections
    tags: [tag1, tag2]
    ---
    
    Content here...
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return _save_generated_content(response.choices[0].message.content, topic)

def _generate_anthropic(topic):
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise Exception('Missing ANTHROPIC_API_KEY environment variable.')
        
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""
    Write a blog post about "{topic}".
    The tone should be personal, reflective, and slightly philosophical, matching the style of "Does This Feel Right?".
    Format the output as a Markdown file with frontmatter.
    
    Frontmatter example:
    ---
    title: The Title of the Post
    date: {datetime.date.today().strftime('%Y-%m-%d')}
    category: Reflections
    tags: [tag1, tag2]
    ---
    
    Content here...
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    return _save_generated_content(response.content[0].text, topic)

def _save_generated_content(generated_content, topic):
    # Clean up code blocks if present
    if generated_content.startswith('```markdown'):
        generated_content = generated_content.replace('```markdown', '', 1)
    if generated_content.startswith('```'):
            generated_content = generated_content.replace('```', '', 1)
    if generated_content.endswith('```'):
        generated_content = generated_content[:-3]
        
    generated_content = generated_content.strip()
    
    # Parse title to create filename
    try:
        post = frontmatter.loads(generated_content)
        title = post.get('title', 'Untitled AI Post')
    except:
        title = f"AI Post - {topic}"
        
    slug = title.lower().replace(' ', '-').replace('?', '').replace(':', '')
    filename = f"{slug}.html" 
    
    filepath = os.path.join(CONTENT_DIR, filename)
    with open(filepath, 'w') as f:
        f.write(generated_content)
        
    return filename

def refine_content(content, provider='gemini'):
    if provider == 'gemini':
        return _refine_gemini(content)
    elif provider == 'openai':
        return _refine_openai(content)
    elif provider == 'anthropic':
        return _refine_anthropic(content)
    else:
        raise ValueError(f"Unknown provider: {provider}")

def _refine_gemini(content):
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise Exception('GEMINI_API_KEY not found')

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return _run_refine_prompt(model.generate_content, content, is_gemini=True)

def _refine_openai(content):
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise Exception('OPENAI_API_KEY not found')
    
    client = openai.OpenAI(api_key=api_key)
    
    def run_prompt(prompt):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
        
    return _run_refine_prompt(run_prompt, content)

def _refine_anthropic(content):
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise Exception('ANTHROPIC_API_KEY not found')
        
    client = anthropic.Anthropic(api_key=api_key)
    
    def run_prompt(prompt):
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
        
    return _run_refine_prompt(run_prompt, content)

def _run_refine_prompt(generate_func, content, is_gemini=False):
    prompt = f"""
    You are an expert editor for a blog called "Does This Feel Right?".
    The aesthetic is "Intellectual Minimalist". 
    The tone is thoughtful, direct, and slightly philosophical, similar to Nate Jones or Paul Graham.
    
    Please refine the following markdown content. 
    - Fix grammar and spelling.
    - Improve clarity and flow.
    - Remove fluff and filler words ("Signal over Noise").
    - Make headings punchy.
    - Do NOT change the meaning.
    - Return ONLY the refined markdown.
    
    Content:
    {content}
    """
    
    if is_gemini:
        response = generate_func(prompt)
        return response.text
    else:
        return generate_func(prompt)

def publish_git():
    print(f"Publishing from: {REPO_DIR}")
    # Run git commands
    subprocess.run(['git', 'add', '.'], cwd=REPO_DIR, check=True, capture_output=True, text=True)
    subprocess.run(['git', 'commit', '-m', 'Update content via Admin Dashboard'], cwd=REPO_DIR, check=True, capture_output=True, text=True)
    subprocess.run(['git', 'push'], cwd=REPO_DIR, check=True, capture_output=True, text=True)
    return "Published successfully!"

def publish_substack(filename):
    filepath = os.path.join(CONTENT_DIR, filename)
    if not os.path.exists(filepath):
        raise Exception('File not found')
        
    # Browser Automation
    # We run this in the background 
    subprocess.Popen(['python3', 'scripts/publish_to_substack_browser.py', filepath])
    return "Browser automation started! Watch the window."
