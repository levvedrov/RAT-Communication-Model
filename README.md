# RAT Communication Model

A Python client-server project built for **cybersecurity education**. It simulates the structure of a command-and-control (C2) system so students can study how such systems communicate, detect them, and build defenses against them.

> This project must only be used in a controlled lab environment you own. See [Disclaimer](#disclaimer).

---

## How It Works

The **server** is a desktop application (Flask + Tkinter) that manages connected agents through a GUI. The **client** is a lightweight agent that connects to the server, registers itself, then polls for tasks on a configurable interval.

```
Client  ──►  /info      register / heartbeat
Client  ◄──  /tasks     poll for next task
Client  ──►  /screen    stream screen frames
Client  ──►  /webcam    stream webcam frames
Client  ──►  /files     send home directory tree
Client  ──►  /download  upload a requested file
```

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

> _Replace with an actual screenshot._

![Main Window](docs/screenshots/main_window.png)

---

### Screen Stream

Clicking **SCREEN** opens a `640×400` stream window titled with the agent's hostname. The server re-queues a `SCREEN` task after every received frame, keeping the feed continuous. Closing the window stops the stream.

> _Replace with an actual screenshot._

![Screen Stream](docs/screenshots/screen_stream.png)

---

### Webcam Stream

Clicking **WEBCAM** opens an identical stream window for the agent's camera. Both the screen and webcam windows can be open simultaneously for the same agent.

> _Replace with an actual screenshot._

![Webcam Stream](docs/screenshots/webcam_stream.png)

---

### File Browser

Clicking **FILE** queues a `FILES` task. The agent walks `~` recursively, builds a JSON tree (name, path, type, size), and POSTs it to `/files`. The server opens a browser window with the full tree — directories in orange, files in grey with size shown. Directories appear before files, both sorted alphabetically. Permission-denied paths are silently skipped.

Selecting a file and clicking **DOWNLOAD** queues a `DOWNLOAD:<path>` task. The agent reads the file in binary and POSTs it to `/download`. The server saves it to `downloads/<agent-id>_<filename>` and updates the status bar at the bottom of the browser window.

> _Replace with an actual screenshot._

![File Browser](docs/screenshots/file_browser.png)

---

## Disclaimer

This software is a **benign educational simulation**. The author does not support any malicious use.

**Allowed:** cybersecurity coursework, network and C2 architecture study, detection engineering, log analysis, local lab demonstrations.

**Prohibited:** unauthorized access to any system, running the client on devices you do not own, any activity that violates laws, university policy, or ethical guidelines.

By using this project you agree to run it only in your own controlled environment and not add malicious functionality.
