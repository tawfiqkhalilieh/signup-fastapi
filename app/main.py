# framework
from fastapi import Depends, FastAPI,APIRouter,Request
from fastapi.security.api_key import APIKeyHeader
from fastapi.security import HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# settings
from app.config import settings
# db
from .database.__init__ import dynamo
from .database.create_user import create_user as db_create_user
from .database.get_all_users import get_all_users as db_get_all_users
from .database.delete_all_users import delete_all_users as db_delete_all_users

# app
app = FastAPI()
api_key_header = APIKeyHeader(name='X-API-Key', auto_error=True)
API_Key = settings.apikey
app_auth = APIRouter()

templates = Jinja2Templates(directory="templates")
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

@app.get("/login/", response_class=HTMLResponse)
async def index():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Create New User</title>
    <style>
html {
  height: 100%;
 }
 body {
  margin:0;
  padding:0;
  font-family: sans-serif;
  background: linear-gradient(#141e30, #243b55);
 }
 .login-box {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 400px;
  padding: 40px;
  transform: translate(-50%, -50%);
  background: rgba(0,0,0,.5);
  box-sizing: border-box;
  box-shadow: 0 15px 25px rgba(0,0,0,.6);
  border-radius: 10px;
 }
 .login-box h2 {
  margin: 0 0 30px;
  padding: 0;
  color: #fff;
  text-align: center;
 }
 .login-box .user-box {
  position: relative;
 }
 .login-box .user-box input {
  width: 100%;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  margin-bottom: 30px;
  border: none;
  border-bottom: 1px solid #fff;
  outline: none;
  background: transparent;
 }
 .login-box .user-box label {
  position: absolute;
  top:0;
  left: 0;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  pointer-events: none;
  transition: .5s;
 }
 .login-box .user-box input:focus ~ label,
 .login-box .user-box input:valid ~ label {
  top: -20px;
  left: 0;
  color: #03e9f4;
  font-size: 12px;
 }
 .login-box form a {
  position: relative;
  display: inline-block;
  padding: 10px 20px;
  color: #03e9f4;
  font-size: 16px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  transition: .5s;
  margin-top: 40px;
  letter-spacing: 4px
 }
 .login-box a:hover {
  background: #03e9f4;
  color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px #03e9f4,
        0 0 25px #03e9f4,
        0 0 50px #03e9f4,
        0 0 100px #03e9f4;
 }
 .login-box a span {
  position: absolute;
  display: block;
 }
 .login-box a span:nth-child(1) {
  top: 0;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #03e9f4);
  animation: btn-anim1 1s linear infinite;
 }
 @keyframes btn-anim1 {
  0% {
   left: -100%;
  }
  50%,100% {
   left: 100%;
  }
 }
 .login-box a span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #03e9f4);
  animation: btn-anim2 1s linear infinite;
  animation-delay: .25s
 }
 @keyframes btn-anim2 {
  0% {
   top: -100%;
  }
  50%,100% {
   top: 100%;
  }
 }
 .login-box a span:nth-child(3) {
  bottom: 0;
  right: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #03e9f4);
  animation: btn-anim3 1s linear infinite;
  animation-delay: .5s
 }
 @keyframes btn-anim3 {
  0% {
   right: -100%;
  }
  50%,100% {
   right: 100%;
  }
 }
 .login-box a span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #03e9f4);
  animation: btn-anim4 1s linear infinite;
  animation-delay: .75s
 }
 @keyframes btn-anim4 {
  0% {
   bottom: -100%;
  }
  50%,100% {
   bottom: 100%;
  }
 }
</style>
</head>
<body>
    <div class="login-box">
        <h2>Create User</h2>
        <form>
         <div class="user-box">
          <input type="text" id="0" required="">
          <label>Username</label>
         </div>
         <div class="user-box">
          <input type="password" id="1" required="">
          <label>Password</label>
         </div>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <button onclick="create_user()">Submit</button>
         </a>
        </form>
       </div>
</body>
<script>
    function create_user(){
    username= document.getElementById('0').value,
    password= document.getElementById('1').value
    url = `/create/user/${username}/${password}`
    fetch(url,{
       method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    }).then(res => {
        return res.json();
    })
    .catch(error => console.log('error'))
}
</script>

</html> """
