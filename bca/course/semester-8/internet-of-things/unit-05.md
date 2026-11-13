---
subject: Internet of Things
grade: BCA Semester 8 (Elective IV)
unit: 5
title: IoT Physical Servers and Cloud Offering
hours: 3
area: BCA 454 · Internet of Things · Unit 5
---

A sensor node has kilobytes of memory and a battery. It cannot keep a year of history, draw charts for ten thousand users or run a model that needs gigabytes. Those jobs move to **servers**: a Raspberry Pi in the farm office, a rack in a company data centre, or machines rented from a cloud provider. This short unit (3 hours in the outline) covers the **cloud storage models** and the **communication APIs** through which IoT devices reach them.

::: key What this unit gives you
- Physical servers for IoT, from a local Raspberry Pi to cloud data centres, and the service models IaaS, PaaS and SaaS.
- Cloud storage models: object, block, file, relational, NoSQL and time-series, and how to choose.
- Communication APIs: REST, WebSocket, MQTT and CoAP, with runnable examples (a topic matcher and a REST resource).
- A comparison of IoT cloud platforms and a checklist for choosing one.
:::

## 5.1 IoT physical servers

A **physical server** is the machine that runs the services of Unit 3 (the web service, the broker, the database). Four placements are common:

| Placement | Example | Strengths | Weaknesses |
|---|---|---|---|
| **Local gateway or mini server** | Raspberry Pi running an MQTT broker and a small database | Works without Internet, low latency, cheap, data stay on site | Limited power and storage, one disk to fail, you manage it |
| **On-premises server** | A server in the company's room or data centre | Full control, compliance, existing staff | Capital cost, power, cooling, backups |
| **Co-location / hosting** | A rented server in a provider's data centre | Better power and network, you keep control of the machine | Still maintain the software |
| **Cloud** | Virtual machines or managed services from AWS, Azure, Google Cloud or a local provider | Elastic, pay as you use, global, managed security patches | Recurring cost, dependence on the provider, data location |

Hybrid designs are normal: the farm gateway keeps working locally and **synchronises** with the cloud when the connection allows. **Containers** (Docker) package a service with its dependencies so that the same image runs on a Pi, a laptop or a cloud server; **Kubernetes** orchestrates many containers.

**Cloud service models** (the "as a service" ladder):

| Model | You manage | Provider manages | IoT example |
|---|---|---|---|
| **IaaS** (infrastructure) | OS, runtime, application, data | Servers, storage, network (virtualised) | Rent a virtual machine and install your own broker and database |
| **PaaS** (platform) | Application and data | Everything below, including runtime and scaling | Deploy a Django or Node.js service on a platform; managed database |
| **SaaS** (software) | Only your use of it | The whole application | A ready-made IoT dashboard service |

**Deployment models:** **public** cloud (shared, provider-owned), **private** (dedicated to one organisation), **hybrid** (both, connected), and **community**.

## 5.2 Cloud storage models for IoT data

IoT data differs in kind, so one store is rarely enough.

| Storage model | What it holds | Strengths | IoT use |
|---|---|---|---|
| **Object storage** (Amazon S3, Google Cloud Storage, Azure Blob) | Files as objects with metadata, addressed by key and URL | Cheap, almost unlimited, durable (copies in several places) | Camera images, firmware files, raw log archives |
| **Block storage** (virtual disks) | Raw volumes attached to a server | Fast, behaves like a local disk | A database server's disk |
| **File storage** (shared file systems, NFS) | Directory tree shared among servers | Familiar, shared access | Shared configuration or exports |
| **Relational database** (MySQL, PostgreSQL) | Tables with schema, SQL, transactions | Strong consistency, joins | Device registry, users, billing |
| **NoSQL** (MongoDB, Cassandra, DynamoDB) | Documents, key-values or wide columns | Scale out, flexible schema | Device state, event logs |
| **Time-series database** (InfluxDB, TimescaleDB) | Time-stamped measurements | Fast writes, downsampling, retention policies | Sensor readings |

**A typical IoT layout** uses several at once: the **latest state** of each device in a key-value store, the **history** in a time-series database, **images and firmware** in object storage and **users and device records** in a relational database. **Data lifecycle**: hot data (last days, fast storage), warm (months, cheaper) and cold (years, archive storage); old readings are **downsampled**, for example from one-second values to one-minute averages.

