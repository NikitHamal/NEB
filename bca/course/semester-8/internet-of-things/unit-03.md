---
subject: Internet of Things
grade: BCA Semester 8 (Elective IV)
unit: 3
title: IoT Platform Design Methodology
hours: 6
area: BCA 454 · Internet of Things · Unit 3
---

Wiring one sensor to one board is a lab exercise. Building a **system** that many people rely on (a weather network, a cold chain, a smart building) needs a method: what is the purpose, what are the entities, what does the data look like, which services exist, where does each piece run, and how is it operated? Bahga and Madisetti, the main text of this course, give a ten-step **IoT platform design methodology**. The outline for this unit is a single case study, the **weather monitoring system**, so this unit teaches the ten steps and works the case through every one, with a working miniature implementation.

::: key What this unit gives you
- The ten design steps and what each step produces.
- The weather monitoring system carried through the steps: requirements, process, domain, information and service models, level, functional and operational views, integration and application.
- A runnable miniature (a web service, a controller and a rules engine) written with the Python standard library only.
- Model answers on how to present a design in an examination.
:::

## 3.1 The ten steps of the methodology

| Step | Name | Question it answers | Output |
|---|---|---|---|
| 1 | **Purpose and requirements specification** | What is the system for? What behaviour, management, analysis, deployment and security does it need? | A requirements list |
| 2 | **Process specification** | What are the steps and decisions of the use cases? | Process diagram |
| 3 | **Domain model specification** | Which physical entities, devices, resources and services exist and how are they related? | Domain model diagram |
| 4 | **Information model specification** | What information (attributes, relations) describes each virtual entity? | Information model |
| 5 | **Service specification** | Which services (inputs, outputs, endpoints, schedules) are needed? | Service table |
| 6 | **IoT level specification** | Which deployment level (1 to 6) suits the system? | The chosen level |
| 7 | **Functional view specification** | How are the functions grouped into the functional groups? | Functional view |
| 8 | **Operational view specification** | Where do the components run (devices, servers, storage, protocols)? | Operational view |
| 9 | **Device and component integration** | How are the devices, boards and software wired together? | Integration (circuit, deployment) |
| 10 | **Application development** | What does the user interface do? | Application (dashboard, API) |

The order matters: requirements and process come before any hardware, the models describe the system independently of products, and the views map them onto real parts. Skipping to step 9 first is how projects end with the wrong sensors.

## 3.2 Step 1: Purpose and requirements for the weather monitor

**Purpose.** A weather monitoring system collects data on environmental conditions (temperature, pressure, humidity and light) in an area using several end nodes, publishes the data to the cloud, and lets users view current values and history.

The requirements are grouped under five headings; these are the headings the examiner expects.

| Heading | Requirement for the weather system |
|---|---|
| **Behaviour** | Each end node senses temperature, pressure, humidity and light at a fixed interval and sends the data to the cloud. |
| **System management** | Nodes can be monitored and configured remotely (sampling interval, node status, firmware version). |
| **Data analysis** | Analysis is done in the cloud: daily minimum and maximum, averages, trends, simple alerts. |
| **Application deployment** | The dashboard and the data service run in the cloud; the web application is available on phones and PCs. |
| **Security** | Only registered nodes may send data; users must log in; data are sent over encrypted links. |

::: note Write measurable requirements
"Collect weather data" is vague. Better: "each node samples every 60 seconds, a reading appears on the dashboard within 5 seconds, and 12 months of hourly history are kept". With such numbers the later steps (data volume, protocol, level) can be calculated, which the program in Section 3.9 does.
:::

## 3.3 Step 2: Process specification

The process specification turns the use cases into a flow. For the weather monitor the main use case is **monitoring**:

1. Start (the node boots and registers with the cloud).
2. Wait for the sampling interval.
3. Read the four sensors.
4. Package the readings with the node ID and timestamp.
5. Publish them to the cloud service.
6. The cloud stores them and evaluates the rules (for example "temperature above 40" or "pressure falling fast").
7. If a rule fires, notify the user; in every case update the dashboard.
8. Go back to step 2.

