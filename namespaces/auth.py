from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_ns = Namespace("auth", description="Talker authentication routes.")

signup_model = auth_ns.model(
    "SignUp",
    {
        "user_name": fields.String(),
        "user_email": fields.String(),
        "user_password": fields.String(),
        "user_firstname": fields.String(),
        "user_lastname": fields.String(),
        "user_address": fields.String(),
    }
)

login_model = auth_ns.model(
    "Login",
    {
        "user_name": fields.String(),
        "user_password": fields.String()
    }
) 

@auth_ns.route("/signup")
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()
        user_name_check = User.query.filter_by(user_name = data.get("user_name")).first()
        user_email_check = User.query.filter_by(user_email = data.get("user_email")).first()
        if user_name_check:
            return make_response(jsonify({"ok": False, "message": "A user with the same username already exists"}), 400)
        if user_email_check:
            return make_response(jsonify({"ok": False, "message": "A user with the same email already exists"}), 400)
        new_user = User(
            user_name = data.get("user_name"),
            user_password = generate_password_hash(data.get("user_password")),
            user_email = data.get("user_email"),
            user_firstname = data.get("user_firstname"),
            user_lastname = data.get("user_lastname"),
            user_address = data.get("user_address")
        )
        new_user.save()
        return make_response(jsonify({"ok": True, "message": "Account created successfully."}), 201)
        
@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        db_check = User.query.filter_by(user_name=data.get("user_name")).first()
        if not db_check:
            return make_response(jsonify({"ok":False, "statusText":"Username not found."}), 401)
        if not check_password_hash(db_check.user_password, data.get("user_password")):
            return make_response(jsonify({"ok":False, "statusText":"Invalid password."}), 401)
        if db_check and check_password_hash(db_check.user_password, data.get("user_password")):
            access_token = create_access_token(identity = db_check.user_name)
            refresh_token = create_refresh_token(identity = db_check.user_name)
            #remove information when uploading online. retain ok and add status text
            return make_response(jsonify({"ok": True,"access_token": access_token, "refresh_token": refresh_token, "user_token": data.get("user_name")}), 200)
        
@auth_ns.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity = current_user)
        return make_response(jsonify({"access_token": new_access_token}), 200)