**Choosing storage: questions to ask.** How fast does data arrive and how long is it kept? Is the schema fixed? Are joins and transactions needed? Is it read mostly by time range? What are the costs of storage and of reading it back? Where may the data legally be stored?

::: example Sizing the storage of a smart-meter project
20,000 meters each send a 100-byte reading every 15 minutes. Readings per day $=20{,}000\times96=1{,}920{,}000$; bytes per day $=192$ MB; per year $=70$ GB raw. With database overhead and indexes of about three times, about 210 GB a year; keeping 15-minute data for 2 years and then hourly averages (a factor of 4) for 5 more years bounds the total near 700 GB. A time-series database with compression would use much less. The numbers come from a few lines of arithmetic, which is how a budget is justified.
:::

```python
meters, bytes_per_reading, per_day = 20_000, 100, 24 * 4
daily = meters * per_day * bytes_per_reading
print("readings per day: %d" % (meters * per_day))
print("raw per day: %.0f MB, per year: %.1f GB" % (daily / 1e6, daily * 365 / 1e9))
with_overhead = daily * 365 * 3 / 1e9
print("with 3x overhead per year: %.0f GB" % with_overhead)
hourly_factor = 4
total = 2 * with_overhead + 5 * with_overhead / hourly_factor
print("2 years of 15-min data + 5 years hourly: %.0f GB" % total)
# storage tiers: price per GB-month (illustrative figures, check provider price lists)
tiers = {"hot (SSD)": 0.10, "standard object": 0.023, "archive": 0.004}
for name, price in tiers.items():
    print("%-16s 1000 GB for a month = $%.2f" % (name, 1000 * price))
```
```output
readings per day: 1920000
raw per day: 192 MB, per year: 70.1 GB
with 3x overhead per year: 210 GB
2 years of 15-min data + 5 years hourly: 683 GB
hot (SSD)        1000 GB for a month = $100.00
standard object  1000 GB for a month = $23.00
archive          1000 GB for a month = $4.00
```
```svgfig label="5.1" caption="One IoT platform, several stores. Devices send readings through the API layer; the platform writes state to a key-value store, history to a time-series database, images and firmware to object storage and device records to a relational database."
f = Fig(640, 250)
f.box(10, 100, 100, 50, "Devices and\ngateways", fill=BLUE, stroke=NAVY, size=10)
f.box(150, 100, 110, 50, "API layer\nREST / MQTT", fill=SAND, stroke=AMBER, size=10)
stores = [("Key-value\nlatest state", 20), ("Time-series DB\nhistory", 80), ("Object storage\nimages, firmware", 140), ("Relational DB\ndevices, users", 200)]
for label, y in stores:
    f.box(340, y - 10, 150, 46, label, fill=MINT, stroke=TEAL, size=10)
    f.arrow([(260, 125), (340, y + 13)], color=NAVY)
f.box(530, 100, 100, 50, "Dashboard,\nanalytics", fill=BLUE, stroke=NAVY, size=10)
for label, y in stores:
    f.arrow([(490, y + 13), (530, 125)], color=TEAL)
f.arrow([(110, 125), (150, 125)], color=NAVY, both=True)
```

## 5.3 Communication APIs of IoT systems

An **API (application programming interface)** is the agreed way for one program to talk to another. IoT systems use four main kinds.

**REST over HTTP(S).** Resources are named by URLs and handled by the HTTP methods.

| Method | Use | Idempotent? | Typical status codes |
|---|---|---|---|
| `GET` | Read a resource | Yes | 200 OK, 404 Not Found |
| `POST` | Create a resource or send a reading | No | 201 Created, 400 Bad Request |
| `PUT` | Replace or update a resource | Yes | 200 OK, 204 No Content |
| `DELETE` | Remove a resource | Yes | 204 No Content, 404 |

Good REST design uses **nouns** in paths (`/devices/ktm-07/readings`), JSON bodies, correct status codes, **authentication** (API key in a header, or tokens) and HTTPS. Its drawbacks for IoT are the text headers (hundreds of bytes per request) and that the server cannot call the device (the device must poll).

**WebSocket.** The client sends an HTTP request asking to **upgrade**; the server answers `101 Switching Protocols` and the connection stays open for **two-way** messages in small frames. In the handshake the client sends a random `Sec-WebSocket-Key`; the server returns `Sec-WebSocket-Accept`, the base64 of the SHA-1 of the key joined with a fixed GUID, which proves it understood the protocol. Used for live dashboards and for pushing commands to a device.

