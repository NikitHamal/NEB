---
subject: Internet of Things
grade: BCA Semester 8 (Elective IV)
unit: 4
title: Data and Analytics for IoT
hours: 10
area: BCA 454 · Internet of Things · Unit 4
---

One jet engine fitted with sensors is often quoted as producing terabytes of data on a single long-haul flight. A smart city of a million people produces more readings per second than any person could read in a lifetime. Collecting data is easy; **turning it into decisions in time** is the hard part. This unit covers the five topics of the outline: an introduction to data analytics for IoT, machine learning, big data analytics tools, edge streaming analytics and network analytics. The structure follows the Cisco Press text on IoT fundamentals that the outline lists, with executable examples added.

::: key What this unit gives you
- The types and special features of IoT data, and the difference between data at rest and data in motion.
- Machine learning for IoT: supervised, unsupervised and reinforcement learning, anomaly detection and predictive maintenance, with worked numbers.
- Big data tools: MPP databases, NoSQL, Hadoop (HDFS, MapReduce, YARN), Spark, Kafka and the lambda architecture.
- Edge streaming analytics (filtering, windows, thresholds) and network analytics (flow records and NetFlow).
:::

## 4.1 An introduction to data analytics for IoT

**Structured and unstructured data.** **Structured data** follows a fixed schema and fits rows and columns: a table of `(node, time, temperature)` in a relational database. **Unstructured data** has no fixed schema: camera images, audio, free-text logs, video. **Semi-structured data** (JSON, XML) has tags but a flexible shape. Most IoT data from sensors is structured or semi-structured, and a smaller share (video, audio) is unstructured but very large. IoT data is typically **time-stamped**, comes from **many sources at high speed (velocity)** in **many formats (variety)** and in **large amounts (volume)**: the three Vs of big data, often extended with **veracity** (is it trustworthy?) and **value**.

**Data in motion and data at rest.** **Data in motion** is data as it flows through the network, processed as it arrives (a stream), for example sensor values reaching the edge. **Data at rest** is stored data, held in a database or a distributed file system and analysed later in batches. Both are needed: streams give a quick reaction, stored data gives history and trends.

| Aspect | Data in motion (streaming) | Data at rest (batch) |
|---|---|---|
| Where | Edge, fog, message queue | Data centre, cloud storage |
| Question | What is happening now? | What happened and why? What will happen? |
| Time scale | Milliseconds to seconds | Minutes to days |
| Typical tools | Kafka, Spark Streaming, Flink, edge rules | Hadoop, Spark batch, SQL, warehouse |
| Example | Stop a pump when pressure spikes | Predict next month's energy use |

**Why IoT analytics differs from classic business analytics.** (1) The data arrives continuously, so analysis must be incremental. (2) The sources are **noisy and unreliable**: missing values, drift, duplicates, and clocks that disagree. (3) Much of the value is in **where** data is analysed (at the edge to cut delay and bandwidth, or in the cloud for history). (4) Analytics must often be **automated** into actions, not just reports. (5) Privacy and security duties are larger because the data describes physical behaviour.

**Challenges.** Scale and speed of data, **data quality** (calibration, outliers, missing readings), **bandwidth and cost** of moving everything to the cloud, **latency** for control decisions, **heterogeneous formats**, **storage** over years, **security and privacy**, and finding people with both domain and data skills.

**The analytics maturity ladder.** **Descriptive** analytics says what happened (average temperature yesterday). **Diagnostic** says why (the cooling fan was off). **Predictive** says what will happen (bearing will fail within 12 days). **Prescriptive** says what to do (replace the bearing on Sunday, when the line is idle).

