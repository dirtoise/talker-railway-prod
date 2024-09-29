from exts import db
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
    
class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    user_password = db.Column(db.String, nullable=False)
    user_email = db.Column(db.String, nullable=False)
    user_firstname = db.Column(db.String)
    user_lastname = db.Column(db.String)
    user_address = db.Column(db.String)
    user_privilege = db.Column(db.String, nullable=False, default="standard", server_default="standard")
    user_status = db.Column(db.String, nullable=False, default="active", server_default="active")
    user_dateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_name, user_password, user_email, user_firstname, user_lastname, user_address):
        self.user_name = user_name
        self.user_password = user_password
        self.user_email = user_email
        self.user_firstname = user_firstname
        self.user_lastname = user_lastname
        self.user_address = user_address
    def __repr__(self):
        return f"Users:{self.user_name}"
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self, user_name, user_password, user_email, user_firstname, user_lastname, user_address):
        self.user_name = user_name
        self.user_password = user_password
        self.user_email = user_email
        self.user_firstname = user_firstname
        self.user_lastname = user_lastname
        self.user_address = user_address
        db.session.commit()

class ContactList(db.Model):
    __tablename__ = "contactlist"
    contact_id = db.Column(db.Integer, primary_key=True)
    contact_room = db.Column(db.String, nullable=False)
    contact_status = db.Column(db.String, nullable=False, default="contact", server_default="contact")
    contact_dateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    contactuser_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    user_relationship = db.relationship("User", foreign_keys=user_id)
    contactuser_relationship = db.relationship("User", foreign_keys=contactuser_id)
    def __init__(self, contact_room, contact_dateCreated, user_id, contactuser_id, contact_status):
        self.contact_room = contact_room
        self.contact_dateCreated = contact_dateCreated
        self.user_id = user_id
        self.contactuser_id = contactuser_id
        self.contact_status = contact_status
    def save(self):
        db.session.add(self)
        db.session.commit()
    def add(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self, contact_status):
        self.contact_status = contact_status
        db.session.commit()

class Message(db.Model):
    __tablename__ = "message"
    message_id = db.Column(db.Integer, primary_key=True)
    message_message = db.Column(db.String)
    message_type = db.Column(db.String, nullable=False)
    message_dateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    message_sender = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    message_sentto = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    sender_relationship = db.relationship("User", foreign_keys=message_sender)
    sendto_relationship = db.relationship("User", foreign_keys=message_sentto)
    def __init__(self, message, type, message_sender, message_sentto):
        self.message_message = message
        self.message_type = type
        self.message_sender = message_sender
        self.message_sentto = message_sentto
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self, message):
        self.message = message
        db.session.commit()