**MQTT (Message Queuing Telemetry Transport).** A publish-subscribe protocol over TCP (port 1883, 8883 with TLS), designed for constrained devices and bad networks.

- **Broker and clients.** Clients **publish** to topics and **subscribe** to topics through a broker (Mosquitto, EMQX, HiveMQ, or the cloud services' brokers).
- **Topics** are `/`-separated strings, for example `farm/field1/soil/moisture`. Subscribers use wildcards: `+` matches **one level** (`farm/+/soil/moisture`), `#` matches **all remaining levels** and must be last (`farm/#`).
- **QoS (quality of service).** QoS 0 is *at most once* (fire and forget), QoS 1 is *at least once* (acknowledged, duplicates possible), QoS 2 is *exactly once* (four-step handshake, slowest).
- **Retained message.** The broker keeps the last message of a topic and gives it to new subscribers at once (the current state).
- **Last Will and Testament (LWT).** A message the broker publishes if a client disappears without a clean disconnect, so a dashboard learns that a device went offline.
- **Keep-alive** and **clean/persistent sessions** let devices sleep and reconnect without losing subscriptions. Fixed header can be only 2 bytes, so a small reading costs little.

**CoAP (Constrained Application Protocol).** A RESTful protocol over **UDP** (port 5683) with the same methods as HTTP in a compact binary format (4-byte header), optional reliability (confirmable messages with retransmission), **observe** (subscribe to changes of a resource) and discovery. It suits very constrained nodes and maps easily to HTTP through a proxy.

| Protocol | Transport | Pattern | Header | Best for |
|---|---|---|---|---|
| HTTP/REST | TCP | Request-response | Hundreds of bytes | Web and mobile apps, configuration, occasional uploads |
| WebSocket | TCP | Exclusive pair, full duplex | 2 to 14 bytes per frame | Live dashboards, instant commands |
| MQTT | TCP | Publish-subscribe via broker | 2 bytes minimum | Telemetry from many devices; unreliable links |
| CoAP | UDP | Request-response, observe | 4 bytes | Very constrained nodes, local networks |

```python
def topic_matches(subscription, topic):
    """MQTT wildcard matching: '+' = one level, '#' = all remaining levels (must be last)."""
    s, t = subscription.split("/"), topic.split("/")
    for i, part in enumerate(s):
        if part == "#":
            return i == len(s) - 1
        if i >= len(t):
            return False
        if part != "+" and part != t[i]:
            return False
    return len(s) == len(t)

tests = [("farm/+/soil/moisture", "farm/field1/soil/moisture"), ("farm/+/soil/moisture", "farm/field1/air/temp"),
         ("farm/#", "farm/field1/soil/moisture"), ("farm/#", "farm"), ("farm/+", "farm/field1/soil"),
         ("+/field1/#", "farm/field1/air/temp"), ("farm/field1", "farm/field1/soil")]
for sub, topic in tests:
    print("%-22s vs %-28s -> %s" % (sub, topic, topic_matches(sub, topic)))
```
```output
farm/+/soil/moisture   vs farm/field1/soil/moisture    -> True
farm/+/soil/moisture   vs farm/field1/air/temp         -> False
farm/#                 vs farm/field1/soil/moisture    -> True
farm/#                 vs farm                         -> True
farm/+                 vs farm/field1/soil             -> False
+/field1/#             vs farm/field1/air/temp         -> True
farm/field1            vs farm/field1/soil             -> False
```
```python
import base64, hashlib
# WebSocket handshake check using the example key of RFC 6455
key = "dGhlIHNhbXBsZSBub25jZQ=="
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
accept = base64.b64encode(hashlib.sha1((key + GUID).encode()).digest()).decode()
print("Sec-WebSocket-Accept:", accept)

# Size of one MQTT 3.1.1 PUBLISH packet at QoS 0 versus an HTTP POST carrying the same reading
topic, payload = "farm/field1/soil/moisture", b'{"v":23.5}'
remaining = 2 + len(topic) + len(payload)            # 2-byte topic length + topic + payload (no packet id at QoS 0)
mqtt_bytes = 1 + 1 + remaining                       # fixed header byte + 1-byte remaining length + body
http = ("POST /api/readings HTTP/1.1\r\nHost: iot.example.com\r\nContent-Type: application/json\r\n"
        "Authorization: Bearer abcdef0123456789\r\nContent-Length: %d\r\n\r\n" % len(payload)).encode() + payload
print("payload %d bytes; MQTT packet %d bytes; HTTP request about %d bytes" % (len(payload), mqtt_bytes, len(http)))
print("ratio HTTP/MQTT = %.1f" % (len(http) / mqtt_bytes))
```
```output
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
payload 10 bytes; MQTT packet 39 bytes; HTTP request about 156 bytes
ratio HTTP/MQTT = 4.0
```
**A REST resource in practice.** The next program models a REST API for devices in memory, with status codes, so that each method and code can be seen. (Unit 3, Section 3.9 ran a real HTTP server; here the focus is on API design.)

```python
devices = {}
def api(method, path, body=None):
    parts = path.strip("/").split("/")
    if parts[0] != "devices": return 404, {"error": "no such resource"}
    if method == "POST" and len(parts) == 1:
        if not body or "id" not in body: return 400, {"error": "id required"}
        if body["id"] in devices: return 409, {"error": "already exists"}
        devices[body["id"]] = {"id": body["id"], "interval": body.get("interval", 60)}
        return 201, devices[body["id"]]
    if len(parts) == 2:
        d = devices.get(parts[1])
        if d is None: return 404, {"error": "device not found"}
        if method == "GET": return 200, d
        if method == "PUT": d.update(body); return 200, d
        if method == "DELETE": del devices[parts[1]]; return 204, None
    return 405, {"error": "method not allowed"}

for call in [("POST", "/devices", {"id": "ktm-07"}), ("POST", "/devices", {"id": "ktm-07"}), ("POST", "/devices", {}),
             ("GET", "/devices/ktm-07", None), ("PUT", "/devices/ktm-07", {"interval": 15}),
             ("GET", "/devices/pkr-02", None), ("DELETE", "/devices/ktm-07", None), ("GET", "/devices/ktm-07", None)]:
    print("%-6s %-16s -> %s" % (call[0], call[1], api(*call)))
```
```output
POST   /devices         -> (201, {'id': 'ktm-07', 'interval': 60})
POST   /devices         -> (409, {'error': 'already exists'})
POST   /devices         -> (400, {'error': 'id required'})
GET    /devices/ktm-07  -> (200, {'id': 'ktm-07', 'interval': 60})
PUT    /devices/ktm-07  -> (200, {'id': 'ktm-07', 'interval': 15})
GET    /devices/pkr-02  -> (404, {'error': 'device not found'})
DELETE /devices/ktm-07  -> (204, None)
GET    /devices/ktm-07  -> (404, {'error': 'device not found'})
```

## 5.4 IoT cloud platforms

An **IoT cloud platform** bundles what Units 3 and 5 described: device registration and identity, secure connection (MQTT, HTTP), a message broker, rules that route data, storage, dashboards and device management with remote updates.

| Platform | Style | Notes |
|---|---|---|
| **AWS IoT Core** | Managed broker with registry | A **thing** is registered with an X.509 **certificate** and a **policy** that lists allowed topics; a **device shadow** stores each device's last reported and desired state, so a command can wait for a sleeping device; **rules** (SQL-like) route messages to storage, functions or other services |
| **Azure IoT Hub** | Managed hub with device identities | Device-to-cloud and cloud-to-device messages, **device twins** (like shadows), message routing, connects to Azure analytics services |
| **Google Cloud IoT Core** | Managed broker | **Retired by Google in August 2023**; designs built on it move to a partner platform or to a self-managed broker. A useful lesson on provider dependence. |
| **ThingSpeak** | Simple REST and MQTT service for makers and teaching | A **channel** with up to 8 fields; the update endpoint writes values with a **write API key**; built-in charts and MATLAB analysis; free tier with a minimum update interval (15 seconds) |
| **ThingsBoard, Node-RED, Home Assistant** | Open source, self-hosted | Full control and no per-message charges; you run and secure the server |
| **Blynk, Adafruit IO** | App-centred services | Quick mobile dashboards for prototypes |

A **device shadow** or **twin** is a good example of cloud design for IoT: the cloud holds a JSON document with the *reported* state (from the device) and the *desired* state (from the app). When the device connects, it reads the difference and acts. The dashboard never talks to the sleeping device, only to the document.

```python
# noexec
# ThingSpeak: send one reading from a Raspberry Pi or PC (needs a real channel write key and Internet access)
import requests
WRITE_KEY = "XXXXXXXXXXXXXXXX"               # from the channel's API Keys tab
r = requests.get("https://api.thingspeak.com/update",
                 params={"api_key": WRITE_KEY, "field1": 24.5, "field2": 61})
print("entry id:", r.text)                    # 0 means the update failed (for example, rate limit)
```
```python
import json
# Device shadow logic: the cloud keeps reported and desired state; the device applies the difference when it wakes
shadow = {"reported": {"interval": 60, "fw": "1.2.0"}, "desired": {"interval": 60, "fw": "1.2.0"}}
def app_sets_desired(**changes): shadow["desired"].update(changes)
def device_wakes():
    delta = {k: v for k, v in shadow["desired"].items() if shadow["reported"].get(k) != v}
    for k, v in delta.items():
        shadow["reported"][k] = v                    # the device applies the change and reports back
    return delta
app_sets_desired(interval=15)                        # the app acts while the device sleeps
app_sets_desired(fw="1.3.0")
print("shadow before wake:", json.dumps(shadow))
print("delta applied by device:", device_wakes())
print("shadow after wake :", json.dumps(shadow))
print("delta on the next wake:", device_wakes())
```
```output
shadow before wake: {"reported": {"interval": 60, "fw": "1.2.0"}, "desired": {"interval": 15, "fw": "1.3.0"}}
delta applied by device: {'interval': 15, 'fw': '1.3.0'}
shadow after wake : {"reported": {"interval": 15, "fw": "1.3.0"}, "desired": {"interval": 15, "fw": "1.3.0"}}
delta on the next wake: {}
```
**Choosing a platform.** Check: supported protocols and device SDKs; per-message and storage pricing (calculate for your device count and interval); security features (per-device certificates, policies, secrets rotation); device management (updates, groups, shadows); regions and data-location law; export of data and **lock-in** (can you move to another provider?); and support. For a student project, ThingSpeak or a self-hosted Mosquitto with Node-RED is enough; for a commercial product, a managed service with per-device identity.

::: caution Cost surprises
Cloud IoT is billed per message, per connection-minute, per GB stored and per rule action. A free tier can vanish when 1,000 devices send every second. Always estimate $\text{devices}\times\text{messages per day}\times\text{price}$ before choosing an interval, and use the edge techniques of Unit 4 (windows, deadbands) to cut it.
:::

```python
devices, interval_s = 1_000, 10
msgs_month = devices * (86_400 // interval_s) * 30
price_per_million = 1.00                              # assumed price in dollars per million messages
print("messages per month: %.1f million" % (msgs_month / 1e6))
print("cost at $%.2f per million: $%.0f" % (price_per_million, msgs_month / 1e6 * price_per_million))
for new_interval in (60, 300):
    m = devices * (86_400 // new_interval) * 30
    print("interval %3d s: %.1f million msgs, $%.2f" % (new_interval, m / 1e6, m / 1e6 * price_per_million))
```
```output
messages per month: 259.2 million
cost at $1.00 per million: $259
interval  60 s: 43.2 million msgs, $43.20
interval 300 s: 8.6 million msgs, $8.64
```
## 5.5 Summary and exercises

Servers for IoT range from a local Raspberry Pi to cloud data centres; IaaS, PaaS and SaaS divide the work between provider and user. IoT data needs several stores: object storage for files, time-series databases for readings, key-value or document stores for state and relational databases for records. Devices reach servers through REST (simple, heavy), WebSocket (two-way), MQTT (publish-subscribe, light, QoS 0 to 2, retained messages, last will) and CoAP (UDP). Platforms such as AWS IoT Core, Azure IoT Hub and ThingSpeak add identity, rules, shadows and dashboards; choose by protocol, cost, security, management and lock-in.

1. Compare local, on-premises, hosted and cloud servers for an IoT project.
2. Distinguish IaaS, PaaS and SaaS with an IoT example each. Name the cloud deployment models.
3. Compare object, block and file storage, and explain why time-series databases suit sensor data.
4. 5,000 devices send 200-byte readings every 5 minutes. Find the data per day and per year.
5. Explain REST with the four methods and status codes. Why is HTTP heavy for constrained devices?
6. Explain MQTT: broker, topics, wildcards, the three QoS levels, retained messages and last will.
7. Does the subscription `home/+/temp` match `home/kitchen/temp`, `home/kitchen/oven/temp` and `home/temp`? Does `home/#` match all three?
8. Compare MQTT, CoAP, HTTP and WebSocket in a table.
9. What is a device shadow and why is it useful for sleeping devices?
10. List six criteria for choosing an IoT cloud platform. What happened to Google Cloud IoT Core and what does it teach?
11. 800 devices publish every 20 seconds at USD 0.80 per million messages. Find the monthly cost and the cost if the interval becomes 2 minutes.
12. Explain how a WebSocket connection is established.

**Answers to the numerical items.** (4) $24\times12=288$ readings per device per day; $5000\times288=1{,}440{,}000$ readings; $\times200$ bytes $=288$ MB per day; $\times365=105$ GB per year. (7) `home/+/temp` matches `home/kitchen/temp` only; `home/kitchen/oven/temp` has an extra level and `home/temp` lacks the middle level. `home/#` matches all three. (11) $800\times(86400/20)\times30=103.68$ million messages, cost $=0.8\times103.68=82.94$ USD; at 120 s: $800\times720\times30=17.28$ million, cost $=0.8\times17.28=13.82$ USD.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the MQTT protocol.**

MQTT is a lightweight publish-subscribe protocol over TCP for constrained devices. Clients publish messages to hierarchical topics (`farm/field1/soil/moisture`) at a broker, which forwards them to every client subscribed to a matching topic; `+` matches one level and `#` the rest. Three QoS levels: 0 at most once, 1 at least once, 2 exactly once. A retained message gives new subscribers the last value; the last will is published if a client vanishes; the header is as small as 2 bytes. A 10-byte reading with this topic needs 39 bytes in MQTT against about 156 bytes in an HTTP request.

**Q2 (5 marks). Compare REST and WebSocket.**

REST is request-response over HTTP: stateless, simple, cacheable, resource-oriented with methods GET, POST, PUT and DELETE, but each request carries headers and the server cannot start a message. WebSocket upgrades an HTTP connection to a persistent two-way channel with 2 to 14 byte frame headers, so either side can send at any time with little overhead. Use REST for configuration and occasional queries; use WebSocket for live dashboards and instant control commands.

**Q3 (10 marks). Describe the cloud storage models for IoT data and design the storage of a smart-meter project.**

*Introduction.* IoT data are of different kinds (readings, state, files, records) with different needs, so several storage models are combined.

*Models.* Object storage (S3-like) for images, firmware and archives; block storage for database disks; file storage for shared files; relational databases for registry and billing; NoSQL (key-value, document, column) for state and logs; time-series databases for readings with compression and retention.

*Design.* 20,000 meters, 100 bytes every 15 minutes: 1.92 million readings and 192 MB a day, about 70 GB a year raw and 210 GB with overhead. Store the latest value per meter in a key-value store, the history in a time-series database (15-minute data for 2 years, then hourly averages), meter records and customers in a relational database and firmware in object storage. Data move from hot to warm to cold tiers.

*Conclusion.* Matching each kind of data to the right store reduces cost and keeps queries fast; sizing by arithmetic justifies the budget.

**Q4 (10 marks). Describe the communication APIs of IoT and the choice of a cloud platform.**

*Introduction.* Devices and applications reach servers through APIs; the choice depends on device power, network and pattern of use.

*APIs.* REST over HTTPS for create, read, update and delete of resources, with proper status codes (201, 404, 409); WebSocket for persistent two-way channels (handshake with `Sec-WebSocket-Key` and `Sec-WebSocket-Accept`); MQTT for publish-subscribe telemetry with QoS and retained messages; CoAP for UDP-based constrained devices with observe.

*Platforms.* AWS IoT Core (thing, certificate, policy, shadow, rules), Azure IoT Hub (device twins, routing), ThingSpeak (channels, write key), open-source ThingsBoard and Node-RED. Google Cloud IoT Core was retired in 2023, a reminder to avoid lock-in.

*Criteria.* Protocols and SDKs, price per message and storage (compute it: 1,000 devices at 10-second intervals send 259 million messages a month), security and per-device identity, device management and shadows, regions and law, and data export.

*Conclusion.* Choose the lightest API that satisfies the pattern (MQTT for telemetry, REST for management, WebSocket for live views) and a platform whose cost and exit options are understood before the first device is deployed.
