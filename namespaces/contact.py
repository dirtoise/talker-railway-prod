from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from models import ContactList, User
from datetime import datetime
import os

contact_ns = Namespace("contact", description="Talker contact routes.")

user_model = contact_ns.model(
    "User",
    {
        "user_name": fields.String(),
        "user_firstname": fields.String(),
        "user_lastname": fields.String(),
        "user_address": fields.String(),
    }
)

contact_model = contact_ns.model(
    "Contact",
    {
        "contact_room": fields.String(),
        "contact_status": fields.String(),
        "contact_dateCreated": fields.Date(),
        "user_id": fields.Integer(),
        "contactuser_id": fields.Integer(),
        "user_relationship": fields.Nested(user_model),
        "contactuser_relationship": fields.Nested(user_model),
    }
)

@contact_ns.route("/<string:user_name>")
class ContactListResource(Resource):
    @contact_ns.marshal_list_with(contact_model, skip_none=True)
    @contact_ns.param("user_name")
    def get(self, user_name):
        id = User.query.filter_by(user_name=user_name).first_or_404()
        contacts = ContactList.query.filter_by(user_id=id.user_id).all()
        return contacts

    @contact_ns.expect(contact_model)
    @contact_ns.param("user_name")
    @jwt_required()
    def post(self, user_name):
        data = request.get_json()
        hex_string = os.urandom(15).hex()
        current_id = User.query.filter_by(user_name=data.get("current_username")).first()
        usercontact_id = User.query.filter_by(user_name=data.get("contact_username")).first()
        new_contact = ContactList(
            contact_room = hex_string,
            contact_dateCreated = datetime.utcnow(),
            user_id = current_id.user_id,
            contactuser_id = usercontact_id.user_id,
            contact_status = "contact"
        )
        new_contact.save()
        return make_response(jsonify({"message":"Contact successfully added."}), 201)

    @contact_ns.marshal_list_with(contact_model)
    @contact_ns.param("user_name")
    @jwt_required()
    def put(self, user_name):
        data = request.get_json()
        current_id = User.query.filter_by(user_name=data.get("current_username")).first()
        contact_id = User.query.filter_by(user_name=data.get("contact_username")).first()
        update_contact = ContactList.query\
            .filter_by((ContactList.user_id==current_id & ContactList.contactuser_id==contact_id) | (ContactList.user_id==contact_id & ContactList.contactuser_id==current_id))\
            .first_or_404()
        update_contact.update(data.get("status"))
        return update_contact

    @contact_ns.marshal_list_with(contact_model)
    @contact_ns.param("user_name")
    @jwt_required()
    def delete(self, user_name): #WRITE THIS ONE BETTER
        data = request.get_json()
        current_id = User.query.filter_by(user_name=data.get("current_username")).first()
        contact_id = User.query.filter_by(user_name=data.get("contact_username")).first()
        delete_contact = ContactList.query\
            .filter((ContactList.user_id==current_id.user_id) & (ContactList.contactuser_id==contact_id.user_id))\
            .first_or_404()
        delete_contact_reverse =ContactList.query\
            .filter((ContactList.user_id==contact_id.user_id) & (ContactList.contactuser_id==current_id.user_id))\
            .first_or_404()
        delete_contact.delete()
        delete_contact_reverse.delete()
        return make_response(jsonify({"message":"Contact deleted successfully."}), 200)

#BELOW ROUTE MIGHT BE PUT IN ARCHIVE.PY IN THE FUTURE
@contact_ns.route("/<string:user_name>/archive")
class ContactListResource(Resource):
    @contact_ns.marshal_list_with(contact_model)
    @contact_ns.param("user_name")
    @jwt_required()
    def put(self, user_name):
        data = request.get_json()
        print(data)
        current_id = User.query.filter_by(user_name=data.get("current_username")).first()
        contact_id = User.query.filter_by(user_name=data.get("contact_username")).first()
        update_contact = ContactList.query\
            .filter((ContactList.user_id==current_id.user_id) & (ContactList.contactuser_id==contact_id.user_id))\
            .first_or_404()
        update_contact_reverse =ContactList.query\
            .filter((ContactList.user_id==contact_id.user_id) & (ContactList.contactuser_id==current_id.user_id))\
            .first_or_404()
        update_contact.update(data.get("status"))
        update_contact_reverse.update(data.get("status"))
        return update_contact
    
@contact_ns.route("/confirm/<string:user_name>/<string:contact_name>")
class ContactListResource(Resource):
    @contact_ns.marshal_list_with(contact_model, skip_none=True)
    @contact_ns.param("user_name", "contact_name")
    def get(self, user_name, contact_name):
        id = User.query.filter_by(user_name=user_name).first_or_404()
        contact_id = User.query.filter_by(user_name=contact_name).first_or_404()
        contacts = ContactList.query.filter_by(user_id=id.user_id).filter_by(contactuser_id=contact_id.user_id).all()
        return contacts