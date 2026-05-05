from flask import Flask, request, jsonify

users = []

def get_user(id):
    for user in users:
        if id == user.id: return user
    return False

class Connections:
    def __init__(self, id, ip, os, name):
        self.id = id
        self.ip = ip
        self.os = os
        self.name = name
    
    

app = Flask(__name__)



@app.route("/info", methods=["POST"])
def get_info():
    data = request.get_json()
    
    try: 
        id = data.get("id")
        os = data.get("os")
        name = data.get("name")
    except ValueError as e:
        print("[-] Fetching connection error: {e}")  
    if get_user(id) == False: 
        new_user = Connections(id,request.remote_addr,os,name)
        users.append(new_user)
        print(f"\n[+] New connection from {request.remote_addr}")
        print(f"INFO:\n-> ID : {new_user.id}\n-> IP : {new_user.ip}\n-> OS : {new_user.os}\n-> NAME : {new_user.name}\n")
    return "OK"



if __name__ == "__main__":
    app.run(debug=True)