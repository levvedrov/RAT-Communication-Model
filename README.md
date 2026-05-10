# RAT Communication Model

A **controlled cybersecurity study project** developed for academic purposes.  
It demonstrates the structure of a command-and-control (C2) communication model — including agent heartbeats, task polling, and real-time data streaming — so that students can better analyze, detect, and defend against such systems.

> **This project must only be used in your own controlled lab environment. See the [Disclaimer](#disclaimer) section.**

---

## Architecture

<img width="1409" height="752" alt="struct" src="https://github.com/user-attachments/assets/5be79057-f8ef-43d9-97ca-61ecb64fb99d" />


The **client** polls the server on a configurable heartbeat interval, picks up queued tasks, and sends results back. The **server** exposes a Tkinter GUI for managing connected agents and issuing tasks.

---

## Features

| Feature | Description |
|---|---|
| Agent tracking | Live table of connected agents with ID, IP, OS, name, and online/offline status |
| Screen stream | Continuous screen capture streamed to the server UI in a live window |
| Webcam stream | Continuous webcam capture streamed to the server UI in a live window |
| Console log | Real-time event log panel inside the server UI |
| Task queue | Per-agent task queue — server issues tasks, client polls and executes |
| Heartbeat | Configurable polling interval; agents marked offline after 15 s of silence |

---

## Project Structure

```
RAT-Communication-Model/
├── server/
│   ├── app.py            # Flask API + Tkinter server UI
│   └── requirements.txt
├── client/
│   ├── app.py            # Agent — polls tasks, sends results
│   ├── .env              # Agent configuration
│   └── requirements.txt
└── README.md
```

---

## Setup

### Requirements

- Python 3.10+

### Server

```bash
cd server
pip install -r requirements.txt
python app.py
```

### Client

1. Edit `client/.env`:

```env
URL=http://<server-ip>:5000
AGENT_ID=<unique-agent-id>
HEARTBEAT=1
```

2. Run:

```bash
cd client
pip install -r requirements.txt
python app.py
```

---

## Configuration

| Variable | Description | Default |
|---|---|---|
| `URL` | Server base URL | `http://127.0.0.1:5000` |
| `AGENT_ID` | Unique identifier for this agent | `1` |
| `HEARTBEAT` | Poll interval in seconds | `1` |

---

## Server API

| Endpoint | Method | Description |
|---|---|---|
| `/info` | POST | Agent registration / heartbeat |
| `/tasks` | POST | Task polling — returns next queued task |
| `/screen` | POST | Receives a screen capture frame |
| `/webcam` | POST | Receives a webcam frame |

---

## UI Screenshots

### Main Window — Active Connections

The main window shows all connected agents in a live-updated table. Each row displays the agent's ID, IP address, operating system, hostname, and online/offline status. Action buttons at the bottom allow issuing tasks to the selected agent.

<img width="1320" height="895" alt="3" src="https://github.com/user-attachments/assets/cea9b7d8-8a4b-4dda-b802-f1ec9d1dee98" />
<img width="1375" height="896" alt="1" src="https://github.com/user-attachments/assets/b5bf4d29-ec5a-45d2-818d-0056c207cd8a" />


---

### Screen Stream Window

Clicking **SCREEN** opens a dedicated stream window for the selected agent. The server continuously re-queues the `SCREEN` task after each frame is received, producing a live feed. Closing the window stops the stream.

<img width="1868" height="899" alt="2" src="https://github.com/user-attachments/assets/1967492e-f87b-40e2-8989-449a9c3ce3a6" />


---

### Webcam Stream Window

Clicking **WEBCAM** opens a separate stream window showing the agent's camera feed. The stream loop works identically to the screen stream — the server re-queues `WEBCAM` after each frame. Both windows can be open simultaneously for the same agent.


---

### Console Log Panel

The right-hand panel displays a real-time event log: new connections, task dispatches, received frames, and offline/online transitions.

---

## Allowed Use Cases

- Cybersecurity coursework and lab assignments
- Network communication and C2 architecture study
- Defensive security and detection engineering research
- Log analysis practice
- Local laboratory demonstrations

## Prohibited Use Cases

- Unauthorized access to any system
- Running the client on devices you do not own or have explicit permission to test
- Any activity that violates laws, university policy, or ethical guidelines

---

## Disclaimer

This software is provided strictly as a **benign educational simulation**.  
The author does not support or encourage any malicious use.

By using this project you agree that:

1. You will only run it in your own controlled environment.
2. You will not use it against real users, public systems, or third-party devices.
3. You will not add malicious functionality.
4. You are solely responsible for complying with all applicable laws and institutional rules.
