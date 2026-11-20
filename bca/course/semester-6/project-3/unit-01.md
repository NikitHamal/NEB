---
subject: Project III
grade: BCA Semester 6
unit: 1
title: From Web to IoT: Scope, Architecture and Hardware Choice
area: BCA 356 · Project III · Unit 1
---

In Project II the data came from people typing into forms. In Project III the data comes from the **physical world**: a probe in the soil, a temperature sensor on a pole. This adds a new kind of trouble. Sensors are noisy, batteries run out, Wi-Fi drops in the hills, and a wrong reading can make a farmer waste water or lose a crop. This unit shows what changes, how to state the problem with numbers, and how to choose the hardware.

::: key What this unit gives you
- The five things that change when a web project meets sensors and phones.
- A numbered problem statement and scope table for the running example, **KhetSense**.
- The four-layer IoT architecture (sense, edge, cloud, app) with a figure.
- Real photographs of the boards and sensors, and a bill-of-materials script with a budget check.
:::

## 1.1 What changes in Project III

A system that senses and acts is judged on more than a working screen. Five things change.

| Concern | Project II (web system) | Project III (sensor and mobile system) |
|---|---|---|
| Source of data | users type it | sensors measure it, so it is noisy and can be missing |
| Where code runs | browser and server | tiny device, gateway, server and phone |
| Power | mains electricity | battery or solar, so every transmission costs life |
| Network | stable broadband | weak Wi-Fi or mobile data that drops for hours |
| Failure cost | a page does not load | wrong irrigation, spoiled crop, or a lost night of data |

Because of these changes, the Project III report needs a **hardware chapter**, a **data-quality chapter** and an **offline behaviour** section. Examiners ask "what does the app show when the sensor stops sending?" and "how do you know the sensor is accurate?". Units 2 to 4 prepare those answers.

## 1.2 The running example: KhetSense

A cooperative of 40 farmers in a hill village grows tomato and cucumber on terraces. Farmers water by habit: every morning, whether or not the soil is dry.

*Problem statement, version 1.* "Forty farmers of a hill cooperative irrigate every morning by habit. Measurements on 12 test plots show that on 4 of 10 days the soil was already wet enough, so about 35 percent of the water is wasted, and the water tank is empty by April. Without a better rule, the shortage worsens as the plots are extended."

*Objectives (SMART).*

| # | Objective | How it is measured at the demo |
|---|---|---|
| O1 | Soil moisture is read every 15 minutes at 6 plots | 24 hours of data, at most 4 missing readings per node |
| O2 | A moisture reading is within 3 percentage points of the oven-dry reference | 10 paired samples, mean error at most 3 points |
| O3 | A node runs at least 30 days on its battery | battery calculation in Unit 2 |
| O4 | The phone shows the latest reading even without internet | aeroplane-mode demo |
| O5 | The whole kit for 6 plots costs under Rs 30,000 | bill of materials (Section 1.5) |

*Scope table.*

| In scope | Out of scope (future work) |
|---|---|
| 6 soil nodes and 1 weather node, MQTT-style messages, SQLite storage, anomaly check, 24-hour forecast, Android client with offline cache | automatic valve control, satellite imagery, payment, multi-village dashboard |

Notice objective O2. It is a **measurable accuracy target**. A project that only says "the sensor works" cannot be examined; one that says "mean error 2.1 points over 10 samples" can.

## 1.3 The four-layer IoT architecture

Almost every IoT project has the same four layers, and each layer solves one problem.

1. **Sense layer**: sensors that turn a physical quantity (moisture, temperature, humidity) into a voltage or digital value.
2. **Edge layer**: a small board (ESP32, Arduino, Raspberry Pi) that reads the sensor, filters noise, packs a message and sends it. It runs on a battery.
3. **Cloud (server) layer**: a broker that receives messages and a database that stores them; analysis code runs here.
4. **Application layer**: the phone app or web page that shows values and advice to the farmer.