```python
import json, statistics
# Semi-structured IoT records: normal use of data cleaning before analysis
raw = ['{"node": "a1", "t": 21.5}', '{"node": "a1", "t": null}', '{"node": "a1", "t": 22.1}',
       '{"node": "a1", "t": 85.0}', '{"node": "a1", "t": 21.9}', 'not json at all']
good, bad = [], 0
for line in raw:
    try:
        v = json.loads(line)["t"]
    except (ValueError, KeyError):
        bad += 1; continue
    if v is None: bad += 1; continue
    good.append(v)
print("kept", len(good), "rejected", bad)
print("mean with outlier   : %.2f" % statistics.mean(good))
print("median (robust)     : %.2f" % statistics.median(good))
clean = [v for v in good if -40 <= v <= 60]          # physical plausibility range of the sensor
print("mean after range check: %.2f" % statistics.mean(clean))
```
```output
kept 4 rejected 2
mean with outlier   : 37.62
median (robust)     : 22.00
mean after range check: 21.83
```
## 4.2 Machine learning for IoT

**Machine learning (ML)** lets a program learn patterns from data instead of being given explicit rules. It is used in IoT because the volume and complexity of sensor data defeat hand-written thresholds. (Unit 2 of BCA 405 Machine Learning gives the algorithms; here the focus is on **use in IoT**.)

**Types of learning.**

| Type | Idea | IoT example |
|---|---|---|
| **Supervised** | Learn from **labelled** examples to predict a label or a number (classification and regression) | Classify vibration as "normal" or "bearing wear"; predict energy demand |
| **Unsupervised** | Find structure in **unlabelled** data (clustering, anomaly detection) | Group households by usage pattern; detect unusual traffic |
| **Reinforcement** | An agent learns by trial and reward | A thermostat or HVAC controller that learns to save energy while keeping comfort |

**Uses of ML in IoT** (the classification used in the Cisco text):

1. **Monitoring.** Detect problems and faults from patterns, for example detecting that a motor is running hotter than normal.
2. **Behaviour control.** Use monitoring results to trigger actions, for example a rule that throttles a machine.
3. **Operations optimisation.** Improve efficiency or reduce waste, for example choosing the schedule that minimises energy cost.
4. **Self-healing, self-optimising systems.** The system adjusts itself without a human, the long-term goal.

**Predictive maintenance.** Instead of repairing after failure (reactive) or by calendar (preventive), the system **predicts** failure from trends in vibration, temperature or current and schedules repair just in time. The data are collected at the edge, features (such as RMS vibration) are computed, and a model predicts remaining useful life.

**Anomaly detection with the z-score.** A reading is unusual when it lies far from the mean measured in standard deviations: $z=(x-\mu)/\sigma$. A common rule flags $|z|>3$ (under a normal distribution, 99.7 percent of values lie within three standard deviations). For small samples, an outlier inflates $\sigma$ and hides itself, so a **rolling** window or a robust measure (median and MAD) is used.

::: example A motor-temperature anomaly
Ten earlier readings: 61, 62, 60, 63, 61, 62, 64, 61, 62, 60 degrees C. The mean is 61.6 and the sample standard deviation is 1.26. A new reading of 69 gives $z=(69-61.6)/1.26=5.9$, well above 3: an alert. A reading of 64.5 gives $z=2.3$ and is accepted. This is the simplest form of **unsupervised** anomaly detection: no failure labels were needed.
:::

