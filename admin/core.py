"""
This core module provides the main functionality for the admin dashboard application.
It handles tasks such as fetching and saving blog posts, generating AI-written content,
refining content, and publishing updates to the Git repository and Substack.
"""

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

def get_posts():
    """
    Retrieves all blog posts from the content directory.

    Returns:
        list: A list of blog post objects, each containing the post's metadata and content.
    """
    posts = []
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith('.md'):
            with open(os.path.join(CONTENT_DIR, filename), 'r') as file:
                post = frontmatter.load(file)
                posts.append(post)
    return posts

# ... (rest of the file content remains the same)