```svgfig label="3.1" caption="Process specification of the weather monitor: the node loops over read, package and publish; the cloud stores, evaluates rules and updates the dashboard."
f = Fig(640, 230)
f.box(10, 90, 76, 44, "Start:\nboot and\nregister", fill=SOFT, stroke=SLATE, size=9.5)
f.box(110, 90, 80, 44, "Wait for\ninterval", fill=BLUE, stroke=NAVY, size=10)
f.box(215, 90, 90, 44, "Read 4\nsensors", fill=BLUE, stroke=NAVY, size=10)
f.box(330, 90, 90, 44, "Package with\nID and time", fill=BLUE, stroke=NAVY, size=10)
f.box(445, 90, 80, 44, "Publish to\ncloud", fill=SAND, stroke=AMBER, size=10)
f.box(550, 30, 80, 44, "Store in\ndatabase", fill=MINT, stroke=TEAL, size=10)
f.box(550, 100, 80, 44, "Evaluate\nrules", fill=MINT, stroke=TEAL, size=10)
f.box(550, 170, 80, 44, "Update\ndashboard", fill=MINT, stroke=TEAL, size=10)
for a, b in ((86, 110), (190, 215), (305, 330), (420, 445)):
    f.arrow([(a, 112), (b, 112)], color=NAVY)
f.arrow([(525, 105), (550, 52)], color=TEAL)
f.arrow([(525, 112), (550, 122)], color=TEAL)
f.arrow([(525, 122), (550, 190)], color=TEAL)
f.arrow([(150, 90), (150, 50), (480, 50), (480, 90)], color=SLATE, dash=True, label="repeat every interval", lpos=(315, 42))
```

## 3.4 Step 3: Domain model specification

The **domain model** names the concepts of the problem and how they relate, without choosing products. Five kinds of concept appear:

| Concept | Meaning | In the weather system |
|---|---|---|
| **Physical entity** | The real thing of interest | The environment at a location |
| **Virtual entity** | Its digital representation (with an ID) | "Weather at site 7" record |
| **Device** | The hardware that links the physical and digital | The end node with its board |
| **Resource** | Software or data on the device that gives access to it | Sensor drivers, the on-device network stack, storage |
| **Service** | An interface to use the device or resource | A controller service on the node; a web service in the cloud |

The relations are: a **device** is attached to (monitors) a **physical entity**; a **virtual entity** represents the physical entity; **resources** are hosted on the device; **services** expose the resources. Here, the node (device) has temperature, pressure, humidity and light **sensors** (resources) and monitors the environment (physical entity), which is represented by a virtual entity "Weather at site 7"; a controller service exposes the readings.

```svgfig label="3.2" caption="Domain model of the weather monitor. The device monitors the physical entity, the virtual entity represents it, resources run on the device and services expose the resources."
f = Fig(640, 250)
f.box(240, 10, 160, 44, "Physical entity\nEnvironment at site 7", fill=SOFT, stroke=SLATE, size=10)
f.box(20, 100, 170, 44, "Virtual entity\nWeather at site 7", fill=BLUE, stroke=NAVY, size=10)
f.box(450, 100, 170, 44, "Device\nEnd node (board)", fill=SAND, stroke=AMBER, size=10)
f.box(450, 190, 170, 44, "Resources\n4 sensors, drivers", fill=MINT, stroke=TEAL, size=10)
f.box(240, 190, 170, 44, "Services\ncontroller, web service", fill=MINT, stroke=TEAL, size=10)
f.arrow([(105, 100), (240, 40)], color=NAVY, label="represents", lpos=(130, 60))
f.arrow([(535, 100), (400, 40)], color=AMBER, label="monitors", lpos=(500, 60))
f.arrow([(535, 190), (535, 144)], color=TEAL, label="hosted on", lpos=(580, 170))
f.arrow([(410, 212), (450, 212)], color=TEAL, label="", lpos=(430, 205))
f.arrow([(240, 212), (105, 144)], color=TEAL, label="exposes data of", lpos=(120, 190))
```

## 3.5 Step 4: Information model specification

The **information model** defines the structure of the information: the virtual entity, its attributes and the relations, **without** saying how it is stored. For the weather monitor:

