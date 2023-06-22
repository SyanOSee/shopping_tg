from uuid import uuid4

from flask import *
from flask_admin import Admin
from flask_login import LoginManager, login_user, logout_user, login_required

from data.database.models import Models
from web.flask_models import FlaskModels
from init_loader import cf, db

login_manager = LoginManager()
admin = Admin(name='Database', template_mode='bootstrap3')
server = Flask(__name__, template_folder='templates')

server.secret_key = cf.FLASK_SECRET_KEY
server.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{cf.DATABASE_PATH}?check_same_thread=False'
server.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

login_manager.init_app(server)
admin.add_views(
    FlaskModels.UserModelView(Models.User, db.session_maker()),
    FlaskModels.ProductModelView(Models.Product, db.session_maker()),
    FlaskModels.OrderModelView(Models.Order, db.session_maker())
)
admin.init_app(server)


@login_manager.user_loader
def load_user(user_id):
    return FlaskModels.User(user_id)


@server.route('/')
def home():
    return redirect('/login')


@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        database_user = request.form.get('database_user')
        database_password = request.form.get('database_password')

        if database_user == cf.DATABASE_USER and database_password == cf.DATABASE_PASSWORD:
            login_user(FlaskModels.User(str(uuid4())))
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