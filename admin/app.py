import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
import frontmatter
import subprocess

app = Flask(__name__)

# Configuration
CONTENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../content'))
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

@app.route('/')
def dashboard():
    sort_by = request.args.get('sort', 'date')  # default to date
    
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
                            'status': 'Published'
                        })
                    except:
                        continue
    
    # Sort based on parameter
    if sort_by == 'title':
        posts.sort(key=lambda x: x['title'].lower())
    elif sort_by == 'category':
        posts.sort(key=lambda x: x['category'].lower())
    else:  # default to date
        posts.sort(key=lambda x: str(x['date']), reverse=True)
    
    return render_template('dashboard.html', posts=posts, current_sort=sort_by)

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

if __name__ == '__main__':
    app.run(debug=True, port=5001)