| Virtual entity | Attribute | Type and unit | Example |
|---|---|---|---|
| Weather station | `node_id` | text | `"ktm-07"` |
| | `timestamp` | UTC date-time | `"2026-04-12T06:30:00Z"` |
| | `temperature` | number, degrees C | 18.4 |
| | `humidity` | number, percent | 72.0 |
| | `pressure` | number, hPa | 856.2 |
| | `light` | number, lux | 5400 |

Relations: one *Weather station* has many *readings* over time, and each reading has exactly one timestamp. A later design could add a `location` (latitude, longitude, altitude) to the station, which the information model makes easy because it is separate from the storage choice.

## 3.6 Step 5: Service specification

A **service specification** lists each service with its **type**, **inputs**, **outputs**, **endpoints**, **schedule** and **preconditions or effects**. The weather system has two:

| Service | Where it runs | Type | Input | Output | Notes |
|---|---|---|---|---|---|
| **Controller service** | On the end node | Native (a background program) | Sensor values read at the configured interval | A message to the web service | Calls the sensor drivers, formats the data, publishes it, restarts after failure |
| **Web service** | In the cloud | REST | `POST /readings` with a JSON body; `GET /readings?node=...` | JSON confirmation or the list of readings | Stores data in the database, runs the rules, serves the dashboard |

An example of the REST contract:

| Method and path | Meaning | Success code |
|---|---|---|
| `POST /nodes/{id}/readings` | Add a reading to node `{id}` | 201 Created |
| `GET /nodes/{id}/readings?last=10` | The last ten readings | 200 OK |
| `GET /nodes/{id}/summary` | Minimum, maximum and average of the stored readings | 200 OK |
| `PUT /nodes/{id}/config` | Change the sampling interval | 200 OK |

## 3.7 Step 6: IoT level specification

The weather system has **many independent end nodes** (one per site), the data are stored and analysed in the **cloud**, and the cloud also sends configuration and commands back to the nodes. This matches **IoT level 6** of Section 1.5: independent nodes, cloud storage, cloud analysis, cloud application and a **centralised controller** in the cloud. If there were only one node at one site with a local display, level 1 would do.

::: example Why not level 1 or 3?
Level 1 keeps everything on the node, so there is no history shared between sites. Level 3 allows one node only; the weather system needs many. Level 5 uses a coordinator node that gathers data from the end nodes; in the weather case each node can reach the Internet by itself (Wi-Fi or cellular) and no coordinator is required, which is exactly the difference between 5 and 6.
:::

## 3.8 Steps 7 and 8: Functional and operational views

**Functional view.** The **functional view** groups the functions of the system into the six **functional groups** met in Section 1.3 and shows the **functional components** in each.

| Functional group | Weather monitor components |
|---|---|
| **Device** | Four sensors (temperature, humidity, pressure, light), the board, firmware |
| **Communication** | Wi-Fi interface, HTTP or MQTT client |
| **Services** | Controller service on the node, web service in the cloud |
| **Management** | Node status and configuration (interval, version), device registry |
| **Security** | Node authentication (API key or certificate), user login, TLS |
| **Application** | Dashboard (current values, charts), alerts, mobile view |

**Operational view.** The **operational view** says where each component runs and which products and protocols are chosen. For the weather monitor (the choices are examples):

| Item | Choice |
|---|---|
| Device | Raspberry Pi (or ESP32) with a DHT22 or BME280 (temperature, humidity, pressure) and a BH1750 light sensor |
| Communication | Wi-Fi to the Internet; HTTPS REST or MQTT over TLS to the cloud |
| Controller service | Python script on the node, started at boot (systemd) |
| Web service | Python (Flask, Django REST framework or FastAPI) on a cloud VM or PaaS |
| Storage | Relational or time-series database in the cloud |
| Application | Web dashboard using a charting library, also usable on phones |
| Security | HTTPS, a per-node secret, hashed user passwords |

