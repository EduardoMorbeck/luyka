import re
import os
from io import BytesIO
from uuid import uuid4
from typing import Optional
from functools import lru_cache
from ..supabase_client import get_supabase
import tempfile

BUCKET = os.getenv("SUPABASE_BUCKET", "produtos-images")
PUBLIC_BUCKET = os.getenv("SUPABASE_PUBLIC", "true").lower() == "true"
_filename_re = re.compile(r"[^A-Za-z0-9._-]+")

def _sanitize(name: str) -> str:
    base = name.rsplit("/", 1)[-1]
    base = _filename_re.sub("-", base).strip("-")
    return base[:160]

@lru_cache(maxsize=1)
def _supabase():
    return get_supabase()

def upload_image(produto_id: int, file_bytes: bytes, filename: str, content_type: str) -> dict:
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        supabase = _supabase()
        name = _sanitize(filename)
        key = f"{produto_id}/{uuid4().hex}_{name}"

        supabase.storage.from_(BUCKET).upload(
            path=key,
            file=tmp_path,
            file_options={
                "contentType": content_type,
                "upsert": "true",
                "cacheControl": "31536000",
            },
        )

        if PUBLIC_BUCKET:
            url = supabase.storage.from_(BUCKET).get_public_url(key)
        else:
            signed = supabase.storage.from_(BUCKET).create_signed_url(key, expires_in=3600)
            url = signed.get("signedURL") or signed.get("signed_url")

        return {"path": key, "url": url}
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
def signed_url(path: str, expires: int = 3600) -> Optional[str]:
    if not path:
        return None
    supabase = _supabase()
    if PUBLIC_BUCKET:
        return supabase.storage.from_(BUCKET).get_public_url(path)
    signed = supabase.storage.from_(BUCKET).create_signed_url(path, expires_in=expires)
    return signed["signedURL"]

def delete_image(path: str) -> bool:
    if not path:
        return True
    
    try:
        supabase = _supabase()
        response = supabase.storage.from_(BUCKET).remove([path])
        return True
    except Exception as e:
        print(f"Erro ao excluir imagem do Supabase: {e}")
        return False