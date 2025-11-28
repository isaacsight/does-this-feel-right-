import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
import frontmatter
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Supabase Setup
from supabase import create_client, Client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Configuration
CONTENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../content'))
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static'))

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

@app.route('/leads')
def leads():
    try:
        response = supabase.table('leads').select("*").order('created_at', desc=True).execute()
        leads_data = response.data
    except Exception as e:
        print(f"Error fetching leads: {e}")
        leads_data = []
    return render_template('leads.html', leads=leads_data)

@app.route('/')
def dashboard():
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
                            'status': 'Published' # Simplified for now
                        })
                    except:
                        continue
    
    # Sort by date desc
    posts.sort(key=lambda x: str(x['date']), reverse=True)
    return render_template('dashboard.html', posts=posts)

@app.route('/edit/<filename>')
def edit(filename):
    filepath = os.path.join(CONTENT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            post = frontmatter.load(f)
            return render_template('editor.html', post=post, filename=filename, content=post.content)
    return redirect(url_for('dashboard'))

@app.route('/new')
def new_post():
    return render_template('editor.html', post={}, filename=None, content="")

@app.route('/save', methods=['POST'])
def save():
    try:
        data = request.form
        filename = data.get('filename')
        title = data.get('title')
        date = data.get('date') or datetime.date.today().strftime('%Y-%m-%d')
        category = data.get('category')
        tags = data.get('tags')
        content = data.get('content')
        
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
            
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Error saving post: {str(e)}", 500

@app.route('/publish', methods=['POST'])
def publish():
    try:
        print(f"Publishing from: {REPO_DIR}")
        # Run git commands
        # Use capture_output=True to get stderr
        subprocess.run(['git', 'add', '.'], cwd=REPO_DIR, check=True, capture_output=True, text=True)
        subprocess.run(['git', 'commit', '-m', 'Update content via Admin Dashboard'], cwd=REPO_DIR, check=True, capture_output=True, text=True)
        subprocess.run(['git', 'push'], cwd=REPO_DIR, check=True, capture_output=True, text=True)
        return jsonify({'status': 'success', 'message': 'Published successfully!'})
    except subprocess.CalledProcessError as e:
        error_msg = f"Git Error: {e.stderr}"
        print(error_msg)
        return jsonify({'status': 'error', 'message': error_msg})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/publish-substack', methods=['POST'])
def publish_substack():
    try:
        data = request.json
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'status': 'error', 'message': 'No filename provided'})
            
        filepath = os.path.join(CONTENT_DIR, filename)
        if not os.path.exists(filepath):
            return jsonify({'status': 'error', 'message': 'File not found'})
            
        with open(filepath, 'r') as f:
            post = frontmatter.load(f)
            
        # Browser Automation
        # We run this in the background so the UI returns immediately
        subprocess.Popen(['python3', 'scripts/publish_to_substack_browser.py', filepath])
        
        return jsonify({'status': 'success', 'message': 'Browser automation started! Watch the window.'})
        
    except Exception as e:
        print(f"Substack Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})



@app.route('/generate-post', methods=['POST'])
def generate_post():
    try:
        data = request.json
        topic = data.get('topic')
        
        if not topic:
            return jsonify({'status': 'error', 'message': 'No topic provided'})
            
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
             return jsonify({'status': 'error', 'message': 'Missing GEMINI_API_KEY environment variable.'})
             
        import google.generativeai as genai
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
        generated_content = response.text
        
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
        filename = f"{slug}.html" # Using .html as per existing convention, though content is MD
        
        filepath = os.path.join(CONTENT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(generated_content)
            
        return jsonify({'status': 'success', 'message': 'Post generated successfully!', 'filename': filename})
        
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/refine', methods=['POST'])
def refine_content():
    try:
        data = request.json
        content = data.get('content')
        
        if not content:
            return jsonify({'status': 'error', 'message': 'No content provided'}), 400

        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return jsonify({'status': 'error', 'message': 'GEMINI_API_KEY not found'}), 500

        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
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
        
        response = model.generate_content(prompt)
        refined_text = response.text
        
        return jsonify({'status': 'success', 'refined_content': refined_text})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
