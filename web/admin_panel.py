from uuid import uuid4

from flask import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy

from data.database.models import Models
from init_loader import db, server, cf

login_manager = LoginManager()
login_manager.init_app(server)


# User class (replace with your own user model)
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


class UserModelView(ModelView):
    form_excluded_columns = ['id', 'basket', 'order_ids']
    column_searchable_list = ['user_id']
    can_edit = False

    @login_required
    def is_accessible(self):
        return current_user.is_authenticated


class ProductModelView(ModelView):
    form_excluded_columns = ['id']
    column_searchable_list = ['product_id', 'category', 'name']
    column_filters = ['category', 'name', 'cost', 'amount', 'discount']

    @login_required
    def is_accessible(self):
        return current_user.is_authenticated


class OrderModelView(ModelView):
    form_excluded_columns = ['id']
    can_edit = False

    @login_required
    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(name='Database', template_mode='bootstrap3')
admin.add_views(
    UserModelView(Models.User, db.session_maker()),
    ProductModelView(Models.Product, db.session_maker()),
    OrderModelView(Models.Order, db.session_maker())
)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@server.route('/')
def home():
    return redirect('/login')


@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        database_user = request.form.get('database_user')
        database_password = request.form.get('database_password')

        if database_user == cf.DATABASE_USER and database_password == cf.DATABASE_PASSWORD:
            login_user(User(str(uuid4())))
            return redirect('/admin')
        # Login failed
        return 'Invalid username or password'

    # GET request, render login form
    return render_template('login.html')


@server.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'


if __name__ == '__main__':
    admin.init_app(server)
    SQLAlchemy().init_app(server)
    server.run(host='0.0.0.0', port=5000, debug=True)