```svgfig label="3.3" caption="Operational view of the weather monitor at level 6: independent nodes publish over HTTPS to a cloud web service that stores data in a database, runs the rules and feeds the dashboard, and the controller in the cloud sends configuration back."
f = Fig(640, 260)
for i, y in enumerate((20, 90, 160)):
    f.box(10, y, 130, 56, "End node %d\nboard + 4 sensors\ncontroller service" % (i + 1), fill=BLUE, stroke=NAVY, size=9.5)
    f.arrow([(140, y + 28), (230, 128)], color=NAVY)
f.box(230, 20, 220, 210, "", fill=SOFT, stroke=SLATE)
f.text(340, 38, "Cloud", size=11, color=NAVY, bold=True)
f.box(250, 52, 180, 40, "Web service (REST, HTTPS)", fill=SAND, stroke=AMBER, size=10)
f.box(250, 102, 180, 36, "Database", fill=MINT, stroke=TEAL, size=10)
f.box(250, 148, 180, 36, "Rules and analysis", fill=MINT, stroke=TEAL, size=10)
f.box(250, 192, 180, 28, "Controller / management", fill=BLUE, stroke=NAVY, size=10)
f.box(500, 90, 130, 56, "Dashboard\nweb and mobile", fill=MINT, stroke=TEAL, size=10)
f.arrow([(450, 118), (500, 118)], color=NAVY, both=True)
f.arrow([(230, 206), (140, 206), (140, 190)], color=AMBER, dash=True, label="config", lpos=(190, 198))
```

## 3.9 Step 9: Device and component integration

Integration connects the parts: sensors to the board (Unit 2), the board to the network, the node to the web service. Before building, **size the system**. With one reading per 60 seconds per node, each stored as a JSON message of about 120 bytes, and 50 nodes, the data volume can be calculated:

```python
nodes, interval_s, msg_bytes = 50, 60, 120
per_day_each = 24 * 3600 // interval_s
total_msgs = per_day_each * nodes
print("messages per node per day:", per_day_each)
print("messages per day, all nodes:", total_msgs)
print("payload per day: %.2f MB" % (total_msgs * msg_bytes / 1e6))
print("payload per year: %.2f GB" % (total_msgs * msg_bytes * 365 / 1e9))
# an HTTP request adds about 300 bytes of headers; MQTT adds 2 bytes of fixed header plus the topic (about 20 bytes)
http_total = total_msgs * (msg_bytes + 300) * 365 / 1e9
mqtt_total = total_msgs * (msg_bytes + 22) * 365 / 1e9
print("per year with HTTP headers: %.2f GB, with MQTT headers: %.2f GB" % (http_total, mqtt_total))
```
```output
messages per node per day: 1440
messages per day, all nodes: 72000
payload per day: 8.64 MB
payload per year: 3.15 GB
per year with HTTP headers: 11.04 GB, with MQTT headers: 3.73 GB
```
The miniature below integrates the **web service**, the **controller service** and the **rules** in one Python program using only the standard library. The server runs in a thread on a free local port with an in-memory SQLite database; the controller posts simulated readings by HTTP, as the real node would (replace `fake_sensor` by the sensor drivers of Unit 2); a rule flags a possible frost.

