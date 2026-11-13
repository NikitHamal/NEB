---
subject: Internet of Things
grade: BCA Semester 8 (Elective IV)
unit: 1
title: Introduction to IoT
hours: 8
area: BCA 454 · Internet of Things · Unit 1
---

A water tank on a hill in Pokhara has a float switch, a small board and a SIM card. When the level drops below 20 percent the board sends a message, and a pump in the valley starts without anyone climbing the hill. Nothing in this story is a computer in the usual sense, yet the tank is **online**, it **senses**, it **reports** and a remote system **acts** on the report. That loop is the **Internet of Things (IoT)**. This unit defines it, shows its physical and logical structure, and surveys the technologies, protocols and application domains that the rest of the course builds on.

::: key What this unit gives you
- A definition of IoT and its characteristics, with the difference between a thing, a gateway and the cloud.
- The physical design (devices, protocols) and logical design (six functional blocks, communication models and APIs).
- The enabling technologies and the six IoT deployment levels.
- IoT versus M2M, and the nine application domains named in the TU outline.
:::

## 1.1 Definition and characteristics of IoT

The **Internet of Things** is a network of physical objects ("things") that carry sensors, actuators, processing and a network connection, so that they can collect data about the world, exchange it with other things and services over the Internet, and be monitored or controlled remotely. A thing can be a temperature probe, a smart meter, a tractor, a pacemaker or a street lamp. What makes it an IoT thing is a **unique identity** (an address or ID), a **way of sensing or acting**, and **connectivity**.

The idea is older than the name. Kevin Ashton used the phrase "Internet of Things" in 1999 while working on RFID-tagged supply chains at Procter and Gamble, and a networked Coca-Cola vending machine at Carnegie Mellon was reporting its stock over the Internet in the early 1980s. What changed in the 2010s was cost: a Wi-Fi microcontroller module now costs a few dollars, and cloud platforms let a student rent the back end by the hour.

**Characteristics of IoT**

| Characteristic | Meaning | Example |
|---|---|---|
| **Dynamic and self-adapting** | Devices change state (asleep, awake, connected, disconnected), location and context, and the system adapts. | A wearable switches from Bluetooth to Wi-Fi when it reaches home. |
| **Self-configuring** | Devices join the network and set up with little or no human effort. | A new smart bulb is found by the hub and given an address. |
| **Interoperable protocols** | Many communication protocols coexist; things must still exchange data. | A Zigbee sensor and a Wi-Fi camera feed the same dashboard through a gateway. |
| **Unique identity** | Every thing has an identifier (MAC address, IPv6 address, device ID, certificate). | Each smart meter has a serial number registered with the utility. |
| **Integrated into the information network** | Things appear as services and their data joins other data in analytics. | Soil data and weather forecasts are combined to schedule irrigation. |
| **Heterogeneous, constrained and large scale** | Different hardware, tiny memory and power budgets, and very many devices. | A coin-cell sensor with 2 KB of RAM among 100,000 others in a city. |

::: note Constrained devices
Most IoT devices have a tiny share of what a laptop has: kilobytes of RAM, a clock of a few megahertz to tens of megahertz and a battery that must last months. This single fact explains lightweight protocols (MQTT, CoAP), the use of gateways, compact data formats and many security difficulties in Unit 6.
:::

## 1.2 Physical design of IoT

The physical design describes the **things** and how they connect.

1. **Things (devices).** A device has a **sensing** part (sensors), an **acting** part (actuators), a **processing** part (a microcontroller or small computer such as an Arduino or Raspberry Pi), **storage** and a **communication interface** (Wi-Fi, Bluetooth, Zigbee, LoRa, Ethernet, cellular). Devices can exchange data with each other directly, with a **gateway**, or with the cloud.
2. **Gateways.** A gateway links devices that speak local protocols (BLE, Zigbee, Modbus) to the Internet. It translates protocols, aggregates and filters data, sometimes runs local rules (edge processing), and often provides the security boundary. The home Wi-Fi router with a smart-home hub plays this role.
3. **Network and protocols.** Link layer: IEEE 802.3 Ethernet, 802.11 Wi-Fi, 802.15.4 (the base of Zigbee, Thread and 6LoWPAN), Bluetooth Low Energy, LoRaWAN, cellular (NB-IoT, LTE-M). Network layer: IPv4, IPv6 and 6LoWPAN, which compresses IPv6 headers so that they fit the 127-byte frame of 802.15.4. Transport: TCP and UDP. Application: HTTP, WebSocket, MQTT, CoAP, AMQP.
4. **Cloud and applications.** Data storage, analytics, rules and dashboards run on cloud servers; users see them in web and mobile apps.