```python
import numpy as np
base = np.array([61, 62, 60, 63, 61, 62, 64, 61, 62, 60], dtype=float)
mu, sd = base.mean(), base.std(ddof=1)
print("mean %.2f  sd %.2f" % (mu, sd))
for x in (62.0, 64.5, 66.0, 69.0):
    z = (x - mu) / sd
    print("reading %.1f  z = %5.2f  %s" % (x, z, "ANOMALY" if abs(z) > 3 else "ok"))

# rolling detector on a stream: window of 8, flag |z| > 3, anomalies are not added to the window
stream = [61, 62, 61, 63, 62, 61, 62, 63, 62, 61, 75, 62, 63, 61, 90]
win, out = [], []
for i, x in enumerate(stream):
    if len(win) >= 8:
        m, s = np.mean(win), max(np.std(win, ddof=1), 0.5)       # floor on s avoids dividing by ~0
        if abs(x - m) / s > 3:
            out.append((i, x)); continue
    win = (win + [x])[-8:]
print("flagged (index, value):", out)
```
```output
mean 61.60  sd 1.26
reading 62.0  z =  0.32  ok
reading 64.5  z =  2.29  ok
reading 66.0  z =  3.48  ANOMALY
reading 69.0  z =  5.85  ANOMALY
flagged (index, value): [(10, 75), (14, 90)]
```
**Forecasting with linear regression.** Often a trend is enough: fit a straight line $y=a+bt$ through recent values by least squares, $b=\dfrac{\sum(t-\bar t)(y-\bar y)}{\sum(t-\bar t)^2}$, and extend it. Bearing temperature rising 0.8 degrees per day towards a limit of 80 degrees C gives a date for maintenance.

```python
import numpy as np
days = np.arange(1, 11)
temp = np.array([62.0, 62.5, 63.1, 63.8, 64.2, 65.1, 65.7, 66.3, 67.2, 67.8])
b, a = np.polyfit(days, temp, 1)                       # slope, intercept
print("fit: temp = %.2f + %.3f * day" % (a, b))
limit = 80.0
day_hit = (limit - a) / b
print("limit %.0f degC reached on day %.1f -> schedule maintenance before day %d" % (limit, day_hit, int(day_hit) - 2))
resid = temp - (a + b * days)
print("max residual %.2f degC, R^2 = %.3f" % (abs(resid).max(), 1 - (resid ** 2).sum() / ((temp - temp.mean()) ** 2).sum()))
```
```output
fit: temp = 61.18 + 0.653 * day
limit 80 degC reached on day 28.8 -> schedule maintenance before day 26
max residual 0.24 degC, R^2 = 0.996
```

## 4.3 Big data analytics tools and technology

When data no longer fits one machine, three families of tools appear: databases built for scale, distributed storage and processing, and streaming platforms.

**Massively parallel processing (MPP) databases.** A relational database split over many nodes, each holding a part of the data and processing it in parallel (Teradata, Amazon Redshift, Greenplum). They keep SQL and strong structure and suit analytical queries over large structured data sets.

**NoSQL databases.** They give up some relational guarantees for scale and flexibility. Four kinds:

| Type | Data model | Examples | IoT use |
|---|---|---|---|
| **Key-value** | Key maps to a value | Redis, DynamoDB | Latest state of each device (key = device ID) |
| **Document** | JSON-like documents | MongoDB, CouchDB | Device records with varying fields |
| **Column family** | Rows with flexible columns grouped in families | Cassandra, HBase | Huge write-heavy time series |
| **Graph** | Nodes and edges | Neo4j | Relations between devices, people and places |

**Time-series databases** (InfluxDB, TimescaleDB, Prometheus) are optimised for time-stamped points: fast appends, down-sampling and retention rules (keep one-second data for a week, one-minute for a year). They are the usual home of sensor readings.

**Hadoop.** Hadoop is an open-source framework for storing and processing very large data sets across clusters of commodity machines. Its core parts:

- **HDFS (Hadoop Distributed File System).** Files are split into large **blocks** (128 MB by default), each replicated on several nodes (default 3) so that a machine failure loses nothing. A **NameNode** keeps the metadata (which block is where) and **DataNodes** store the blocks.
- **MapReduce.** A programming model with two phases. **Map**: each node processes its local block and emits key-value pairs. The framework **shuffles** (groups pairs by key). **Reduce**: each key's values are combined into a result. Computation moves to the data, not data to the computation.
- **YARN (Yet Another Resource Negotiator).** Manages cluster resources and schedules jobs; it lets engines other than MapReduce run on the same cluster.
- **Ecosystem**: Hive (SQL on Hadoop), Pig (scripting), HBase (column store), Sqoop (import from databases), Flume (log collection), Oozie (workflows), ZooKeeper (coordination).

