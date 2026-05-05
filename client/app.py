
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
        
        
def handle_task(tsk):
    pass
 
def connect(url):
    id, name, os =  me.id, socket.gethostname(), platform.system()
    res = requests.post(url+"/info", json={"id" : id, "os" : os, "name" : name}, timeout=5)
    while res.text != "OK":
        res = requests.post(url+"/info", json={"id" : id, "os" : os, "name" : name}, timeout=5)
    
    
        
def active_loop(pointurl, agentID, heartbeat):
    connect(pointurl)
    
    while True:
        try:
            response = requests.post(pointurl, json={"agent_id" : agentID}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                if data.get("task"):
                    task = data.get("task")
                    print(f"[+] Task received: {task}")
                    handle_task(task)
                    
                    
            
        except requests.exceptions.ConnectionError:
            print("[-] Cannot connect to server")

        except requests.exceptions.Timeout:
            print("[-] Server timeout")

        except Exception as e:
            print(f"[-] Unexpected error: {e}")
        
        time.sleep(heartbeat)
    

me = Agent()
    
active_loop(me.pointurl, me.id, me.heartbeat)