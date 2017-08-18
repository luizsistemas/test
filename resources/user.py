from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Nome não preenchido")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Senha não preenchido")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "Usuário já cadastrado!"}, 400

        user = UserModel(**data)  # data['username'], data['password']
        user.save_to_db()

        return {"message": "User criado com sucesso"}, 201
