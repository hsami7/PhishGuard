import os
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.routers import auth, analysis
from app.database import engine
from app import models, security

# Rate limiter: tracks requests per IP
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

# 1. Initialize FastAPI app
app = FastAPI(title="PhishGuard Gateway")

# 2. Add rate limiting middleware
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# 3. Startup: create DB tables
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)
    import sqlite3
    try:
        conn = sqlite3.connect("phishguard.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS phishtank_urls (url TEXT PRIMARY KEY)")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Failed to create phishtank_urls table: {e}")

# Include routers
app.include_router(auth.router)
app.include_router(analysis.router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

@app.get("/dashboard", response_class=HTMLResponse)
def read_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")

@app.get("/admin/stats")
def admin_stats(current_user: models.User = Depends(security.get_current_admin_user)):
    return {"message": "Admin area access granted", "user": current_user.username, "role": current_user.role}
