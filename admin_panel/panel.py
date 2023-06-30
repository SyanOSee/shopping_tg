from typing import Optional
from uuid import uuid4
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.middleware.sessions import SessionMiddleware

from models import UserModel, ProductModel, OrderModel
from init_loader import db, cf

load_dotenv()


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form['username'], form['password']
        if username == cf.DATABASE_USER and password == cf.DATABASE_PASSWORD:
            request.session.update({'token': str(uuid4())})
            request.cookies.update({'logout': 'False'})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.update({'logout': 'True'})
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        if request.cookies.get('logout') == 'True' or request.session.get('logout') == 'True':
            request.session.update({'token': None, 'logout': None})
            request.cookies.update({'token': '', 'logout': 'False'})
        if not request.session.get('token') and not request.cookies.get('token'):
            response = RedirectResponse(request.url_for('login_get'))
            response.set_cookie(key='logout', value='False')
            response.set_cookie(key='token', value='')
            return response


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=cf.SERVER_SECRET_KEY, )
authentication_backend = AdminAuth(secret_key=cf.SERVER_SECRET_KEY)
admin = Admin(app=app, engine=db.engine, authentication_backend=authentication_backend)
admin.add_view(UserModel)
admin.add_view(ProductModel)
admin.add_view(OrderModel)


@app.get('/')
async def home(request: Request):
    return RedirectResponse('/login')


@app.get('/login')
async def login_get(request: Request):
    with open(os.path.dirname(os.path.abspath(__file__)) + '/web/templates/login.html', encoding='utf-8') as f:
        content = f.read()
        return HTMLResponse(content=content)


@app.post('/login')
async def login_post(request: Request):
    if await authentication_backend.login(request):
        response = RedirectResponse('/admin', status_code=303)
        response.set_cookie(key='token', value=request.session.get('token'))
        response.set_cookie(key='logout', value=request.cookies.get('logout'))
        return response
    return 'Invalid data'


@app.get('/admin')
async def admin_panel(request: Request):
    return await admin.index(request)


if __name__ == '__main__':
    from uvicorn import run

    run(
        app,
        host=cf.SERVER_HOST,
        port=int(cf.SERVER_PORT)
    )
