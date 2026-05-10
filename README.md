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

> _Screenshot placeholder — replace with an actual screenshot of the main window._

![Main Window](docs/screenshots/main_window.png)

---

### Screen Stream Window

Clicking **SCREEN** opens a dedicated stream window for the selected agent. The server continuously re-queues the `SCREEN` task after each frame is received, producing a live feed. Closing the window stops the stream.

> _Screenshot placeholder — replace with an actual screenshot of the screen stream window._

![Screen Stream](docs/screenshots/screen_stream.png)

---

### Webcam Stream Window

Clicking **WEBCAM** opens a separate stream window showing the agent's camera feed. The stream loop works identically to the screen stream — the server re-queues `WEBCAM` after each frame. Both windows can be open simultaneously for the same agent.

> _Screenshot placeholder — replace with an actual screenshot of the webcam stream window._

![Webcam Stream](docs/screenshots/webcam_stream.png)

---

### Console Log Panel

The right-hand panel displays a real-time event log: new connections, task dispatches, received frames, and offline/online transitions.

> _Screenshot placeholder — replace with an actual screenshot of the console panel._

![Console Log](docs/screenshots/console_log.png)

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