::: example HDFS storage
A 1 GB file with 128 MB blocks has $1024/128=8$ blocks. With replication 3 it occupies 3 GB of raw disk spread over the cluster. With one DataNode lost, each block still has two copies and the NameNode orders new copies to restore 3.
:::

**MapReduce by example.** Daily maximum temperature per node from a log of lines `node,hour,temperature`. The **map** emits `(node, temperature)`, the **shuffle** groups by node, and the **reduce** takes the maximum.

```python
from collections import defaultdict
lines = ["a1,0,21.0", "b2,0,18.5", "a1,1,24.2", "b2,1,19.9", "a1,2,23.1", "c3,0,30.4", "b2,2,17.8", "c3,1,31.0"]

def map_phase(line):                       # runs on every block, in parallel
    node, hour, t = line.split(",")
    yield node, float(t)

shuffle = defaultdict(list)                # the framework groups values by key between map and reduce
for line in lines:
    for k, v in map_phase(line):
        shuffle[k].append(v)

def reduce_phase(key, values):             # runs once per key, in parallel
    return key, max(values), sum(values) / len(values)

for key in sorted(shuffle):
    k, mx, avg = reduce_phase(key, shuffle[key])
    print("%s  max %.1f  avg %.2f  (%d readings)" % (k, mx, avg, len(shuffle[key])))
```
```output
a1  max 24.2  avg 22.77  (3 readings)
b2  max 19.9  avg 18.73  (3 readings)
c3  max 31.0  avg 30.70  (2 readings)
```
**Apache Spark.** Spark keeps data in **memory** across steps, so iterative work (machine learning, graph processing) is much faster than MapReduce's write-to-disk between stages; it offers batch (Spark SQL, DataFrames), streaming (Structured Streaming) and ML libraries. **Apache Kafka** is a distributed, durable **log** to which producers append messages (organised in **topics** and **partitions**) and from which consumers read at their own pace; it decouples many sensors from many consumers and is the usual backbone of streaming. **Storm and Flink** process streams record by record with very low latency.

**The lambda architecture.** It combines a **batch layer** (all data, recomputed periodically, accurate but slow), a **speed layer** (recent data, approximate, immediate) and a **serving layer** that merges their results for queries. A newer simplification, the **kappa architecture**, uses a single streaming path and replays the log when recomputation is needed.

```svgfig label="4.1" caption="Lambda architecture. Sensor data enter a message queue (for example Kafka); the batch layer recomputes accurate views over all stored data, the speed layer updates approximate views from recent data, and the serving layer merges both for dashboards and applications."
f = Fig(640, 250)
f.box(10, 100, 100, 50, "Sensors /\nedge devices", fill=BLUE, stroke=NAVY, size=10)
f.box(150, 100, 100, 50, "Message queue\n(Kafka)", fill=SAND, stroke=AMBER, size=10)
f.box(300, 30, 150, 56, "Batch layer\nHDFS + MapReduce / Spark\n(all data, slow, exact)", fill=MINT, stroke=TEAL, size=9.5)
f.box(300, 164, 150, 56, "Speed layer\nSpark Streaming / Flink\n(recent data, fast)", fill=MINT, stroke=TEAL, size=9.5)
f.box(490, 100, 140, 50, "Serving layer\nmerged views", fill=BLUE, stroke=NAVY, size=10)
f.arrow([(110, 125), (150, 125)], color=NAVY)
f.arrow([(250, 112), (300, 62)], color=NAVY)
f.arrow([(250, 138), (300, 190)], color=NAVY)
f.arrow([(450, 62), (500, 100)], color=TEAL)
f.arrow([(450, 190), (500, 150)], color=TEAL)
f.text(560, 180, "queries,\ndashboards", size=10, color=SLATE)
```

