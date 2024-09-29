from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from models import Message, User
from datetime import datetime

message_ns = Namespace("message", description="Talker message routes.")

user_model = message_ns.model(
    "User",
    {
        "user_name": fields.String(),
        "user_firstname": fields.String(),
        "user_lastname": fields.String(),
        "user_address": fields.String(),
    }
)

message_model = message_ns.model(
    "Message",
    {
        "message_message": fields.String(),
        "message_type": fields.String(),
        "message_sender": fields.Integer(),
        "message_sentto": fields.Integer(),
        "sender_relationship" : fields.Nested(user_model),
        "sendto_relationship" : fields.Nested(user_model),
    }
)

@message_ns.route("/<string:user_name>/<string:contact_name>")
class MessageResource(Resource):
    @message_ns.marshal_list_with(message_model, skip_none=True)
    @message_ns.param("user_name", "contact_name")
    def get(self, user_name, contact_name):
        sender_id = User.query.filter_by(user_name=user_name).first_or_404()
        sentto_id = User.query.filter_by(user_name=contact_name).first_or_404()
        messages =  Message.query\
                    .filter(((Message.message_sender==sender_id.user_id) & (Message.message_sentto==sentto_id.user_id)) | ((Message.message_sender==sentto_id.user_id) & (Message.message_sentto==sender_id.user_id)))\
                    .order_by(Message.message_dateCreated.asc()).all()
        return messages
    
    @message_ns.marshal_list_with(message_model, skip_none=True)
    @message_ns.param("user_name", "contact_name")
    def post(self, user_name, contact_name):
        data = request.get_json()
        sender_id = User.query.filter_by(user_name=data.get("message_sender")).first_or_404()
        sentto_id = User.query.filter_by(user_name=data.get("message_sentto")).first_or_404()
        new_message = Message(
            message = data.get("message"),
            type = data.get("type"),
            message_sender= sender_id.user_id,
            message_sentto= sentto_id.user_id
        )
        new_message.save()
        return make_response(jsonify({"message":"Message sent."}), 201)
    
    #FUTURE FUNCTIONALITY TO EDIT AND DELETE OWN MESSAGE
    def put(self):
        pass
    def delete(self):
        pass