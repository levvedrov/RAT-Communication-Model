# Python Client-Server Cybersecurity Study Project

## Overview

This project is a **controlled cybersecurity study project** developed for academic purposes.  
It demonstrates the basic structure of **server-client communication** often discussed in cybersecurity courses, especially in relation to command-and-control architecture, agent communication, heartbeat messages, task polling, logging, and defensive analysis.

The goal of this project is **not to create malware**.  
The goal is to understand how suspicious remote-control systems can be structured so that students can better analyze, detect, and defend against them.

## Academic Purpose Only

This project must be used **only for educational, research, and academic purposes** in a controlled lab environment.

Allowed use cases:

- Cybersecurity coursework
- Network communication study
- Defensive security research
- Log analysis practice
- Detection engineering practice
- Safe client-server architecture learning
- Local laboratory demonstrations

Prohibited use cases:

- Unauthorized access to any system
- Running the client on devices you do not own
- Credential collection
- Keylogging
- Webcam or microphone access
- Persistence mechanisms
- Privilege escalation
- Stealth or evasion techniques
- Real command execution on remote machines
- Data theft or exfiltration
- Any activity that violates laws, university policy, or ethical rules

## Important Disclaimer

This software is provided strictly as a **benign educational simulation**.  
The author does not support or encourage any malicious use of this project.

By using this project, you agree that:

1. You will only run it in your own controlled environment.
2. You will not use it against real users, public systems, or third-party devices.
3. You will not add malicious functionality.
4. You are responsible for following all applicable laws and institutional rules.

## Project Concept

The project uses a simple client-server model:

```text
Client Agent  --->  Server
   sends heartbeat, status, and safe task results

Server  --->  Client Agent
   returns safe academic tasks from an allowlist