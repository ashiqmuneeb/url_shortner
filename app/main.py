import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Request, status, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.gzip import GZipMiddleware

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import get_db, init_db
from .models import ShortURL
from .schemas import ShortenRequest, ShortenResponse, ExpandResponse
from .utils import make_code_from_id, is_public_http_url, build_base_url

# --- App setup ---
app = FastAPI(title="PyShort ✂️", version="1.0.0", docs_url="/docs", redoc_url="/redoc")
app.add_middleware(GZipMiddleware, minimum_size=500)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Create tables on startup
@app.on_event("startup")
def on_startup():
    init_db()

# --- UI routes ---
@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    recent = db.query(ShortURL).order_by(ShortURL.created_at.desc()).limit(10).all()
    return templates.TemplateResponse("index.html", {"request": request, "recent": recent})

@app.post("/shorten", response_class=HTMLResponse)
def shorten_form(
    request: Request,
    url: str = Form(...),
    custom_alias: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    if not is_public_http_url(url):
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "Only public http/https URLs are allowed.", "recent": recent_list(db)},
            status_code=400,
        )

    # If custom alias provided, try to create directly
    if custom_alias:
        su = ShortURL(code=custom_alias, original_url=url)
        db.add(su)
        try:
            db.commit()
            db.refresh(su)
        except IntegrityError:
            db.rollback()
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": "Alias already taken. Try another.", "recent": recent_list(db)},
                status_code=409,
            )
    else:
        # Create placeholder to get ID, then encode with hashids
        placeholder = ShortURL(code="pending", original_url=url)
        db.add(placeholder)
        db.commit()
        db.refresh(placeholder)
        placeholder.code = make_code_from_id(placeholder.id)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": "Generation collision. Try again.", "recent": recent_list(db)},
                status_code=500,
            )
        su = placeholder

    short_url = f"{build_base_url(request)}/{su.code}"
    # Render result with QR
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "short_url": short_url, "original_url": su.original_url, "code": su.code, "recent": recent_list(db)},
        status_code=201,
    )

def recent_list(db: Session):
    return db.query(ShortURL).order_by(ShortURL.created_at.desc()).limit(10).all()

@app.get("/stats/{code}", response_class=HTMLResponse)
def stats_page(code: str, request: Request, db: Session = Depends(get_db)):
    su = db.query(ShortURL).filter_by(code=code).first()
    if not su:
        raise HTTPException(status_code=404, detail="Short code not found")
    return templates.TemplateResponse("stats.html", {"request": request, "item": su, "short_url": f"{build_base_url(request)}/{code}"})

# --- API routes ---
@app.post("/api/shorten", response_model=ShortenResponse)
def api_shorten(payload: ShortenRequest, request: Request, db: Session = Depends(get_db)):
    url = str(payload.url)
    if not is_public_http_url(url):
        raise HTTPException(status_code=400, detail="Only public http/https URLs are allowed.")

    if payload.custom_alias:
        su = ShortURL(code=payload.custom_alias, original_url=url)
        db.add(su)
        try:
            db.commit()
            db.refresh(su)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=409, detail="Alias already taken.")
    else:
        placeholder = ShortURL(code="pending", original_url=url)
        db.add(placeholder)
        db.commit()
        db.refresh(placeholder)
        placeholder.code = make_code_from_id(placeholder.id)
        db.commit()
        su = placeholder

    return ShortenResponse(code=su.code, short_url=f"{build_base_url(request)}/{su.code}", original_url=su.original_url)

@app.get("/api/expand/{code}", response_model=ExpandResponse)
def api_expand(code: str, db: Session = Depends(get_db)):
    su = db.query(ShortURL).filter_by(code=code).first()
    if not su:
        raise HTTPException(status_code=404, detail="Short code not found")
    return ExpandResponse(
        code=su.code,
        original_url=su.original_url,
        clicks=su.clicks,
        created_at=su.created_at,
        last_accessed=su.last_accessed
    )

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# --- Redirect route (last for priority) ---
@app.get("/{code}")
def redirect(code: str, request: Request, db: Session = Depends(get_db)):
    su = db.query(ShortURL).filter_by(code=code).first()
    if not su:
        raise HTTPException(status_code=404, detail="Short code not found")

    su.clicks = (su.clicks or 0) + 1
    su.last_accessed = datetime.utcnow()
    db.commit()

    return RedirectResponse(url=su.original_url, status_code=status.HTTP_302_FOUND)
