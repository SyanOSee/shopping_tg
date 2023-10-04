# Third-party
from fastapi import *
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from sqladmin import Admin

# Project
import config as cf
from database import database
from models import UserModel, ProductModel, OrderModel

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=cf.server['secret_key'], )
admin = Admin(app=app, engine=database.engine)
admin.add_view(UserModel)
admin.add_view(ProductModel)
admin.add_view(OrderModel)


@app.get('/')
async def home(request: Request):
    return RedirectResponse('/admin')


# Define route for admin page
@app.get('/admin')
async def admin_page(request: Request):
    return await admin.index(request)


if __name__ == '__main__':
    from uvicorn import run

    run(
        app=app,
        host=cf.server['host'],
        port=cf.server['port']
    )