```python
import json, sqlite3, threading, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

db = sqlite3.connect(":memory:", check_same_thread=False)
db.execute("CREATE TABLE readings (node TEXT, ts TEXT, temp REAL, hum REAL, pres REAL, light REAL)")
lock = threading.Lock()

class Service(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_POST(self):                                   # POST /nodes/<id>/readings
        parts = self.path.strip("/").split("/")
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if len(parts) != 3 or parts[2] != "readings": return self._send(404, {"error": "not found"})
        with lock:
            db.execute("INSERT INTO readings VALUES (?,?,?,?,?,?)", (parts[1], data["ts"], data["temp"], data["hum"], data["pres"], data["light"]))
        alert = "possible frost" if data["temp"] < 2 else None   # rule evaluated in the cloud
        self._send(201, {"stored": True, "alert": alert})
    def do_GET(self):                                    # GET /nodes/<id>/summary
        parts = self.path.strip("/").split("/")
        if len(parts) == 3 and parts[2] == "summary":
            with lock:
                n, lo, hi, avg = db.execute("SELECT COUNT(*), MIN(temp), MAX(temp), AVG(temp) FROM readings WHERE node=?", (parts[1],)).fetchone()
            return self._send(200, {"node": parts[1], "count": n, "min": lo, "max": hi, "avg": round(avg, 2)})
        self._send(404, {"error": "not found"})

server = HTTPServer(("127.0.0.1", 0), Service)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = "http://127.0.0.1:%d" % server.server_port

def fake_sensor(i):                                      # stands in for DHT22 / BMP280 / BH1750 drivers
    temps = [6.5, 4.0, 2.5, 1.2, 0.4, 3.0]
    return {"ts": "2026-01-15T0%d:00:00Z" % i, "temp": temps[i], "hum": 80 - i, "pres": 856.0 - 0.2 * i, "light": 0 if i < 4 else 120 * i}

def call(method, path, body=None):
    req = urllib.request.Request(base + path, data=json.dumps(body).encode() if body else None, method=method,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return r.status, json.loads(r.read())

for i in range(6):                                       # the controller service loop (interval skipped here)
    code, reply = call("POST", "/nodes/ktm-07/readings", fake_sensor(i))
    print("POST reading %d -> %d %s" % (i, code, reply))
print("GET summary ->", call("GET", "/nodes/ktm-07/summary"))
server.shutdown()
```
```output
POST reading 0 -> 201 {'stored': True, 'alert': None}
POST reading 1 -> 201 {'stored': True, 'alert': None}
POST reading 2 -> 201 {'stored': True, 'alert': None}
POST reading 3 -> 201 {'stored': True, 'alert': 'possible frost'}
POST reading 4 -> 201 {'stored': True, 'alert': 'possible frost'}
POST reading 5 -> 201 {'stored': True, 'alert': None}
GET summary -> (200, {'node': 'ktm-07', 'count': 6, 'min': 0.4, 'max': 6.5, 'avg': 2.93})
```
::: note What the program shows
The node never touches the database; it only calls the service. That separation lets the same service accept data from any number of nodes (level 6), lets the rules change in one place, and allows authentication to be added at the service entry (a missing key returns 401). Real deployments add HTTPS, an API key per node, input validation and a proper server (gunicorn or a PaaS).
:::

## 3.10 Step 10: Application development

The last step builds the **application**: the dashboard and mobile interface used by people. For the weather monitor, the application provides:

- a **current conditions** panel for every node (latest temperature, humidity, pressure, light and time);
- **history charts** (line charts over the last day, week and month);
- **alerts** (frost, storm warning when pressure falls sharply, sensor offline);
- an **admin view** to register nodes, change the sampling interval and check the firmware version;
- **login**, with different rights for viewers and administrators.

A browser dashboard asks the REST service for JSON and draws charts; for live updates it can use a WebSocket (exclusive pair) or poll every few seconds. The following program renders a text dashboard from a list of readings, the same transformation a chart library applies.

```python
readings = [("06:00", 6.5, 80, 856.0), ("07:00", 4.0, 79, 855.8), ("08:00", 2.5, 78, 855.6),
            ("09:00", 1.2, 77, 855.4), ("10:00", 0.4, 76, 855.2), ("11:00", 3.0, 75, 855.0)]
lo, hi = min(r[1] for r in readings), max(r[1] for r in readings)
print("node ktm-07   temperature (degC)     min %.1f  max %.1f  avg %.2f" % (lo, hi, sum(r[1] for r in readings) / len(readings)))
for t, temp, hum, pres in readings:
    bar = "#" * int(round(temp * 4))
    flag = "  <- FROST ALERT" if temp < 2 else ""
    print("%s  %4.1f  %-26s%s" % (t, temp, bar, flag))
trend = readings[-1][3] - readings[0][3]
print("pressure change over 5 h: %+.1f hPa -> %s" % (trend, "falling slowly" if trend < 0 else "rising"))
```
```output
node ktm-07   temperature (degC)     min 0.4  max 6.5  avg 2.93
06:00   6.5  ##########################
07:00   4.0  ################          
08:00   2.5  ##########                
09:00   1.2  #####                       <- FROST ALERT
10:00   0.4  ##                          <- FROST ALERT
11:00   3.0  ############              
pressure change over 5 h: -1.0 hPa -> falling slowly
```

## 3.11 Summary and exercises

The methodology moves from **purpose and requirements** through **process**, **domain**, **information** and **service** models to the **IoT level**, the **functional** and **operational views**, **integration** and the **application**. The weather monitor is a level 6 system: independent nodes with four sensors and a controller service publish over HTTPS to a cloud web service that stores, analyses and serves the dashboard, and the cloud sends configuration back.

