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

# ... (rest of the file content remains the same)
