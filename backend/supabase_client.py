import os
from supabase import create_client, Client

VITE_SUPABASE_URL = os.getenv("VITE_SUPABASE_URL")
VITE_SUPABASE_API_KEY = os.getenv("VITE_SUPABASE_API_KEY")

supabase: Client = create_client(VITE_SUPABASE_URL, VITE_SUPABASE_API_KEY)
