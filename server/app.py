from flask import Flask, request, jsonify
import threading
import tkinter as tk
import time
import queue
from tkinter import ttk

log_queue = queue.Queue()
OFFLINE_TIMEOUT = 15
OFFLINE_CHECK_PERIOD = 5
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
        self.time_last_seen = time.time()
        self.status = "online"
    
    

app = Flask(__name__)


def render():
    global root, console
    root = tk.Tk()
    root.title("Remote Access")
    root.geometry("1200x800")

    
    console_frame = tk.Frame(root, width=500, bg="#000000")
    console_frame.pack(side="right", fill="y")
    console_frame.pack_propagate(False)   
    
    console = tk.Text(
    console_frame,
    bg="black",
    fg="#FFFFFF",
    font=("Menlo", 11),
    state="disabled",
    bd=0,
    highlightthickness=0,
    relief="flat",
    cursor="arrow"
)
    console.pack(fill="both", expand=True, padx=10, pady=10)
    
    active_frame = tk.Frame(root, width=700, bg="#0D0D0D")
    active_frame.pack(side="left", fill="y")
    active_frame.pack_propagate(False) 
    
    connections_table = ttk.Treeview(
    active_frame,
    columns=("id", "ip", "os", "name", "status"),
    show="headings"
)

    connections_table.heading("id", text="ID")
    connections_table.heading("ip", text="IP")
    connections_table.heading("os", text="OS")
    connections_table.heading("name", text="Name")
    connections_table.heading("status", text="Status")

    connections_table.column("id", width=120)
    connections_table.column("ip", width=120)
    connections_table.column("os", width=100)
    connections_table.column("name", width=180)
    connections_table.column("status", width=100)

    connections_table.pack(fill="both", expand=True, padx=10, pady=10)
    
    def update_connections_list():
        for item in connections_table.get_children():
            connections_table.delete(item)

        for user in users:
            connections_table.insert(
                "",
                "end",
                values=(
                    user.id,
                    user.ip,
                    user.os,
                    user.name,
                    user.status
                )
            )

        root.after(1000, update_connections_list)
    
    def update_console():
        while not log_queue.empty():
            message = log_queue.get()

            console.config(state="normal")
            console.insert("end", message + "\n")
            console.see("end")
            console.config(state="disabled")

        root.after(300, update_console)

    update_connections_list()
    update_console()
        

    root.mainloop()

def log(message):
    print(message)
    log_queue.put(message)

    
@app.route("/info", methods=["POST"])
def get_info():
    data = request.get_json()
    
    try: 
        id = data.get("id")
        os = data.get("os")
        name = data.get("name")
    except ValueError as e:
        log("[-] Fetching connection error: {e}")  
    if get_user(id) == False: 
        new_user = Connections(id,request.remote_addr,os,name)
        users.append(new_user)
        log(f"\n[+] New connection from {request.remote_addr}")
        log(f"INFO:\n-> ID : {new_user.id}\n-> IP : {new_user.ip}\n-> OS : {new_user.os}\n-> NAME : {new_user.name}\n")
        get_user(id).time_last_seen = time.time()
    else:
        log(f"[+] {get_user(id).ip} connected")
        get_user(id).time_last_seen = time.time()
    return "OK"

def handling_inactive_connections(connections):
    while True:
        for con in connections:
            if time.time() - con.time_last_seen >= OFFLINE_TIMEOUT: con.status="offline"
            else: con.status = "online"
        time.sleep(OFFLINE_CHECK_PERIOD)
        

            
    

def run_server():
    app.run(debug=True, use_reloader=False)



if __name__ == "__main__":
    checker_thread = threading.Thread(
        target=handling_inactive_connections,
        args=(users,),
        daemon=True
    )

    server_thread = threading.Thread(
        target=run_server,
        daemon=True
    )

    checker_thread.start()
    server_thread.start()

    render()