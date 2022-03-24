# framework
from fastapi import Depends, FastAPI,APIRouter,Request
from fastapi.security.api_key import APIKeyHeader
from fastapi.security import HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
# settings
from app.config import settings
from app.templates import websites
# db
from .database.__init__ import dynamo
from .database.create_user import create_user as db_create_user
from .database.login import login as db_login
from .database.get_all_users import get_all_users as db_get_all_users
from .database.delete_all_users import delete_all_users as db_delete_all_users
# app
app = FastAPI()
api_key_header = APIKeyHeader(name='X-API-Key', auto_error=True)
API_Key = settings.apikey
app_auth = APIRouter()
# CORS
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:4040",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def stratup_table():
    dynamo.create_table()
    dynamo.create_users_table()
@app.get('/get/all/users')
def get_all_users(APIkey: str = Depends(api_key_header)):
    if APIkey == settings.apikey:
        return(db_get_all_users())
    return {"Error": "Your API Key is wrong"}
@app.delete("/delete/all/users")
def delete_all_users_(APIkey: str = Depends(api_key_header)):
    if APIkey == settings.apikey:
        return db_delete_all_users()
    return {"Error":"Your API Key is wrong"}
@app.post("/create/user/{username}/{password}")
def create_user(username: str,password: str):
    db_create_user(username=username,password=password)
@app.post("/logindb/{username}/{password}")
def logindb(username: str,password: str):
    return db_login(username=username,password=password)
@app.get("/signup/", response_class=HTMLResponse)
async def signup():
    return websites.create_user_html
@app.get("/login/" , response_class=HTMLResponse)
async def login():
    return websites.login
@app.get('/loginredi/{username}/{password}' , response_class=HTMLResponse)
async def loginredi(username: str, password: str):
    if db_login(username=username,password=password) == "Logged in Succsessfully":
        return RedirectResponse(url="/home/")
    return RedirectResponse(url="/signup/")
@app.get("/home/", response_class=HTMLResponse)
async def homepage():
    return websites.homepage