# RAT Communication Model

A **controlled cybersecurity study project** developed for academic purposes.  
It demonstrates the structure of a command-and-control (C2) communication model — including agent heartbeats, task polling, and real-time data streaming — so that students can better analyze, detect, and defend against such systems.

> **This project must only be used in your own controlled lab environment. See the [Disclaimer](#disclaimer) section.**

---

## Architecture

```
Client Agent  ──►  POST /info     ──►  Server (Flask)
Client Agent  ◄──  GET  /tasks    ◄──  Server (Flask)
Client Agent  ──►  POST /screen   ──►  Server (Flask + Tkinter UI)
Client Agent  ──►  POST /webcam   ──►  Server (Flask + Tkinter UI)
```

The **client** polls the server on a configurable heartbeat interval, picks up queued tasks, and sends results back. The **server** exposes a Tkinter GUI for managing connected agents and issuing tasks.

---

## Features

| Feature | Description |
|---|---|
| Agent tracking | Live table of connected agents with ID, IP, OS, name, and online/offline status |
| Screen stream | Continuous screen capture streamed to the server UI in a live window |
| Webcam stream | Continuous webcam capture streamed to the server UI in a live window |
| File browser | Full recursive file tree of the agent's home directory, shown in a dedicated UI window |
| File download | Select any file in the browser and download it to the server's `downloads/` folder |
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
| `/screen` | POST | Receives one frame of the screen stream; server immediately re-queues the next capture |
| `/webcam` | POST | Receives one frame of the webcam stream; server immediately re-queues the next capture |
| `/files` | POST | Receives a JSON file tree of the agent's home directory |
| `/download` | POST | Receives a file downloaded from the agent; saved to `downloads/` |

---

## UI Screenshots

### Main Window — Active Connections

The main window shows all connected agents in a live-updated table. Each row displays the agent's ID, IP address, operating system, hostname, and online/offline status. Action buttons at the bottom allow issuing tasks to the selected agent.

<img width="1375" height="896" alt="1" src="https://github.com/user-attachments/assets/18c6ddc1-f6ff-4213-a208-fbab178f34b0" />
<img width="1638" height="907" alt="image" src="https://github.com/user-attachments/assets/2949fd47-9256-4f6b-a0c7-fa933a0a67a8" />


---

### Screen Stream Window

Clicking **SCREEN** opens a dedicated stream window for the selected agent. The server continuously re-queues the `SCREEN` task after each frame is received, producing a live feed. Closing the window stops the stream.

<img width="1645" height="935" alt="image" src="https://github.com/user-attachments/assets/4d25d97f-f646-49cc-b824-7c6970325c8f" />


---

### Webcam Stream Window

Clicking **WEBCAM** opens a separate stream window showing the agent's camera feed. The stream loop works identically to the screen stream — the server re-queues `WEBCAM` after each frame. Both windows can be open simultaneously for the same agent.

<img width="1574" height="886" alt="image" src="https://github.com/user-attachments/assets/93091ded-f9f9-4a1b-99a9-85807d4c255d" />


---

### File Browser Window

Clicking **FILE** sends a `FILES` task to the selected agent. The agent walks its entire home directory recursively and sends a JSON file tree back to the server. The server then opens a dedicated browser window showing the tree — directories in orange, files in grey with their size displayed alongside the name.

Selecting a file and clicking **DOWNLOAD** queues a `DOWNLOAD:<path>` task. The agent reads the file and streams it back; the server saves it to `downloads/` and updates the status bar in the browser window.

> _Screenshot placeholder — replace with an actual screenshot of the file browser window._

![File Browser](docs/screenshots/file_browser.png)

---

### Console Log Panel

The right-hand panel displays a real-time event log: new connections, task dispatches, received frames, and offline/online transitions.

> _Screenshot placeholder — replace with an actual screenshot of the console panel._

![Console Log](docs/screenshots/console_log.png)

---

## File System

The file system feature works in two steps:

### 1. Browse

Clicking **FILE** in the server UI queues a `FILES` task for the selected agent. On the next heartbeat the agent:

1. Walks the user's home directory (`~`) recursively via `os.scandir`
2. Builds a nested JSON tree — each node contains `name`, `path`, `type` (`dir` or `file`), and `size` (bytes)
3. POSTs the tree to `/files`

The server receives it and opens a **File Browser** window — a scrollable treeview where directories are collapsible and files show their size. Directories are sorted before files; both are sorted alphabetically. Permission-denied paths are silently skipped.

### 2. Download

Inside the browser, selecting a file and clicking **DOWNLOAD** queues a `DOWNLOAD:<absolute-path>` task. On the next heartbeat the agent:

1. Reads the file in binary mode
2. POSTs it to `/download` as a multipart upload

The server saves the file to `downloads/<agent-id>_<filename>` and updates the status bar at the bottom of the browser window.

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
