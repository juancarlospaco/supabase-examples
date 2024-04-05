import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

data = supabase.table("products").select("*").execute()

supabase.table("products").update({"name": "system76"}).eq("id", 1).execute()
