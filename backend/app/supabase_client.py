import os
from supabase import create_client, Client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
