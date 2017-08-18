from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.item import ItemModel


class ItemRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Preço é obrigatório!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Todo item necessita de uma venda"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "O item com nome '{}' já existe".format(name)}, 400

        data = ItemRegister.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "Erro ocorreu"}, 500  # internal error server

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = ItemRegister.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemsRegister(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}