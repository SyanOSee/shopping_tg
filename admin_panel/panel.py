# Third-party
from fastapi import *
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from sqladmin import Admin

# Project
import admin_panel.config as cf
from admin_panel.database import database
from admin_panel.models import UserModel, ProductModel, OrderModel

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=cf.server['secret_key'], )
admin = Admin(app=app, engine=database.engine)
admin.add_view(UserModel)
admin.add_view(ProductModel)
admin.add_view(OrderModel)


# Dependency to get the current user from the session
def get_current_user(token: str = Cookie(default=None)):
    if token is None:
        return None
    return token


# Function to check if credentials are valid
def check_credentials(user: str, password: str):
    return user == cf.database['user'] and password == cf.database['password']


@app.get('/')
async def home(request: Request):
    return RedirectResponse('/login')


# Define route for login form
@app.get('/login')
async def login_form(request: Request):
    with open('templates/login.html', encoding='utf-8') as f:
        response = HTMLResponse(content=f.read())
    response.set_cookie(key='session_token', value='')
    return response


@app.post('/login')
async def login(request: Request):
    form = await request.form()
    user, password = form['username'], form['password']
    if check_credentials(user, password):
        response = RedirectResponse('/admin', status_code=303)
        response.set_cookie(key='session_token', value=cf.server['secret_key'])
        return response
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')


# Define route for admin page
@app.get('/admin')
async def admin_page(request: Request):
    if request.cookies['session_token'] != cf.server['secret_key']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    return await admin.index(request)