::: example How many addresses?
IPv4 has $2^{32}\approx 4.3\times10^{9}$ addresses, fewer than the number of IoT devices expected to be deployed, and most are used already. IPv6 has $2^{128}\approx 3.4\times10^{38}$ addresses. Dividing by Earth's surface area of about $5.1\times10^{14}\ \text{m}^2$ gives about $6.7\times10^{23}$ addresses per square metre. This is why IPv6 is the long-term addressing answer for IoT, with NAT and gateways as the bridge in the meantime.
:::

```svgfig label="1.1" caption="Physical design of an IoT system. Things with sensors and actuators talk to a gateway over local links, the gateway talks to the cloud over the Internet, and users see the results in an application."
f = Fig(640, 250)
f.box(10, 20, 120, 46, "Temperature\nsensor node", fill=BLUE, stroke=NAVY, size=10)
f.box(10, 82, 120, 46, "Soil moisture\nnode", fill=BLUE, stroke=NAVY, size=10)
f.box(10, 144, 120, 46, "Pump actuator\n(relay)", fill=MINT, stroke=TEAL, size=10)
f.box(200, 70, 110, 70, "Gateway\nBLE / Zigbee\nto Wi-Fi", fill=SAND, stroke=AMBER, size=10)
f.box(380, 40, 120, 130, "", fill=SOFT, stroke=SLATE)
f.text(440, 58, "Cloud", size=11, color=NAVY, bold=True)
f.box(392, 70, 96, 30, "Storage", fill=BLUE, stroke=NAVY, size=9.5)
f.box(392, 106, 96, 30, "Analytics", fill=BLUE, stroke=NAVY, size=9.5)
f.box(392, 140, 96, 22, "Rules", fill=BLUE, stroke=NAVY, size=9.5)
f.box(550, 85, 80, 46, "Mobile / web\napp", fill=MINT, stroke=TEAL, size=10)
f.arrow([(130, 43), (200, 95)], color=NAVY)
f.arrow([(130, 105), (200, 105)], color=NAVY)
f.arrow([(200, 125), (130, 167)], color=TEAL, dash=True)
f.arrow([(310, 105), (380, 105)], color=NAVY, both=True)
f.arrow([(500, 108), (550, 108)], color=NAVY, both=True)
f.text(165, 215, "local links: BLE, Zigbee, LoRa", size=10, color=SLATE)
f.text(345, 215, "Internet: Wi-Fi, Ethernet, cellular", size=10, color=SLATE)
f.text(590, 215, "users", size=10, color=SLATE)
```

## 1.3 Logical design of IoT