```svgfig label="1.1" caption="KhetSense four-layer architecture. Sensors feed an ESP32 node, which sends a small JSON message over Wi-Fi to a gateway; the server stores the data, analyses it and exposes a REST API that the Android app reads."
f = Fig(580, 230)
f.box(8, 80, 100, 70, "Soil probe\n+ DHT22", fill=BLUE, stroke=NAVY, size=11, color=NAVY)
f.box(150, 80, 100, 70, "ESP32 node\n(battery)", fill=SOFT, stroke=TEAL, size=11, color=NAVY)
f.box(292, 80, 100, 70, "Gateway /\nbroker", fill=SOFT, stroke=AMBER, size=11, color=NAVY)
f.box(434, 20, 138, 60, "Server: SQLite\n+ analysis", fill=BLUE, stroke=RED, size=11, color=NAVY)
f.box(434, 140, 138, 60, "Android app + cache", fill=SOFT, stroke=NAVY, size=11, color=NAVY)
f.arrow([(108,115),(150,115)], color=NAVY)
f.arrow([(250,115),(292,115)], color=NAVY)
f.arrow([(392,100),(434,60)], color=NAVY)
f.arrow([(503,80),(503,140)], color=NAVY)
f.text(129, 105, "ADC", size=9, color=NAVY)
f.text(271, 105, "JSON", size=9, color=NAVY)
f.text(530, 112, "REST", size=9, color=NAVY)
f.text(58, 175, "1 Sense", size=10, color=NAVY)
f.text(200, 175, "2 Edge", size=10, color=NAVY)
f.text(342, 175, "3 Cloud", size=10, color=NAVY)
f.text(503, 218, "4 Application", size=10, color=NAVY)
```

Figure 1.1 also shows where each risk lives. The probe can drift, the node can run out of battery, the Wi-Fi link can drop, and the phone can be offline. A good Project III names the **failure of each arrow** and says what the system does about it.

```photogrid label="1.1" cols="3" ratio="1.0" caption="Three common edge boards. (a) An ESP32 development board mounted beside a breadboard: dual-core 240 MHz chip with built-in Wi-Fi and Bluetooth, the usual choice for a battery node. (b) A Raspberry Pi 4 single-board computer: a full Linux computer, suited to a gateway that runs the database. (c) An Arduino Uno clone: an 8-bit ATmega328P with no networking, very cheap, but it needs an extra module to send data."
@ photo id="bca356/esp32" cap="ESP32 development board"
fit 1.0
focus 0.5 0.8
call 0.5 0.85 0.5 0.62 "ESP32 module"
@ photo id="bca356/rpi" cap="Raspberry Pi 4 gateway"
fit 1.0
focus 0.5 0.5
call 0.5 0.85 0.5 0.62 "CPU under cover"
@ photo id="bca356/uno" cap="Arduino Uno clone"
fit 1.0
focus 0.5 0.5
call 0.5 0.9 0.5 0.7 "ATmega328P"
```

## 1.4 Choosing the sensors and the board

Choose hardware from the **requirements**, not from what looks exciting. Plate 1.2 shows the sensing and watering side of KhetSense.

```photogrid label="1.2" cols="3" ratio="1.0" caption="The physical world that KhetSense measures and controls. (a) A hand-held resistive soil probe: two metal contacts measure how well the soil conducts, which rises with moisture; cheap probes corrode within months. (b) A DHT22 (AM2302) sensor that reports air temperature and humidity digitally. (c) A drip emitter, the device that a future valve would switch on and off."
@ photo id="bca356/soil" cap="Resistive soil probe"
fit 1.0
focus 0.4 0.55
call 0.45 0.5 0.7 0.75 "Metal probe"
@ photo id="bca356/dht22" cap="DHT22 temperature and humidity sensor"
fit 1.0
focus 0.5 0.55
call 0.5 0.9 0.5 0.7 "Vented sensor case"
@ photo id="bca356/drip" cap="Drip emitter"
fit 1.0
focus 0.5 0.5
call 0.5 0.9 0.5 0.7 "Water outlet"
```

| Choice | Option A | Option B | Our decision for KhetSense |
|---|---|---|---|
| Soil sensor | resistive probe (Rs 150, corrodes) | capacitive probe (Rs 350, coated, lasts years) | capacitive, because O2 needs stable readings |
| Air sensor | DHT11 (±2 °C, ±5 %RH) | DHT22 (±0.5 °C, ±2 %RH) | DHT22 on the weather node only |
| Node board | Arduino Uno (no network) | ESP32 (Wi-Fi, deep sleep) | ESP32 |
| Gateway | Raspberry Pi 4 | low-cost Pi Zero 2 class board | decided by the budget script below |
| Power | mains adapter | 18650 cell with a small solar panel | cell and panel, because plots have no mains |

The following script prices both versions of the kit against objective O5. The prices are rough, invented orders of magnitude.

