from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.routers import auth, analysis
from app.database import engine
from app import models, security

# 1. On initialise d'abord l'application FastAPI
app = FastAPI(title="PhishGuard Gateway")

# 2. Maintenant on peut utiliser le décorateur @app sans NameError
@app.on_event("startup")
def on_startup():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(analysis.router)

# Mount static files (ensure 'static' directory exists)
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
