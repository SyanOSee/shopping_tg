from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, current_user, UserMixin


class FlaskModels:
    class User(UserMixin):
        def __init__(self, user_id):
            self.id = user_id

    class UserModelView(ModelView):
        form_excluded_columns = ['id', 'cart', 'order_ids']
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