## 4.4 Edge streaming analytics

Sending every reading to the cloud wastes bandwidth and adds delay. **Edge (and fog) analytics** processes data near the source, on the device, gateway or a nearby fog node, and sends upward only the results.

| | Big data analytics (cloud) | Edge streaming analytics |
|---|---|---|
| Data | Large, historical, at rest | Streaming, just-arrived, in motion |
| Latency | Minutes to hours | Milliseconds to seconds |
| Scope | The whole system, many sites | One machine, one site |
| Purpose | Find patterns, train models, plan | React quickly, filter, reduce volume |
| Hardware | Clusters | Gateways, routers, industrial PCs |

The Cisco text describes an edge analytics processing unit with three parts: **raw input data** (the stream of sensor values), an **analytics processing unit (APU)** that filters, cleans and analyses the stream with rules and models, and **output streams** that go to actuators (immediate control) and to the cloud (summarised data). **Distributed analytics systems** place analytics at several levels: simple filters on the device, rules on the gateway, aggregation at the fog node, and heavy model training in the cloud.

**Core edge functions.**

- **Filtering and cleaning**: drop out-of-range values and duplicates.
- **Thresholding**: act when a value crosses a limit, with hysteresis (Section 2.10).
- **Aggregation over windows**: send the average, minimum, maximum and count of a time window instead of every value. A **tumbling window** splits time into fixed, non-overlapping slices (every 60 seconds). A **sliding window** moves forward in smaller steps and overlaps (the last 60 seconds, updated every 10).
- **Complex event processing**: find patterns across streams ("temperature up and vibration up within 5 minutes").
- **Compression and change detection**: report only when a value changes by more than a **deadband**, a technique that often cuts traffic by 90 percent or more.

::: example Traffic saved at the edge
A vibration sensor samples at 1,000 Hz with 2-byte values, which is 2,000 bytes per second. The gateway computes the RMS over 1-second windows and sends 8 bytes per second: a 250-fold reduction (99.6 percent), and raw data are kept only when RMS exceeds a threshold, for diagnosis.
:::

```python
import random
random.seed(3)
# 120 s of temperature at 1 Hz: slow drift plus noise, one spike
data = [20 + 0.01 * i + random.uniform(-0.2, 0.2) for i in range(120)]
data[75] = 35.0

def tumbling(values, size):
    for i in range(0, len(values), size):
        w = values[i:i + size]
        yield i, min(w), max(w), sum(w) / len(w)

print("tumbling 30 s windows (start, min, max, mean):")
for i, lo, hi, mean in tumbling(data, 30):
    print("  t=%3d  min %.2f  max %.2f  mean %.2f" % (i, lo, hi, mean))

# deadband reporting: send only if the value moved more than 0.5 from the last reported value
sent, last = [], None
for i, v in enumerate(data):
    if last is None or abs(v - last) > 0.5:
        sent.append((i, round(v, 2))); last = v
print("deadband 0.5: sent %d of %d readings (%.0f %% saved)" % (len(sent), len(data), 100 * (1 - len(sent) / len(data))))
print("sent:", sent)
alarms = [i for i, v in enumerate(data) if v > 30]
print("edge rule (> 30 degC) fired at t =", alarms)
```
```output
tumbling 30 s windows (start, min, max, mean):
  t=  0  min 19.87  max 20.44  mean 20.15
  t= 30  min 20.21  max 20.76  mean 20.50
  t= 60  min 20.48  max 35.00  mean 21.22
  t= 90  min 20.74  max 21.29  mean 21.05
deadband 0.5: sent 4 of 120 readings (97 % saved)
sent: [(0, 19.9), (26, 20.41), (75, 35.0), (76, 20.81)]
edge rule (> 30 degC) fired at t = [75]
```

## 4.5 Network analytics