```python
items = {  # name: (price in Rs, v1 qty, v2 qty)
    "ESP32 board": (1200, 7, 7),
    "Capacitive soil probe": (350, 6, 6),
    "DHT22 sensor": (700, 7, 1),
    "18650 cell + holder": (600, 7, 7),
    "1 W solar panel": (500, 7, 7),
    "Weatherproof box": (400, 7, 7),
    "Raspberry Pi 4 gateway": (9000, 1, 0),
    "Pi Zero 2 class gateway": (5000, 0, 1),
}
BUDGET = 30000
for v in (1, 2):
    total = sum(price * qty[v - 1] for price, *qty in items.values())
    verdict = "within" if total <= BUDGET else "OVER"
    print(f"Version {v}: Rs {total:,}  ->  {verdict} budget of Rs {BUDGET:,}  (margin {BUDGET - total:+,})")
```
```output
Version 1: Rs 34,900  ->  OVER budget of Rs 30,000  (margin -4,900)
Version 2: Rs 26,700  ->  within budget of Rs 30,000  (margin +3,300)
```
Version 1 fails objective O5, so the team revises it. This is normal: **a project plan is a series of measured revisions**, and the report should show both versions and the reason for each change.

## 1.5 Requirements as user stories and measurable checks

Write each need as a user story and give it a check that can be shown in the demo.

| User story | Priority | Acceptance check |
|---|---|---|
| As a farmer I want to see today's moisture of my plot, so that I can decide whether to irrigate | Must | latest reading shown with its time |
| As a farmer I want advice in plain words ("water now", "skip today"), so that I do not need to read numbers | Must | rule output matches the table in Unit 3 |
| As a farmer I want the app to work without internet in the field, so that weak coverage does not stop me | Must | aeroplane-mode demo |
| As an extension officer I want a 7-day chart, so that I can advise the cooperative | Should | chart with at least 672 points |
| As a cooperative treasurer I want to know the water saved, so that I can justify the cost | Could | before and after litres |
| As an owner I want an alert when a node is silent for 2 hours, so that I can repair it | Should | alert in the demo log |

## 1.6 Eight reasons sensor projects fail, and the cure

1. **The sensor was never calibrated.** The team trusts the raw number from the datasheet. Compare the sensor with a reference (oven-dry sample, lab thermometer) at several points and fit a line, as in Unit 2.
2. **The battery dies in a week.** The node stays awake and sends every few seconds. Sleep between readings, send in batches, and calculate the battery life before buying, as in Section 2.5.
3. **No plan for a missing reading.** The chart shows a flat line or zero when Wi-Fi drops. Mark gaps as missing, never as zero, and store a timestamp with every reading.
4. **Noise is mistaken for events.** A single spike triggers an irrigation alert. Use a median or moving average and a rule that needs two consecutive high readings.
5. **Hardware not protected from the weather.** Electronics get wet in the first monsoon night. Use a sealed box, cable glands, a drip loop on the cable and a silica-gel pack.
6. **The phone app needs the internet for everything.** In the field there is no signal and the screen is blank. Keep a local cache and sync later, as in Unit 4.
7. **Clock errors.** Nodes without a real-time clock stamp readings wrongly, so the series is out of order. Let the server add its own receive time and keep the node's tick count as a second field.
8. **Testing only on the desk.** Everything works on the table and fails on the terrace because of distance, rain and sunlight. Run a field test of at least 48 hours and report the result honestly (Unit 5).

