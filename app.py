from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from resources.item import ItemRegister, ItemsRegister
from resources.user import UserRegister
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'lambda'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(ItemRegister, '/item/<string:name>')
api.add_resource(ItemsRegister, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