**Network analytics** studies the traffic and behaviour of the network that carries IoT data, to manage performance and detect threats. IoT networks have thousands of devices that normally do very **predictable** things (a meter sends 200 bytes to one server every 15 minutes), so any deviation stands out. Uses: **traffic profiling** (what is normal for each device type), **capacity planning**, **troubleshooting** (which link is saturated), **security** (a camera suddenly scanning other hosts), and **billing and quality of service**.

**Flow analysis and NetFlow.** A **flow** is a unidirectional sequence of packets sharing the same **key fields**. In classic NetFlow the key is the 7-tuple: source IP, destination IP, source port, destination port, protocol, type of service and ingress interface. The router or switch keeps a **flow record** per flow, with **non-key fields** such as packet and byte counts, start and end time, TCP flags and next hop, and **exports** the records to a **collector** for analysis. This is far cheaper than capturing every packet and still shows who talked to whom, how much and when.

**Flexible NetFlow (FNF)** lets the operator choose the key and non-key fields through three components:

| Component | Role |
|---|---|
| **Flow record** | Defines the **key fields** (what makes two packets belong to the same flow) and **non-key fields** (what is measured per flow). |
| **Flow exporter** | Defines where and how the cached records are sent (collector address, protocol, timers). |
| **Flow monitor** | Applies the record and exporter to an interface and holds the **flow cache**. |

Related standards are **IPFIX** (the IETF standard derived from NetFlow v9) and **sFlow** (packet sampling). A collector and analyser (commercial or open source) builds **baselines**, such as the usual number of destinations of a sensor, and raises alerts for deviations: a thermostat contacting hundreds of addresses is probably infected (compare the Mirai botnet in Unit 6). In industrial IoT networks, analytics can also learn the normal **protocol conversation** of a plant (which controller writes to which device) and warn when a new one appears.

```python
from collections import defaultdict
# (src, dst, sport, dport, proto, bytes) packets seen on a gateway
packets = [("10.0.0.5", "52.1.1.1", 40001, 1883, "TCP", 120), ("10.0.0.5", "52.1.1.1", 40001, 1883, "TCP", 130),
           ("10.0.0.6", "52.1.1.1", 40002, 1883, "TCP", 118), ("10.0.0.5", "52.1.1.1", 40001, 1883, "TCP", 125),
           ("10.0.0.9", "8.8.8.8", 51000, 53, "UDP", 70)]
packets += [("10.0.0.9", "192.0.2.%d" % i, 52000 + i, 23, "TCP", 60) for i in range(1, 9)]   # camera scanning telnet

flows = defaultdict(lambda: [0, 0])                      # key (5-tuple) -> [packets, bytes]
for src, dst, sp, dp, proto, size in packets:
    f = flows[(src, dst, sp, dp, proto)]
    f[0] += 1; f[1] += size
print("flow records:", len(flows))
for k, (p, b) in list(flows.items())[:3]:
    print("  %s:%d -> %s:%d %s  packets %d bytes %d" % (k[0], k[2], k[1], k[3], k[4], p, b))

dests = defaultdict(set)
for (src, dst, sp, dp, proto) in flows:
    dests[src].add(dst)
BASELINE = 3                                              # a sensor normally talks to at most 3 destinations
for src, d in sorted(dests.items()):
    print("%-9s destinations %2d  %s" % (src, len(d), "ALERT: scanning pattern" if len(d) > BASELINE else "normal"))
```
```output
flow records: 11
  10.0.0.5:40001 -> 52.1.1.1:1883 TCP  packets 3 bytes 375
  10.0.0.6:40002 -> 52.1.1.1:1883 TCP  packets 1 bytes 118
  10.0.0.9:51000 -> 8.8.8.8:53 UDP  packets 1 bytes 70
10.0.0.5  destinations  1  normal
10.0.0.6  destinations  1  normal
10.0.0.9  destinations  9  ALERT: scanning pattern
```
## 4.6 Putting the pieces together: an IoT analytics pipeline

A typical pipeline for the factory-motor example runs in five stages.

