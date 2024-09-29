from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from models import ContactList, User
from datetime import datetime
import os

request_ns = Namespace("request", description="Talker request routes.")

user_model = request_ns.model(
    "User",
    {
        "user_name": fields.String(),
        "user_firstname": fields.String(),
        "user_lastname": fields.String(),
        "user_address": fields.String(),
    }
)

request_model = request_ns.model(
    "Request",
    {
        "contact_status": fields.String(),
        "contact_dateCreated": fields.Date(),
        "user_id": fields.Integer(),
        "contactuser_id": fields.Integer(),
        "user_relationship": fields.Nested(user_model),
        "contactuser_relationship": fields.Nested(user_model),
    }
)

@request_ns.route("/<string:user_name>")
class RequestListResource(Resource):
    @request_ns.marshal_list_with(request_model, skip_none=True)
    @request_ns.param("user_name")
    def get(self, user_name):
        id = User.query.filter_by(user_name=user_name).first_or_404()
        contacts = ContactList.query.filter_by(user_id=id.user_id).all()
        return contacts
    
    @request_ns.marshal_list_with(request_model)
    @request_ns.param("user_name")
    @jwt_required()
    def post(self, user_name):
        data = request.get_json()
        hex_string = os.urandom(15).hex()
        current_id = User.query.filter_by(user_name=data.get("current_username")).first()
        usercontact_id = User.query.filter_by(user_name=data.get("contact_username")).first()
        new_request = ContactList(
            contact_room = hex_string,
            contact_dateCreated = datetime.utcnow(),
            user_id = current_id.user_id,
            contactuser_id = usercontact_id.user_id,
            contact_status = "request"
        )
        new_request_reverse = ContactList(
            contact_room = hex_string,
            contact_dateCreated = datetime.utcnow(),
            user_id = usercontact_id.user_id,
            contactuser_id =  current_id.user_id,
            contact_status = "requested"
        )
        new_request.save()
        new_request_reverse.save()
        return make_response(jsonify({"message":"Request sent successfully."}), 201)
        
    @request_ns.expect(request_model)
    @request_ns.param("user_name")
    @jwt_required()
    def put(self, user_name):
        data = request.get_json()
        current_id = User.query.filter_by(user_name=data.get("current_username")).first()
        contact_id = User.query.filter_by(user_name=data.get("contact_username")).first()
        update_contact = ContactList.query\
            .filter_by(user_id=contact_id.user_id)\
            .filter_by(contactuser_id=current_id.user_id)\
            .first_or_404()
        update_contact_reverse = ContactList.query\
            .filter_by(user_id=current_id.user_id)\
            .filter_by(contactuser_id=contact_id.user_id)\
            .first_or_404()
        update_contact.update(data.get("status"))
        update_contact_reverse.update(data.get("status"))
        return make_response(jsonify({"message":"Contact added successfully."}), 201)
    
    @request_ns.marshal_list_with(request_model)
    @request_ns.param("user_name")
    @jwt_required()
    def delete(self, user_name):
        data = request.get_json()
        current_id = User.query.filter_by(user_name=data.get("current_username")).first_or_404()
        contact_id = User.query.filter_by(user_name=data.get("contact_username")).first_or_404()
        contact_delete = ContactList.query.filter_by(user_id=contact_id.user_id).filter_by(contactuser_id=current_id.user_id).first_or_404()
        contact_delete_reverse = ContactList.query.filter_by(user_id=current_id.user_id).filter_by(contactuser_id=contact_id.user_id).first_or_404()
        contact_delete.delete()
        contact_delete_reverse.delete()
        return make_response(jsonify({"message":"Request deleted successfully."}), 200)