The logical design abstracts the system from the hardware: functional blocks, communication models and APIs. It follows the reference model of Bahga and Madisetti (the course's first text).

**Functional blocks.** Six blocks give a system its services.

| Block | Role | Typical content |
|---|---|---|
| **Device** | Sensing, actuation, monitoring and control | Sensors, actuators, the board and its firmware |
| **Communication** | Handles the links and protocols | Wi-Fi, MQTT client, a TCP/IP stack |
| **Services** | Device modelling, device control, data publishing, device discovery | Cloud service that exposes a device as a REST resource |
| **Management** | Governs the system | Configuration, monitoring, device registry, OTA updates |
| **Security** | Protects data and access | Authentication, authorisation, encryption, key storage |
| **Application** | Interface for control and view of status | Dashboard, mobile app, alerts, analytics screens |

**Communication models.** Four patterns are used.

| Model | How it works | Used when |
|---|---|---|
| **Request-response** | A client sends a request and the server returns a response; stateless. HTTP and REST follow it. | A phone app asks "what is the room temperature now?" |
| **Publish-subscribe** | Publishers send messages to a **topic** at a **broker**; the broker delivers them to all subscribers of that topic. Publishers and subscribers never meet. MQTT follows it. | Many sensors and many consumers; loose coupling |
| **Push-pull** | Producers push data to a queue and consumers pull from it at their own pace; the queue decouples speeds. | A burst of readings must not overwhelm a slow consumer |
| **Exclusive pair** | A persistent, full-duplex connection between exactly two ends; once open, either side sends at any time. WebSocket follows it. | Live dashboards and instant control |

The program below is a tiny in-memory broker. Two subscribers register for topics and one publisher sends three readings; the broker alone knows who receives what.

```python
class Broker:
    def __init__(self):
        self.subs = {}                       # topic -> list of callbacks
    def subscribe(self, topic, callback):
        self.subs.setdefault(topic, []).append(callback)
    def publish(self, topic, payload):
        for cb in self.subs.get(topic, []):  # deliver to every subscriber of the topic
            cb(topic, payload)

broker = Broker()
broker.subscribe("home/hall/temp", lambda t, p: print("dashboard got", t, p))
broker.subscribe("home/hall/temp", lambda t, p: print("alarm check:", "HOT" if p > 30 else "ok"))
broker.subscribe("home/hall/light", lambda t, p: print("logger got", t, p))
for topic, value in [("home/hall/temp", 26.5), ("home/hall/light", 310), ("home/hall/temp", 31.2)]:
    broker.publish(topic, value)
```
```output
dashboard got home/hall/temp 26.5
alarm check: ok
logger got home/hall/light 310
dashboard got home/hall/temp 31.2
alarm check: HOT
```
**Communication APIs.** Two styles expose a device or service.

- **REST (Representational State Transfer).** Resources have URIs (`/api/devices/7/temperature`); the HTTP methods GET, POST, PUT, DELETE read, create, update and remove them; every request carries all the context needed (stateless); responses use JSON. REST is simple and cacheable, but each exchange has a full HTTP header, which is heavy for a battery device.
- **WebSocket.** A client opens an HTTP connection and **upgrades** it to a persistent two-way channel. After the handshake, messages are small frames with a 2 to 14 byte header, and the server can push data without being asked. It suits live dashboards and bi-directional control.

## 1.4 IoT enabling technologies

| Technology | Contribution to IoT |
|---|---|
| **Wireless sensor networks (WSN)** | Many small nodes with sensors and radios form a network (star, tree, mesh) and report to a sink; gives wide, low-cost sensing. |
| **Cloud computing** | Elastic storage, compute and services that devices cannot provide themselves (Unit 5). |
| **Big data analytics** | Store and process the volume, velocity and variety of sensor data (Unit 4). |
| **Embedded systems** | Microcontrollers with firmware that sense, decide and act in real time at low power. |
| **Communication protocols** | The layers of Section 1.2 that make exchange possible. |
| **Short-range identification** | **RFID** (passive tags read at a few centimetres to metres) and **NFC** (13.56 MHz, about 4 cm, used in contactless payment) identify and track objects. |

**The common IoT protocols at a glance**

| Protocol | Layer | Idea | Remark |
|---|---|---|---|
| **MQTT** | Application | Publish-subscribe over TCP via a broker; header as small as 2 bytes; QoS 0, 1, 2 | The most common messaging protocol for telemetry |
| **CoAP** | Application | RESTful request-response over UDP, with GET, POST, PUT, DELETE and optional reliability | Designed for constrained nodes; maps onto HTTP |
| **HTTP / REST** | Application | Request-response over TCP | Familiar and heavy |
| **Zigbee** | Network and above, on 802.15.4 | Low-power mesh, 250 kb/s at 2.4 GHz | Home automation and lighting |
| **Bluetooth Low Energy** | Link | Short range, years on a coin cell | Wearables, beacons |
| **LoRaWAN** | Link | Long range (km), low data rate (bytes per message), unlicensed bands | Agriculture, metering, cities |
| **NB-IoT / LTE-M** | Link | Cellular low-power wide area | Smart meters, trackers |

## 1.5 IoT levels and deployment templates

Bahga and Madisetti describe six **levels** that differ in where processing, storage and the application live.

| Level | Description | Example |
|---|---|---|
| **1** | One node does sensing and actuation; storage, analysis and the app are **local**. | Home automation with a single board |
| **2** | One node; data stored in the **cloud**, analysis and app local or cloud. Used where data is **not big** but must be kept. | Smart irrigation of a small farm |
| **3** | One node; storage, analysis and app all in the **cloud**. Data is big and needs heavy analysis. | Tracking packages |
| **4** | Multiple nodes; **local** analysis, storage and app in the cloud. | Nodes too many for one local server |
| **5** | Multiple end nodes plus a **coordinator**; analysis and storage in the cloud. | Forest-fire detection (nodes report to a coordinator) |
| **6** | Multiple independent end nodes send to the cloud; a **centralised controller** in the cloud acts on actuators and nodes. | Weather-monitoring system |

```svgfig label="1.2" caption="IoT levels. As the level rises, more processing moves from the local device to the cloud, and the number of nodes grows."
f = Fig(640, 190)
heads = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6"]
sub = ["1 node, all local", "1 node, cloud store", "1 node, all cloud", "n nodes, local analysis", "n nodes + coordinator", "n nodes, cloud controller"]
fills = [(BLUE, NAVY), (BLUE, NAVY), (MINT, TEAL), (SAND, AMBER), (SAND, AMBER), (ROSE, RED)]
for i in range(6):
    x = 10 + i * 104
    f.box(x, 20, 96, 34, heads[i], fill=fills[i][0], stroke=fills[i][1], size=11, bold=True)
    f.box(x, 62, 96, 48, sub[i].replace(", ", ",\n", 1), fill=SOFT, stroke=SLATE, size=9.5)
f.arrow([(30, 150), (600, 150)], color=SLATE)
f.text(110, 172, "more local processing", size=10, color=SLATE)
f.text(520, 172, "more cloud processing", size=10, color=SLATE)
```

## 1.6 IoT and M2M

**Machine-to-machine (M2M)** is the older term for devices exchanging data directly, with little human involvement, usually over a cellular or wired link between a device and a **single application** (a vending machine reporting to its operator's server). IoT widens this: devices from many vendors, on the Internet, serving many applications, with analytics and cloud services.

| Aspect | M2M | IoT |
|---|---|---|
| Communication | Point to point, often over cellular or proprietary links | Over the Internet using IP and many protocols |
| Scope | Closed, one application and one operator | Open; many applications use the same data |
| Devices | Homogeneous, same vendor | Heterogeneous |
| Intelligence | Mostly device-level | Cloud analytics, machine learning |
| Standards | Vendor or sector specific (for example, ETSI M2M, Modbus) | Open and IP-based (MQTT, CoAP, REST) |
| Integration | Hardware-centric | Software-centric, web and cloud services |

Two management ideas from the outline's reference book appear here. **SDN (software-defined networking)** separates the control plane (decisions) from the data plane (forwarding) so that the huge, changing IoT traffic can be steered programmatically. **NFV (network function virtualisation)** runs firewalls, load balancers and gateways as software on standard servers. For managing devices, **SNMP** (simple, polling-based, suited to monitoring) is older, and **NETCONF with YANG** gives structured configuration with transactions: YANG models the data, NETCONF installs it. IoT management tools such as LWM2M build on the same ideas for constrained devices.

## 1.7 Domain-specific IoTs

The outline names nine areas. For each, know what is sensed, what is controlled, who benefits and what goes wrong.

| Domain | What is sensed or controlled | Typical IoT level and links | Benefit | Risk or limit |
|---|---|---|---|---|
| **Home automation** | Light, temperature, door and window contacts, motion, smoke; relays for lamps, fans, locks, thermostats | Level 1 to 2; Wi-Fi, Zigbee, BLE | Comfort, energy saving, safety alerts | Insecure cameras and default passwords |
| **Cities (smart city)** | Street lighting, parking occupancy, waste-bin fill level, traffic flow, air quality, water leaks | Level 4 to 6; LoRaWAN, NB-IoT, cellular | Lower cost of services, less congestion | Privacy of citizens, vendor lock-in, maintenance cost |
| **Environment** | Air and water quality, forest-fire smoke and temperature, river level, earthquake and landslide motion | Level 5 to 6; LoRa, satellite, cellular | Early warning for floods and fire | Harsh conditions, power, calibration drift |
| **Energy** | Smart meters, grid load, solar output, battery state, leak detection | Level 3 to 6; PLC, cellular, Zigbee | Demand response, loss detection, remote billing | Grid attacks, data about household habits |
| **Retail** | RFID shelf stock, footfall counters, smart carts, cold-chain temperature | Level 2 to 4; RFID, BLE beacons, Wi-Fi | Stock accuracy, less shrinkage | Tracking of customers |
| **Logistics** | GPS location, container door and shock, refrigerated-truck temperature | Level 3 to 6; GPS with cellular | Visibility of shipments, spoilage alerts | Battery life, coverage gaps |
| **Agriculture** | Soil moisture and pH, leaf wetness, weather, tank level; control of pumps and valves | Level 2 to 6; LoRa, cellular | Water saving, yield | Cost for small farmers, rural coverage |
| **Industry (IIoT)** | Vibration, temperature, current of motors; machine counts; PLC data | Level 4 to 6; Modbus, OPC UA, MQTT | Predictive maintenance, less downtime | Safety-critical, legacy equipment, attacks on plants |
| **Health and lifestyle** | Heart rate, SpO2, steps, glucose, falls, sleep; medication dispensers | Level 2 to 3; BLE to phone to cloud | Remote care, early warning, fitness | Sensitive health data, accuracy, regulation |

::: example Choosing a level for smart irrigation
A farmer has one field with 3 soil-moisture probes and one valve. Data volume is a few bytes a minute, and an Internet outage must not stop watering. A sensible design is **Level 2**: one gateway node reads probes and controls the valve using local rules, and also uploads readings to the cloud for history and for the farmer's phone. If the village had no cellular signal, Level 1 (local display only) would still work. If the farm grew to 200 probes across 40 hectares, Level 5 with a coordinator and cloud analytics would fit better.
:::

::: caution Do not confuse IoT with "anything with Wi-Fi"
A laptop connected to the Internet is a computer, not a thing in the IoT sense. The defining idea is that the object's main job is physical (measure, switch, move) and the network connection serves that job.
:::

```python
# Energy: monthly electricity use of a smart meter, with a time-of-day tariff (illustrative rates)
readings_kwh = {"day": 140.0, "peak": 55.0, "night": 70.0}     # kWh in the month
tariff_rs = {"day": 8.0, "peak": 12.0, "night": 6.0}           # Rs per kWh (assumed)
total_kwh = sum(readings_kwh.values())
bill = sum(readings_kwh[k] * tariff_rs[k] for k in readings_kwh)
print("total kWh:", total_kwh)
print("bill: Rs", bill)
print("average rate: Rs %.2f per kWh" % (bill / total_kwh))
shifted = bill - 15 * (tariff_rs["peak"] - tariff_rs["night"])      # move 15 kWh from peak to night
print("bill after shifting 15 kWh from peak to night: Rs", shifted)
```
```output
total kWh: 265.0
bill: Rs 2200.0
average rate: Rs 8.30 per kWh
bill after shifting 15 kWh from peak to night: Rs 2110.0
```
## 1.8 Summary and exercises

IoT connects uniquely identified, sensing and acting things to networks and cloud services. The physical design has things, gateways, networks and a cloud; the logical design has six functional blocks, four communication models and REST or WebSocket APIs. Enabling technologies are WSN, cloud, big data, embedded systems and communication protocols. Six levels place processing locally or in the cloud. M2M is the closed, point-to-point ancestor of the open IoT, and the nine domains apply the same pattern.

1. Define IoT and list its six characteristics with one example each.
2. Distinguish a thing, a gateway and the cloud in the physical design of IoT.
3. Name the six functional blocks of the logical design and state the role of each.
4. Compare request-response and publish-subscribe. Why is publish-subscribe popular for sensors?
5. Explain REST and WebSocket and say when each is better.
6. Describe IoT level 3 and level 6 with one example each.
7. Distinguish IoT from M2M in at least five points.
8. Explain how IoT is applied in agriculture and in health, naming sensors, links, benefits and risks.
9. Why is IPv6 important for IoT? Show the address count.
10. Explain the role of SDN and NFV in IoT networks.
11. A sensor sends a 6-byte reading every 10 seconds with MQTT, whose smallest header is 2 bytes (ignore the topic). How many bytes of data and header does it send in a day?
12. Which IoT level would you choose for a classroom with 10 temperature nodes and a local display, no cloud? Justify.

**Answers to the numerical items.** (9) $2^{128}\approx3.4\times10^{38}$. (11) 8,640 messages a day; $8640\times(6+2)=69{,}120$ bytes, of which header is 17,280 bytes. (12) Level 4, since multiple nodes use local analysis, storage and application; if one board read all ten sensors it would be level 1.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Distinguish IoT from M2M.**

M2M links machines directly, usually point to point over cellular or proprietary links, in a closed system with one application and one operator, and the devices are homogeneous. IoT uses open, IP-based protocols (MQTT, CoAP, HTTP) over the Internet, devices are heterogeneous, the same data serves many applications, and cloud analytics and machine learning are central. M2M is hardware-centric and IoT is software-centric. A vending machine reporting stock to its operator is M2M; the same machine feeding a shared cloud platform used by the operator, the supplier and an app is IoT.

**Q2 (5 marks). Explain the communication models of IoT.**

Request-response: a client asks, a server answers, stateless (HTTP). Publish-subscribe: publishers send to topics at a broker, the broker forwards to subscribers, the two sides are decoupled (MQTT). Push-pull: producers push into a queue and consumers pull at their pace. Exclusive pair: a persistent full-duplex link between two ends (WebSocket). Example: a hall thermometer publishes `home/hall/temp`; both a dashboard and an alarm subscribe, and neither the thermometer nor the subscribers know each other.

**Q3 (10 marks). Describe the physical and logical design of an IoT system.**

*Introduction.* The physical design shows the tangible parts; the logical design abstracts them into blocks and models.

*Physical design.* Things with sensors, actuators, a processor, storage and a radio; gateways translating local protocols to IP and filtering data; the network and protocol stack (802.15.4, Wi-Fi, BLE, LoRaWAN, 6LoWPAN, IP, TCP/UDP, MQTT, CoAP, HTTP); cloud and applications. Figure 1.1 shows this.

*Logical design.* Six functional blocks: device, communication, services, management, security, application. Four communication models (request-response, publish-subscribe, push-pull, exclusive pair), and two API styles (REST and WebSocket).

*Example.* In a farm system the soil probes and valve are the devices; the gateway runs the irrigation rule and connects to the cloud; the services block exposes `/fields/1/moisture`; the management block tracks firmware versions; security issues certificates; the application is a phone dashboard.

*Conclusion.* The physical design determines what can be built and the logical design keeps the system understandable, so both are drawn before any code is written.

**Q4 (10 marks). Explain the six IoT levels with examples.**

*Introduction.* The levels classify deployment by the number of nodes and by where storage, analysis and the application live.

*Body.* Level 1: one node, everything local (single-board home automation). Level 2: one node, cloud storage (a small farm). Level 3: one node, storage, analysis and app in the cloud (package tracker). Level 4: several nodes, local analysis, cloud storage and app. Level 5: several end nodes and a coordinator (forest-fire detection). Level 6: independent nodes feed a cloud and a cloud controller drives actuators (weather monitoring). Figure 1.2 summarises the movement from local to cloud.

*Example.* Choose level 2 for a farm with 3 probes and one valve; level 5 or 6 for 200 probes.

*Conclusion.* Choose the lowest level that meets the data volume, reliability and cost needs.