1. **Sense**: a vibration and temperature sensor on each motor, sampled at 1 kHz.
2. **Edge**: a gateway computes RMS vibration per second, drops bad readings and applies a local trip rule (stop above a safe limit).
3. **Transport**: MQTT or Kafka carries the one-second summaries to the cloud.
4. **Store and analyse**: summaries are written to a time-series database; a nightly batch job trains or updates a model; the streaming layer scores each new summary.
5. **Act**: a dashboard shows health, alerts go to the maintenance team, and a work order is generated automatically.

```svgfig label="4.2" caption="Where analytics runs. The edge cuts volume and reacts in milliseconds, the fog layer aggregates a site, and the cloud stores history and trains models. Each step up the hierarchy handles less data per second but a wider scope and more time."
f = Fig(640, 230)
f.box(20, 150, 180, 60, "Edge: device / gateway\nfilter, threshold, RMS\nms reaction, all raw data", fill=BLUE, stroke=NAVY, size=9.5)
f.box(230, 90, 180, 60, "Fog: site server\naggregate, local models\nseconds, one site", fill=SAND, stroke=AMBER, size=9.5)
f.box(440, 30, 180, 60, "Cloud: data centre\nhistory, training, planning\nminutes+, all sites", fill=MINT, stroke=TEAL, size=9.5)
f.arrow([(200, 170), (230, 130)], color=NAVY, label="summaries", lpos=(190, 132))
f.arrow([(410, 110), (440, 70)], color=NAVY, label="aggregates", lpos=(400, 72))
f.arrow([(440, 50), (420, 50), (420, 100), (400, 100)], color=TEAL, dash=True)
f.text(120, 40, "data volume: high", size=10, color=SLATE)
f.text(540, 120, "data volume: low", size=10, color=SLATE)
```

## 4.7 Summary and exercises

IoT data is structured, semi-structured and unstructured, time-stamped, fast and large, and exists in motion (streams) and at rest (stores). Machine learning supplies monitoring, behaviour control, operations optimisation and self-healing; supervised models classify and predict, unsupervised models find anomalies and groups, and reinforcement learning controls by reward. Big-data tools (MPP and NoSQL databases, HDFS and MapReduce, YARN, Spark, Kafka, the lambda architecture) handle volume; edge streaming analytics (filtering, windows, deadbands) handles speed and bandwidth; network analytics (flows, NetFlow, FNF) manages and secures the network.

1. Differentiate structured, semi-structured and unstructured data with IoT examples. List the Vs of big data.
2. Compare data in motion and data at rest, with tools and examples of each.
3. Explain the four uses of machine learning in IoT.
4. Differentiate supervised, unsupervised and reinforcement learning with an IoT example each.
5. Ten readings have mean 61.6 and standard deviation 1.26. Is a reading of 66.0 an anomaly under the $|z|>3$ rule?
6. Explain predictive maintenance and how it differs from reactive and preventive maintenance.
7. Fit a line to (1, 10), (2, 12), (3, 13), (4, 15) and predict day 6.
8. Describe HDFS and MapReduce. A 1.5 GB file uses 128 MB blocks and replication 3: how many blocks and how much raw storage?
9. Write the map and reduce functions to count how many readings each node sent.
10. Explain the lambda architecture and the role of Kafka.
11. Compare big-data (cloud) analytics and edge streaming analytics, and explain the three parts of an edge analytics unit.
12. A sensor sends 4-byte readings at 200 Hz. A gateway sends the mean, min and max (12 bytes) per 2-second window. Find the reduction.
13. Define a flow, key fields and non-key fields, and describe the three components of Flexible NetFlow.
14. How can flow records reveal a compromised IoT camera?

