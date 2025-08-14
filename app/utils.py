import os
from hashids import Hashids
from urllib.parse import urlparse

HASHIDS_SALT = os.getenv("HASHIDS_SALT", "dev-secret-salt-change-me")
hashids = Hashids(salt=HASHIDS_SALT, min_length=6)

def make_code_from_id(pk: int) -> str:
    return hashids.encode(pk)

def is_public_http_url(url: str) -> bool:
    """
    Basic safety: only allow http/https; block obvious local/private targets.
    """
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    host = (parsed.hostname or "").lower()

    blocked = {"localhost", "127.0.0.1", "0.0.0.0"}
    if host in blocked:
        return False
    # naive private ranges check
    private_prefixes = ("10.", "192.168.", "172.16.", "172.17.", "172.18.", "172.19.",
                        "172.2", "169.254.")
    return not any(host.startswith(p) for p in private_prefixes)

def build_base_url(request, fallback_env: str | None = None) -> str:
    # Prefer explicit BASE_URL, else infer from request (works in dev)
    base = os.getenv("BASE_URL", fallback_env)
    if base:
        return base.rstrip("/")
    return f"{request.url.scheme}://{request.headers.get('host')}".rstrip("/")
