import fastapi
from fastapi import FastAPI, APIRouter, Depends, Request,status,Form
from sqlalchemy.orm import Session
from models import UserDetails
from pydantic import BaseModel
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# PostgreSQL database connection Configuration
DATABASE_URL = f"postgresql://joelnencil:123456@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
app = FastAPI()
router = APIRouter()
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    email: str
    password: str

@app.get('/',response_class=HTMLResponse,include_in_schema=False)
def form(request:Request):
    return templates.TemplateResponse("/index.html",{"request":request})


@app.post("/",response_class=HTMLResponse)
async def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user_details = db.query(UserDetails).filter(UserDetails.email == email, UserDetails.password == password).first()
    if user_details:
        response= fastapi.responses.RedirectResponse(url='/dashboard',status_code=status.HTTP_302_FOUND)
        return response
    else:
        return {"message": "Login failed"}
    
@router.get("/dashboard",response_class=HTMLResponse)
def dashboard(request:Request):
    print("hello world")
    return templates.TemplateResponse("/dashboard.html",{"request":request})

