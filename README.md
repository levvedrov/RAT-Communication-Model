
# RAT Communication Model

A Python client-server project built for **cybersecurity education**. It simulates the structure of a command-and-control (C2) system so students can study how such systems communicate, detect them, and build defenses against them.

> This project must only be used in a controlled lab environment you own. See [Disclaimer](#disclaimer).

---

<img width="1375" height="896" alt="1" src="https://github.com/user-attachments/assets/6f9d4a3c-5aba-4c78-bbb6-a77433408f16" />


## How It Works

The **server** is a desktop application (Flask + Tkinter) that manages connected agents through a GUI. The **client** is a lightweight agent that connects to the server, registers itself, then polls for tasks on a configurable interval.



Each task is issued from the server GUI, queued per agent, and picked up by the client on the next heartbeat.

---

## Features

| Feature | Description |
|---|---|
| Agent tracking | Live table showing ID, IP, OS, hostname, and online/offline status for every connected agent |
| Screen stream | Continuous screen capture — each frame triggers the next, producing a live feed in a dedicated window |
| Webcam stream | Same streaming loop as screen, using the agent's default camera |
| File browser | Recursive tree of the agent's home directory displayed in a collapsible Treeview window |
| File download | Select any file in the browser and pull it to the server's `downloads/` folder |
| Console log | Real-time event log panel built into the main window |
| Heartbeat | Configurable poll interval; agents go offline after 15 s of silence |

---

## Project Structure

```
RAT-Communication-Model/
├── server/
│   ├── app.py            # Flask API + Tkinter UI
│   └── requirements.txt
├── client/
│   ├── app.py            # Agent
│   ├── .env              # Agent config
│   └── requirements.txt
└── README.md
```

---

## Setup

**Python 3.10+ required.**

### Server

```bash
cd server
python -m pip install -r requirements.txt
python app.py
```

### Client

Edit `client/.env`:

```env
URL=http://<server-ip>:5000
AGENT_ID=<unique-id>
HEARTBEAT=1
```

Then run:

```bash
cd client
python -m pip install -r requirements.txt
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

| Endpoint | Method | Body | Description |
|---|---|---|---|
| `/info` | POST | JSON | Agent registration and heartbeat |
| `/tasks` | POST | JSON | Returns the next queued task for the agent |
| `/screen` | POST | multipart | One frame of the screen stream; server re-queues next immediately |
| `/webcam` | POST | multipart | One frame of the webcam stream; server re-queues next immediately |
| `/files` | POST | JSON | Full recursive file tree of the agent's home directory |
| `/download` | POST | multipart | A file requested via the browser; saved to `downloads/` |

---

## UI Screenshots

### Main Window

The main window is split into two panels. The left panel shows **Active Connections** — a live-updated table with each agent's ID, IP, OS, hostname, and status. Online agents appear in green, offline in red. Clicking a row selects it with a dark highlight while keeping the status colour. Three action buttons sit at the bottom: **WEBCAM**, **SCREEN**, and **FILE**. The right panel is a read-only **Console** with a scrolling log of all server events.

<img width="1320" height="895" alt="3" src="https://github.com/user-attachments/assets/97e1bd23-f372-43b6-9dae-244fe7abaeb9" />

<img width="1320" height="895" alt="3" src="https://github.com/user-attachments/assets/0e54a55f-7dcc-47f4-897f-dbb33e1ebf79" />

---

### Screen Stream

Clicking **SCREEN** opens a `640×400` stream window titled with the agent's hostname. The server re-queues a `SCREEN` task after every received frame, keeping the feed continuous. Closing the window stops the stream.

<img width="1505" height="848" alt="image" src="https://github.com/user-attachments/assets/4f36d820-e433-405a-abe1-8bc616ac8cbe" />


---

### Webcam Stream

Clicking **WEBCAM** opens an identical stream window for the agent's camera. Both the screen and webcam windows can be open simultaneously for the same agent.

<img width="1497" height="905" alt="image" src="https://github.com/user-attachments/assets/af82ad01-0ccb-426f-b124-1e253d061828" />


---

### File Browser

Clicking **FILE** queues a `FILES` task. The agent walks `~` recursively, builds a JSON tree (name, path, type, size), and POSTs it to `/files`. The server opens a browser window with the full tree — directories in orange, files in grey with size shown. Directories appear before files, both sorted alphabetically. Permission-denied paths are silently skipped.

Selecting a file and clicking **DOWNLOAD** queues a `DOWNLOAD:<path>` task. The agent reads the file in binary and POSTs it to `/download`. The server saves it to `downloads/<agent-id>_<filename>` and updates the status bar at the bottom of the browser window.

<img width="1587" height="949" alt="image" src="https://github.com/user-attachments/assets/d205db9d-26da-4389-9995-649ea859ccac" />


---

## Disclaimer

This software is a **benign educational simulation**. The author does not support any malicious use.

**Allowed:** cybersecurity coursework, network and C2 architecture study, detection engineering, log analysis, local lab demonstrations.

**Prohibited:** unauthorized access to any system, running the client on devices you do not own, any activity that violates laws, university policy, or ethical guidelines.

By using this project you agree to run it only in your own controlled environment and not add malicious functionality.
