from flask import request
from flask_socketio import emit, send, join_room, leave_room

from exts import socketio

onlineUsers = []

def go_online(data):
    if data.get("username") == None:
        return
    if not any(dic.get("username") == data.get("username") for dic in onlineUsers):
        return onlineUsers.append({"username": data.get("username"),"socketid":data.get("socketid")})
    for dic in onlineUsers:
        if dic.get("username") == data.get("username"):
            dic.get("socketid") == data.get("socketid")
    
def go_offline(data):
    global onlineUsers
    onlineUsers = [user for user in onlineUsers if user.get("socketid") != data]

def get_user(data):
    user_info = [user for user in onlineUsers if user.get("username") == data.get("specificContact")]
    return user_info

@socketio.on("connection")
def handle_connect():
    print(f"Client with id:{request.sid} connected!")

@socketio.on("go_online")
def handle_go_online(data):
    go_online({"username":data, "socketid":request.sid})

@socketio.on("join_room")
def handle_join_room(data):
    join_room(data.get("room")) #IN THE FUTURE: USE request.sid as argument for to=... ex: to = request.sid
    emit("join_room", {"user_name":data.get("user_name"), "room":data.get("room")}, to=data.get("room"))

@socketio.on("send_message")
def handle_send_message(data):
    emit("receive_message", data, to=data.get("room"))   

@socketio.on("send_notif")
def handle_send_notif(data):
    send_user = get_user(data)
    if(send_user):
        emit("receive_notif", {"user_name": data.get("currentUser")}, to=send_user[0].get("socketid"))
    else:
        print("user offline")

@socketio.on("disconnect")
def handle_disconnect():
    go_offline(request.sid)