from flask import request, jsonify
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt
from models import User, ContactList
from werkzeug.security import generate_password_hash, check_password_hash

user_ns = Namespace("user", description="Talker user routes.")

user_model = user_ns.model(
    "User",
    {
        "user_id": fields.Integer(),
        "user_name": fields.String(),
        "user_email": fields.String(),
        "user_password": fields.String(),
        "user_firstname": fields.String(),
        "user_lastname": fields.String(),
        "user_address": fields.String(),
    }
)
#BELOW RETURNS ALL USER IN THE DATABASE. MAY OR MAY NOT CHANGE AT SOME POINT
@user_ns.route("/users")
class UsersResources(Resource):
    @user_ns.marshal_list_with(user_model)
    def get(self):
        users = User.query.all()
        print(users)
        return users
    
@user_ns.route("/<user_name>")
class UserResources(Resource):
    @user_ns.marshal_list_with(user_model)
    def get(self, user_name):
        user = User.query.filter_by(user_name=user_name).first_or_404()
        return user

    #MAY HAVE TO EDIT BELOW ROUTE
    @user_ns.marshal_list_with(user_model)
    @jwt_required()
    def put(self, user_name):
        user_update = User.query.filter_by(user_name=user_name).first_or_404()
        data = request.get_json()
        user_update.update(
            data.get("user_name"),
            data.get("user_password"),
            data.get("user_email"),
            data.get("user_firstname"),
            data.get("user_lastname"),
            data.get("user_address")
        )
        return user_update

    @user_ns.marshal_list_with(user_model)
    @jwt_required()
    def delete(self, user_name):
        user_delete = User.query.filter_by(user_name=user_name).first_or_404()
        user_delete.delete()
        return user_delete

