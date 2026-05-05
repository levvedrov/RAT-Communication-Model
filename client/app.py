
from dotenv import load_dotenv
import os
import requests
import time 

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
        
        
def active_loop(pointurl, agentID, heartbeat):
    
    while True:
        try:
            response = requests.post(pointurl, json={"agent_id" : agentID}, timeout=5)
            if response == 200:
                pass # response handling
            
        except requests.exceptions.ConnectionError:
            print("[-] Cannot connect to server")

        except requests.exceptions.Timeout:
            print("[-] Server timeout")

        except Exception as e:
            print(f"[-] Unexpected error: {e}")
        
        time.sleep(heartbeat)
    

agent = Agent()
    
active_loop(agent.pointurl, agent.id, agent.heartbeat)