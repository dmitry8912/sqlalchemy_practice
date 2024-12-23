from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import create_engine
import uvicorn
from models import User, Order
from config import app_config

db_engine = create_engine(
    str(app_config.postgresql_dsn)
)

app = FastAPI()
admin = Admin(app, db_engine, base_url="/")

class UsersAdminView(ModelView, model=User):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = [User.id, User.name, User.balance]
    column_sortable_list = [User.id, User.name, User.balance]
    column_default_sort = [(User.name, True)]


class OrdersAdminView(ModelView, model=Order):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = [Order.id, Order.user_id, Order.amount]
    column_sortable_list = [Order.id, Order.user_id, Order.amount]
    column_default_sort = [(Order.amount, True)]


admin.add_view(UsersAdminView)
admin.add_view(OrdersAdminView)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8089, forwarded_allow_ips='*', proxy_headers=True)