1. List the ten steps of the IoT platform design methodology and the output of each.
2. State the five groups of requirements and write one requirement of each group for a weather monitoring system.
3. Draw the process specification of the weather monitor.
4. Define physical entity, virtual entity, device, resource and service, and draw the domain model of the weather monitor.
5. What is an information model? Give the attributes of the weather station entity with units.
6. Write the service specification of the weather monitor (controller service and web service).
7. Why is the weather monitor level 6 and not level 5? What changes if there is only one node?
8. Differentiate the functional view and the operational view with examples.
9. For 200 nodes sending a 150-byte reading every 5 minutes, find the messages per day and the payload per year.
10. A frost alert fires when temperature falls below 2 degrees C. Suggest two improvements to avoid false alarms and one reason for each.
11. Choose the hardware, protocol and cloud components for a river-level monitoring system and justify each.
12. Draw the operational view of a smart parking system after applying the ten steps in outline.

**Answers to the numerical items.** (9) Per node $24\times60/5=288$ messages a day, so $288\times200=57{,}600$ messages a day; payload per day $=57{,}600\times150=8.64$ MB; per year $=8.64\times365=3.15$ GB.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the domain model and information model of the weather monitoring system.**

The domain model names the entities and relations: the physical entity is the environment at a site; the virtual entity "Weather at site 7" represents it; the device (end node) monitors the physical entity; resources (four sensors and their drivers) are hosted on the device; services (controller service and web service) expose the resources. The information model describes the virtual entity's attributes: `node_id` (text), `timestamp` (UTC), `temperature` (degrees C), `humidity` (percent), `pressure` (hPa) and `light` (lux), with one station having many readings over time. The domain model shows **what exists and how it is related**; the information model shows **what is known about the entity**.

**Q2 (5 marks). Specify the services of the weather monitor.**

Controller service: runs on the node as a native service; input is the sensor values read every 60 seconds; it formats a JSON message with node ID and timestamp, publishes it to the web service and retries after failure. Web service: a REST service in the cloud; `POST /nodes/{id}/readings` stores a reading (201), `GET /nodes/{id}/readings?last=10` returns recent data (200), `GET /nodes/{id}/summary` returns minimum, maximum and average, and `PUT /nodes/{id}/config` changes the interval. It writes to the database, evaluates alert rules and serves the dashboard.

**Q3 (10 marks). Describe the IoT platform design methodology and apply it to a weather monitoring system.**

*Introduction.* Building an IoT system needs a method so that purpose, entities, data, services and deployment are decided in order. The ten-step methodology of Bahga and Madisetti provides it.

*Steps.* (1) Purpose and requirements: behaviour, management, analysis, deployment, security. (2) Process specification: the use-case flow (Figure 3.1). (3) Domain model (Figure 3.2). (4) Information model: attributes of the station. (5) Service specification: controller and web service. (6) Level: level 6. (7) Functional view: the six functional groups. (8) Operational view: devices, protocols, cloud, database (Figure 3.3). (9) Integration: wiring sensors to the board, connecting the node to the service, sizing the data. (10) Application: dashboard, alerts, admin and login.

*Example.* Fifty nodes sampling every minute send 72,000 messages a day, about 3.15 GB a year at 120 bytes each; HTTP headers raise this to about 11 GB, so MQTT would be considered if data volume or battery life matter.

*Conclusion.* The methodology keeps the design independent of products until the operational view, which makes it easier to change hardware or cloud later.

**Q4 (10 marks). Explain the functional and operational views with the weather monitor as the case, and explain why the system is level 6.**

*Functional view.* Groups the functions into device (sensors, board), communication (Wi-Fi, HTTP or MQTT), services (controller, web), management (status, configuration), security (authentication, TLS) and application (dashboard, alerts).

*Operational view.* Chooses where and how: Raspberry Pi or ESP32 with DHT22 or BME280 and BH1750, Wi-Fi, HTTPS REST, Python web service on a cloud server, a database, a web dashboard, and per-node keys.

*Level.* Many independent nodes, cloud storage, cloud analysis, cloud application and a centralised controller that pushes configuration: level 6. Level 5 would need a coordinator node, which is unnecessary when each node reaches the Internet itself.

*Conclusion.* The functional view answers "what must exist" and the operational view answers "what runs where"; level 6 follows from the many-node, cloud-centred requirements.
