import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_SERVICE_KEY not found in .env")
    sys.exit(1)

supabase: Client = create_client(url, key)

def run_migration(filepath):
    with open(filepath, 'r') as f:
        sql = f.read()
    
    # Supabase-py doesn't have a direct 'query' or 'rpc' for raw SQL easily accessible 
    # without a stored procedure, but we can try using the postgrest client or just 
    # assume the user has to run this manually if this fails.
    # Actually, the python client is mostly for data. 
    # A better way for raw SQL is often via the dashboard or a specific PG client.
    # However, we can try to use the `rpc` if we had a function, but we don't.
    
    # ALTERNATIVE: Use the requests library to hit the SQL API if enabled, 
    # but usually it's best to just ask the user or use a postgres library.
    
    # Let's try to use `psycopg2` if available, or just print instructions.
    # But wait, I can use the `admin/app.py` which might have a connection?
    # No, admin app uses supabase-py too.
    
    print(f"Please run the following SQL in your Supabase SQL Editor:\n\n{sql}")

if __name__ == "__main__":
    run_migration('scripts/setup_leads.sql')
