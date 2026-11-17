<div align="center">

# ✂️ PyShort

**A fast, clean URL shortener built with Python and FastAPI.**
Custom aliases · Click analytics · QR codes · REST API · One-command Docker

![Python](https://img.shields.io/badge/python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-38B2AC?logo=tailwindcss&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

[Features](#-features) · [Quickstart](#-quickstart) · [API](#-api-reference) · [Configuration](#-configuration) · [Deployment](#-deployment) · [Roadmap](#-roadmap)

</div>

---

## ✨ Features

- 🔗 **Shorten any public `http`/`https` URL** with validation
- 🏷️ **Custom aliases** such as `/docs` or `/promo_2025`
- ↪️ **302 redirects** so links can be edited or analysed later
- 📊 **Click analytics**: total clicks and last accessed time
- 📱 **QR code** generation for every short link
- 🖥️ **Web UI** (Tailwind CSS) and a **JSON API** (FastAPI, with auto-generated docs)
- 🗄️ **SQLite by default**, switch to **PostgreSQL** with one environment variable
- 🐳 **Docker** one-command start

## 🧰 Tech Stack

| Layer      | Technology                         |
|------------|------------------------------------|
| Backend    | Python, FastAPI, Uvicorn           |
| Database   | SQLite (default), PostgreSQL       |
| ID scheme  | Hashids (short, non-sequential codes) |
| Frontend   | Jinja templates + Tailwind CSS     |
| Packaging  | Docker, Docker Compose             |

## 🚀 Quickstart

### Option 1: Docker (recommended)

```bash
git clone https://github.com/ashiqmuneeb/pyshort.git
cd pyshort
cp .env.example .env
docker compose up --build
```

Open **http://localhost:8000**.

### Option 2: Local

**Requirements:** Python 3.11+

```bash
git clone https://github.com/ashiqmuneeb/pyshort.git
cd pyshort

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # Windows: copy .env.example .env
# (optional) edit BASE_URL and HASHIDS_SALT in .env

make run                         # or: uvicorn app.main:app --reload --port 8000
```

- Web UI: http://localhost:8000
- Interactive API docs (Swagger): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## ⚙️ Configuration

All settings are read from environment variables (or the `.env` file).

| Variable        | Default                   | Description                                              |
|-----------------|---------------------------|----------------------------------------------------------|
| `BASE_URL`      | `http://localhost:8000`   | Public URL used when building short links               |
| `HASHIDS_SALT`  | *(change me)*             | Secret salt for generating codes. Keep it private and stable |
| `DATABASE_URL`  | `sqlite:///./pyshort.db`  | SQLAlchemy URL, e.g. `postgresql://user:pass@host:5432/db` |

> ⚠️ Changing `HASHIDS_SALT` after links exist will change how new codes are generated. Set it once and keep it.

## 📡 API Reference

> Endpoint paths below are examples. Check `/docs` for the exact, always up-to-date schema.

### Create a short link

```bash
curl -X POST http://localhost:8000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very/long/path", "alias": "promo_2025"}'
```

`alias` is optional. If omitted, a code is generated automatically.

**Response `201`**

```json
{
  "code": "promo_2025",
  "short_url": "http://localhost:8000/promo_2025",
  "original_url": "https://example.com/very/long/path",
  "created_at": "2026-11-17T10:30:00Z"
}
```

### Get link stats

```bash
curl http://localhost:8000/api/stats/promo_2025
```

```json
{
  "code": "promo_2025",
  "clicks": 42,
  "last_accessed": "2026-11-17T12:05:31Z"
}
```

### Redirect

```bash
curl -i http://localhost:8000/promo_2025
# HTTP/1.1 302 Found
# location: https://example.com/very/long/path
```

### Error codes

| Status | Meaning                                   |
|--------|-------------------------------------------|
| `400`  | Invalid URL or alias format               |
| `404`  | Short code not found                      |
| `409`  | Custom alias already taken                |
| `422`  | Request body failed validation            |

## 🗂️ Project Structure

```
pyshort/
├── app/
│   ├── main.py          # FastAPI app and routes
│   ├── models.py        # Database models
│   ├── schemas.py       # Pydantic request/response models
│   ├── crud.py          # Database operations
│   ├── config.py        # Settings from environment
│   ├── templates/       # Jinja + Tailwind UI
│   └── static/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── .env.example
└── README.md
```

> Adjust this tree to match your actual layout.

## 🧪 Testing

```bash
pip install -r requirements-dev.txt
pytest -q
```

## ☁️ Deployment

**Docker on any VPS**

```bash
docker compose up -d --build
```

Put it behind a reverse proxy (Caddy or Nginx) for HTTPS, and set `BASE_URL` to your public domain.

**Platforms:** works on Render, Railway, Fly.io, or any host that runs a Docker image. For production, use PostgreSQL by setting `DATABASE_URL`.

## 🔒 Security Notes

- Only `http`/`https` URLs are accepted (no `javascript:`, `data:` or `file:` schemes)
- Reserved paths (`api`, `docs`, `static`, etc.) cannot be used as aliases
- Keep `HASHIDS_SALT` secret and out of version control
- Consider adding rate limiting if you expose the service publicly

## 🗺️ Roadmap

- [ ] Link expiry dates
- [ ] User accounts and per-user dashboards
- [ ] API keys and rate limiting
- [ ] Analytics charts (referrer, country, device)
- [ ] Bulk link creation via CSV

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Commit your changes and run the tests
4. Open a pull request

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

<div align="center">

Built by [Ashiq Muneeb](https://github.com/ashiqmuneeb) · If you find this useful, give it a ⭐

</div>