```photogrid label="1.6" cols="2" ratio="1.27" caption="A sensor node on a far terrace cannot always reach a Wi-Fi router, and a LoRa radio trades speed for range. (a) A LoRa module. (b) Free-space path loss at 868 MHz grows by 6 dB each time the distance doubles. A transmitter at 14 dBm and a receiver sensitivity of -137 dBm at spreading factor 12 give a budget of 151 dB; after keeping 40 dB in reserve for trees, walls and hills the usable loss is 111 dB, which corresponds to about 9.8 km. The faster setting SF7 at -123 dBm has a budget of 97 dB and reaches only 1.9 km. In practice the sensor team picks the slowest rate that the battery can afford."
@ photo id="bcapj/lora" cap="A LoRa radio module, the long-range link for a sensor node far from the Wi-Fi router"
fit 1.27
focus 0.5 0.5
@ svg cap="LoRa link budget: how far can a node reach?"
import math
F = 868.0
def fspl(d):
    return 20 * math.log10(d) + 20 * math.log10(F) + 32.44
def reach(db):
    return 10 ** ((db - 32.44 - 20 * math.log10(F)) / 20.0)
TX, MARGIN = 14.0, 40.0
b12 = TX + 137 - MARGIN
b7 = TX + 123 - MARGIN
r12, r7 = reach(b12), reach(b7)
assert abs(r12 - 9.76) < 0.05 and abs(r7 - 1.95) < 0.05
f = Fig(300, 236)
f.text(150, 14, "free-space path loss at 868 MHz, dB", size=10.5, color=NAVY, bold=True)
ax = Axes(f, 40, 24, 244, 146, (0, 12), (70, 120))
ax.grid(2, 10, xfmt=lambda x: "%d" % x, yfmt=lambda y: "%d" % y)
ax.axes(xl="distance, km", yl="loss, dB")
ax.curve(fspl, 0.2, 12, color=NAVY, sw=2.4, n=240)
ax.hline(b12, color=TEAL)
ax.hline(b7, color=RED)
ax.pt(r12, b12, "", color=TEAL)
ax.pt(r7, b7, "", color=RED)
f.text(150, 207, "SF12 (-137 dBm): %.1f km   SF7 (-123): %.1f km" % (r12, r7), size=10, color=NAVY, bold=True)
f.text(150, 222, "budget = 14 dBm + sensitivity - 40 dB margin", size=10, color=SLATE, bold=True)
facts = dict(r12=r12, r7=r7, b12=b12, b7=b7)
```

## Formula and fact sheet

- Four layers: sense, edge, cloud, application. Each arrow can fail.
- Accuracy target = mean absolute error over paired readings (sensor against reference).
- Budget check: total = sum of (unit price × quantity); keep a margin of at least 5 to 10 percent.
- Missing is not zero: store gaps as missing, with a timestamp.
- ESP32: Wi-Fi + Bluetooth, deep sleep; Arduino Uno: no network; Raspberry Pi: full Linux gateway.

## Chapter summary

- A sensor project adds noisy real-world data, batteries, weak networks and costly failures to the concerns of Project II.
- KhetSense is the running example; its objectives are measurable, including an accuracy target (O2) and a budget (O5).
- The four-layer architecture separates sensing, edge processing, cloud storage and the phone app.
- Hardware is chosen from requirements and checked against the budget; the plan is revised with numbers.
- The eight failure causes (calibration, battery, gaps, noise, weather, offline, clocks, desk-only testing) guide Units 2 to 5.

## Practice

1. List the five concerns that change when a web project becomes a sensor project.
2. Write a four-part problem statement for a project that monitors water level in a village tank.
3. Name the four layers of KhetSense and one failure of each.
4. Why is "the sensor works" a weak objective? Rewrite it as a measurable one.
5. Why is a resistive soil probe a poor choice for a one-year project?
6. State two differences between an ESP32 and an Arduino Uno.
7. Why should a missing reading never be stored as zero?
8. Why does the budget script report version 1 as over budget? Give the cost difference between the two gateways.
9. Rank four user stories of a tank-level monitor with MoSCoW.
10. Version 2 costs Rs 26,700 and the budget is Rs 30,000. What percentage of the budget is the margin?

::: note Answers and worked solutions
**1.** Source of data, where code runs, power, network, failure cost.
**2.** Example: "Fifty households share one village tank. Residents learn that it is empty only when the tap stops. Over three dry months the tank ran dry on 11 days. Without monitoring, shortages increase as households are added."
**3.** Sense (probe drifts), edge (battery dies), cloud (server down), application (phone offline).
**4.** It cannot be checked. Better: "mean error at most 3 moisture points over 10 paired samples".
**5.** Its bare metal contacts corrode within months, so readings drift.
**6.** The ESP32 has built-in Wi-Fi and a deep-sleep mode; the Uno has no network and is an 8-bit board.
**7.** Zero means "completely dry", which is a real value; a gap must show as missing so that charts and rules do not treat it as data.
**8.** Version 1 totals Rs 34,900 against Rs 30,000. The Pi 4 gateway costs Rs 9,000 and the Pi Zero class board Rs 5,000, a difference of Rs 4,000; the other Rs 4,200 saved comes from fitting DHT22 only on the weather node.
**9.** Must: show current level, low-level alert. Should: 7-day chart. Could: SMS. Won't now: pump control.
**10.** Margin Rs 3,300; 3,300 ÷ 30,000 × 100 = 11 percent.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the four-layer architecture of an IoT system with a diagram reference and an example.**

