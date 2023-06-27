from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from typing import Optional
from uuid import uuid4

from init_loader import db, cf
from models import UserModel, ProductModel, OrderModel


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
templates = Jinja2Templates(directory="templates")
authentication_backend = AdminAuth(secret_key=cf.SERVER_SECRET_KEY)
admin = Admin(app=app, engine=db.engine, authentication_backend=authentication_backend)
admin.add_view(UserModel)
admin.add_view(ProductModel)
admin.add_view(OrderModel)


@app.get('/set')
async def setting(response: Response):
    response.set_cookie(key='token', value='')
    return True


@app.get('/')
async def home(request: Request):
    return RedirectResponse('/login')


@app.get('/login')
async def login_get(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=cf.BASE_URL,
        port=5000,
        log_level='info'
    )
