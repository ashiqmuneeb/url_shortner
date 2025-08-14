# PyShort ✂️ — A Python URL Shortener

Clean UI, REST API, custom aliases, click counts, QR, Docker, and easy deployment.

## Features
- Shorten any public http/https URL
- Custom aliases (e.g. `/docs`, `/promo_2025`)
- 302 redirects
- Click analytics (count + last accessed)
- Web UI (Tailwind) + JSON API (FastAPI)
- SQLite by default; switch to Postgres via `DATABASE_URL`
- Docker one-command start

## Quickstart (Local)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# (optional) edit BASE_URL and HASHIDS_SALT in .env
make run  # or: uvicorn app.main:app --reload --port 8000