*Introduction.* An IoT (Internet of Things) system connects physical sensors to software through four layers, each solving one problem. Separating them lets each part be built, tested and replaced on its own.

*The layers.*

1. **Sense layer.** Sensors convert a physical quantity into an electrical signal, such as a voltage from a soil probe or a digital value from a DHT22.
2. **Edge layer.** A small board such as the ESP32 reads the sensor through an analogue-to-digital converter, filters noise, packs a short JSON message and sleeps to save battery.
3. **Cloud layer.** A broker receives the messages and a database stores them; analysis code finds anomalies and makes forecasts.
4. **Application layer.** A phone app or web page shows values and advice and keeps a local cache for offline use.

*Example and figure.* In Figure 1.1 a KhetSense node reads moisture every 15 minutes and sends it over Wi-Fi to the gateway; the server stores it and the Android app asks the REST API for the latest value.

*Why use it.* (i) Each layer can be tested separately. (ii) Only the edge layer needs low-power code. (iii) The same cloud data can feed many apps.

*Conclusion.* The four-layer view gives the examiner a map of the system and tells the student where to place each failure and each security control.

**Q2 (5 marks). Compare ESP32, Arduino Uno and Raspberry Pi for use as a battery-powered sensor node. Which would you choose and why?**

*Introduction.* The three boards are all popular in student projects, but they are designed for different jobs. The right choice depends on networking, power use, cost and the amount of computing needed.

| Feature | ESP32 | Arduino Uno | Raspberry Pi 4 |
|---|---|---|---|
| Processor | dual-core 240 MHz | 8-bit 16 MHz | quad-core 1.5 GHz |
| Operating system | none (firmware) | none | full Linux |
| Network | Wi-Fi and Bluetooth built in | none (extra module) | Ethernet, Wi-Fi |
| Sleep current | microamperes in deep sleep | milliamperes (board regulator) | no true deep sleep |
| Rough price | Rs 1,200 | Rs 1,000 | Rs 9,000 |
| Best use | wireless sensor node | learning, simple control | gateway, database, camera |

*Choice.* For a battery node, the ESP32: it has built-in Wi-Fi, sleeps at very low current and costs little. The Uno cannot send data without an extra module, and the Pi uses too much power for a solar node but is suitable as the gateway.

*Conclusion.* Match the board to the layer: ESP32 at the edge, Raspberry Pi class device at the gateway.

**Q3 (10 marks). Describe how you would plan an IoT and mobile-app project from problem to architecture. Use a soil-moisture monitor as an example and discuss requirements, hardware, data quality, power, connectivity and risks.**

*Introduction.* An IoT project joins hardware, networking, data and a mobile app, so planning must cover all four layers. The example is KhetSense, a soil-moisture monitor for a hill cooperative that wastes about 35 percent of its irrigation water.

*1. Problem and objectives.* Write a four-part problem statement (who, what, how big, what if nothing changes) and measurable objectives: read every 15 minutes, error at most 3 points, 30-day battery life, offline app, kit under Rs 30,000.

*2. Architecture.* Draw the four layers (Figure 1.1): sensors, ESP32 node, gateway and server, Android app. Mark every arrow as a possible failure.

*3. Hardware choice.* Select parts from requirements: capacitive probe for lasting accuracy, DHT22 for air readings, ESP32 for Wi-Fi and sleep, solar-charged 18650 cell. Check the total with a bill of materials; version 1 cost Rs 34,900 and was revised to Rs 26,700.

*4. Data quality.* Calibrate against an oven-dry reference, filter noise with a median or moving average, and store gaps as missing with a timestamp.

*5. Power and connectivity.* Sleep between readings, send batches, and calculate battery life before buying. Plan for the network to drop: the node buffers and the app caches.

*6. Risks and testing.* Weather, corrosion, clock errors and desk-only testing are the usual causes of failure; plan a 48-hour field test.

| Area | Web project (II) | IoT project (III) |
|---|---|---|
| Data source | users | sensors with noise and gaps |
| Power | mains | battery, solar |
| Network | stable | intermittent |
| Failure | page error | wrong physical action |

*Conclusion.* A well-planned IoT project states measurable targets, chooses hardware by numbers, and designs for noise, gaps and outages from the first day.