**Answers to the numerical items.** (5) $z=(66.0-61.6)/1.26=3.5>3$: anomaly. (7) $\bar t=2.5$, $\bar y=12.5$; $b=\sum(t-\bar t)(y-\bar y)/\sum(t-\bar t)^2=(-1.5)(-2.5)+(-0.5)(-0.5)+(0.5)(0.5)+(1.5)(2.5)=3.75+0.25+0.25+3.75=8$ over $2.25+0.25+0.25+2.25=5$, so $b=1.6$, $a=12.5-1.6(2.5)=8.5$; day 6: $8.5+9.6=18.1$. (8) 1.5 GB $=1536$ MB $/128=12$ blocks; raw storage $=1.5\times3=4.5$ GB. (12) Raw: $200\times4\times2=1600$ bytes per 2 s; sent 12 bytes: a reduction of $1600/12=133$ times (99.25 percent).

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Distinguish data in motion from data at rest.**

Data in motion is data flowing through the network and processed as a stream, at the edge or in a message system such as Kafka, to answer "what is happening now" within milliseconds to seconds (stop a pump when pressure spikes). Data at rest is stored in databases or HDFS and analysed in batches, to answer "what happened and what will happen" over minutes to days (forecast next month's load). IoT needs both: the speed layer for reaction and the batch layer for history and model training, combined in the lambda architecture.

**Q2 (5 marks). Explain MapReduce with an example.**

MapReduce processes large data in parallel in two phases. Map: each node reads its local block and emits key-value pairs. Shuffle: the framework groups values by key. Reduce: each key's values are combined. To find each node's maximum temperature from lines `node,hour,temperature`, map emits `(node, temperature)`, shuffle collects the temperatures per node, and reduce returns the maximum, so `c3` with 30.4 and 31.0 gives 31.0. Computation moves to the data, which avoids moving terabytes over the network.

**Q3 (10 marks). Explain machine learning in IoT, including anomaly detection and predictive maintenance.**

*Introduction.* The volume and complexity of sensor data defeat hand-written rules, so ML finds the patterns.

*Body.* Types: supervised (labelled data, classification or regression), unsupervised (clustering, anomaly detection), reinforcement (reward-driven control). Uses: monitoring, behaviour control, operations optimisation and self-healing. Anomaly detection with the z-score: $z=(x-\mu)/\sigma$ and a limit $|z|>3$; for a motor with mean 61.6 and sd 1.26, a reading of 69 has $z=5.9$ and raises an alert, with no failure labels required. Predictive maintenance: fit the trend (temperature rising 0.65 degrees per day from 61.2) and extrapolate to the limit (80 degrees C on day 29) to schedule repair before failure.

*Example.* Factory motors send RMS vibration summaries; a model flags drift, the system predicts remaining life and issues a work order.

*Conclusion.* ML turns IoT data from records into predictions and actions; it works best with clean, calibrated data and with the model run where the decision is needed, at the edge or in the cloud.

**Q4 (10 marks). Describe edge streaming analytics and network analytics for IoT.**

*Edge streaming analytics.* Process data near the source to cut latency and bandwidth. The analytics processing unit takes raw input data, filters, thresholds, aggregates over tumbling or sliding windows, applies deadbands or complex-event rules, and produces output streams to actuators and to the cloud. Example: 2,000 bytes per second of vibration data becomes 8 bytes per second of RMS values, a 250-fold reduction, with raw data kept only during alarms. Distributed analytics places simple filters on devices, rules on gateways, aggregation in fog and model training in the cloud.

*Network analytics.* Studies traffic to manage and secure the network. A flow is a unidirectional packet sequence with common key fields (addresses, ports, protocol, ToS, interface); the router stores a flow record with packet and byte counts and times and exports it. Flexible NetFlow uses a flow record (key and non-key fields), a flow exporter (collector and timers) and a flow monitor (interface and cache). Baselines of normal behaviour reveal a camera that suddenly contacts dozens of hosts on port 23.

*Conclusion.* Edge analytics gives speed and economy; network analytics gives visibility and protection; the cloud gives history and learning.
