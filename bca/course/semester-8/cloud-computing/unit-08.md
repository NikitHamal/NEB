---
subject: Cloud Computing
grade: BCA Semester 8
unit: 8
title: Parallel Computing and the MapReduce Model
hours: 8
area: BCA 451 · Cloud Computing · Unit 8
---

Everything in the earlier units (virtual machines, storage, networks, containers) exists so that **many ordinary computers can behave like one very large one**. This unit shows how a *program* uses that large machine. Its answer is the idea that made cloud-scale data processing practical: **MapReduce**, a programming model in which the programmer writes two small functions and the platform handles distribution, scheduling, communication and failure.

The unit follows the TU outline: introduction to parallel computing, the MapReduce model, applications of MapReduce, parallel efficiency of MapReduce, and MapReduce infrastructure. Every numerical example is calculated by a short Python program in the book, so you can check each result.

::: key What this unit gives you
- Parallel computing: types of parallelism, Flynn's taxonomy, speedup, efficiency, Amdahl's law and Gustafson's law.
- The MapReduce model: map, shuffle and sort, reduce, combiner and partitioner, with an executed word-count example.
- Typical applications (word count, inverted index, grep, joins, log analysis, PageRank) and the cases where MapReduce is a poor fit.
- A cost model for a MapReduce job and its parallel efficiency; stragglers and speculative execution.
- The infrastructure: Google MapReduce and GFS, Hadoop HDFS and YARN, data locality, fault tolerance and the cloud services built on them.
:::

## 8.1 Introduction to parallel computing

**Serial computing** executes instructions one after another on one processor. **Parallel computing** divides a problem into parts that are solved *at the same time* on several processing elements. Parallelism is needed for two reasons: a single processor cannot be made fast enough (clock speeds stopped rising in the mid-2000s because of heat), and the data of a modern service is simply too large for one machine to read in reasonable time. Reading 1 TB at 200 MB/s from one disk takes about 5,000 seconds (nearly an hour and a half); 1,000 disks reading in parallel take about 5 seconds.

### Levels and kinds of parallelism

| Kind | What runs in parallel | Example |
|---|---|---|
| **Bit-level** | The bits of one word | A 64-bit adder works on all 64 bits at once |
| **Instruction-level** | Several instructions of one program | Pipelining and superscalar CPU cores (BCA 152) |
| **Data parallelism** | The *same* operation on different parts of the data | Counting words in each of 1,000 file blocks; GPU image filters |
| **Task parallelism** | *Different* operations at the same time | One thread serves web requests while another writes logs |
| **Pipeline parallelism** | Stages of a flow work on different items | Fetch, parse, index and store stages of a web crawler |

MapReduce is mostly **data parallelism**: the same map function runs on every block of the input.

### Flynn's taxonomy

Flynn classified architectures by the number of instruction streams and data streams.

| Class | Meaning | Example |
|---|---|---|
| **SISD** | Single instruction, single data | A classical single-core computer |
| **SIMD** | One instruction applied to many data items | Vector units, GPUs |
| **MISD** | Several instructions on one data stream | Rare; some fault-tolerant systems |
| **MIMD** | Many processors, each with its own instructions and data | Multicore servers, clusters, the cloud |

A cloud cluster is **MIMD** and is usually organised with **distributed memory**: each node has its own memory and nodes communicate by messages over the network. In **shared-memory** machines (one multicore server) all processors see the same memory, which is simpler to program but does not scale beyond one box.

### Speedup, efficiency and Amdahl's law

If a job takes T1 seconds on one processor and Tp on p processors:

- **Speedup** S = T1 / Tp.
- **Efficiency** E = S / p. Perfect scaling has S = p and E = 1 (100%).

Almost no program is perfectly parallel. Suppose a fraction **f** of the work can be parallelised and the remaining **1 − f** is serial (reading the input, combining results, a lock). **Amdahl's law** gives the best possible speedup:

$$S(p) = \frac{1}{(1 - f) + f / p}$$

As p grows, the term f / p vanishes, so the speedup can never exceed **1 / (1 − f)**. With f = 0.95 the limit is 20, however many machines are used.

```python
def amdahl(f, p):
    return 1 / ((1 - f) + f / p)

for f in (0.90, 0.95, 0.99):
    row = []
    for p in (2, 8, 64, 1024):
        s = amdahl(f, p)
        row.append(f"p={p}: S={s:.2f} E={s / p * 100:.1f}%")
    print(f"f={f}: limit {1 / (1 - f):.0f}x | " + " | ".join(row))
```
```output
f=0.9: limit 10x | p=2: S=1.82 E=90.9% | p=8: S=4.71 E=58.8% | p=64: S=8.77 E=13.7% | p=1024: S=9.91 E=1.0%
f=0.95: limit 20x | p=2: S=1.90 E=95.2% | p=8: S=5.93 E=74.1% | p=64: S=15.42 E=24.1% | p=1024: S=19.64 E=1.9%
f=0.99: limit 100x | p=2: S=1.98 E=99.0% | p=8: S=7.48 E=93.5% | p=64: S=39.26 E=61.3% | p=1024: S=91.18 E=8.9%
```

The table is the central lesson of parallel computing: with 95% parallel work, 64 processors give a speedup of about 15, not 64, and 1,024 processors give barely 20. **The serial part, not the number of machines, decides the limit.** That is why MapReduce moves almost *all* work into the parallel map and reduce phases and keeps the serial coordination tiny.

**Gustafson's law** offers the optimistic view. If the *problem size grows with the number of processors* (a bigger data set for a bigger cluster, which is exactly what cloud users do), the scaled speedup is S = p − (1 − f)(p − 1) for the serial fraction (1 − f) measured on the parallel run. Big-data jobs live in this regime: a cluster is added because the data grew, not to make a fixed job faster.

### Why parallel programs are hard

Programmers of explicit parallel code must handle **partitioning** the work, **communication** between parts, **synchronisation** (locks, barriers), **load balancing** (one slow part delays the whole job), **fault tolerance** (with 1,000 machines, some fail every day) and **debugging** non-deterministic behaviour (race conditions, deadlock; see BCA 251 and Unit 6 of the distributed systems book). MapReduce removes most of these from the programmer by fixing the *shape* of the computation.

## 8.2 The MapReduce model

MapReduce was introduced by Jeffrey Dean and Sanjay Ghemawat at Google (OSDI 2004). Its design idea is that a very large class of data-processing jobs can be written as two functions on **key/value pairs**:

- **map**: (k1, v1) → list of (k2, v2). It is applied to *every input record independently* and emits intermediate key/value pairs.
- **reduce**: (k2, list of v2) → list of (k3, v3). It receives *all* the values that share one intermediate key and combines them.

Between the two, the framework performs the **shuffle and sort**: it moves every intermediate pair across the network to the reducer responsible for its key, and groups the pairs by key. The programmer never writes this step.

### The word-count example

The classic example counts how often each word occurs in a collection of documents.

1. **Split.** The input is divided into splits (usually one per file block); each split is given to a map task.
2. **Map.** For every word in its split, a map task emits the pair (word, 1).
3. **Shuffle and sort.** All pairs with the same word go to the same reducer, grouped as (word, [1, 1, 1 ...]).
4. **Reduce.** The reducer sums the list and emits (word, total).

The following program imitates the framework in memory with three splits, so that each phase can be printed.

```python
from collections import defaultdict

splits = ["cloud moves fast", "fast cloud scales", "cloud cloud cloud"]

# map phase: one task per split
map_out = []
for task, text in enumerate(splits):
    pairs = [(word, 1) for word in text.split()]
    map_out.append(pairs)
    print(f"map task {task}: {pairs}")

# shuffle and sort: group by key
groups = defaultdict(list)
for pairs in map_out:
    for key, value in pairs:
        groups[key].append(value)
print("after shuffle:", {k: groups[k] for k in sorted(groups)})

# reduce phase
result = {key: sum(values) for key, values in sorted(groups.items())}
print("reduce output:", result)
print("pairs shuffled:", sum(len(p) for p in map_out), "distinct keys:", len(result))
```
```output
map task 0: [('cloud', 1), ('moves', 1), ('fast', 1)]
map task 1: [('fast', 1), ('cloud', 1), ('scales', 1)]
map task 2: [('cloud', 1), ('cloud', 1), ('cloud', 1)]
after shuffle: {'cloud': [1, 1, 1, 1, 1], 'fast': [1, 1], 'moves': [1], 'scales': [1]}
reduce output: {'cloud': 5, 'fast': 2, 'moves': 1, 'scales': 1}
pairs shuffled: 9 distinct keys: 4
```

Nine words became nine intermediate pairs; the shuffle grouped them into four keys; the reduce step produced the four totals. If the three splits had been three terabytes each, the programmer's code would be unchanged: only the number of tasks changes.

### Combiner and partitioner

- A **combiner** is a "mini-reducer" run on each mapper's output *before* the shuffle. For word count it adds up the pairs of the same word locally, so (cloud, 1) repeated 5,000 times from one mapper becomes (cloud, 5000). It is allowed when the reduce function is **associative and commutative** (sum, max, count) and it can cut the shuffled data dramatically, since the network is the scarcest resource.
- The **partitioner** decides which reducer gets which key, usually `hash(key) mod R` for R reducers. A poor partitioner or a very **skewed** key (one word making up 30% of all words) makes one reducer the bottleneck; fixes include custom partitioning and key salting.

::: note
Why this model fits the cloud: map tasks are independent, so they can run on any machine and be **restarted anywhere** if a machine fails; reduce tasks depend only on the shuffled data. Failure handling is therefore easy: just run the task again.
:::

## 8.3 Applications of MapReduce

Any job that processes a huge set of independent records and then aggregates by key is a candidate. The original paper and later practice list the following patterns.

| Application | Map emits | Reduce does |
|---|---|---|
| **Word count** | (word, 1) | Sums the counts |
| **Distributed grep** | The line, if it matches the pattern | Identity (just copies matches) |
| **Count of URL accesses** | (URL, 1) from each log line | Sums to get hits per URL |
| **Inverted index** (search engines) | (word, document ID) | Builds the list of documents for each word |
| **Reverse web-link graph** | (target URL, source URL) for each link | Lists all pages that link to a target |
| **Sorting** (TeraSort) | (key, record); the framework's shuffle sorts | Identity, with a range partitioner |
| **Log analysis** | (error code, 1) or (user, session data) | Counts, averages, session building |
| **Relational join** | (join key, tagged row from either table) | Combines rows that share the key |
| **PageRank** (one iteration) | Sends rank shares to linked pages | Sums incoming shares |
| **k-means** (one iteration) | (nearest centroid, point) | Averages points to new centroids |
| **Machine-learning feature counts** | (feature, label statistics) | Aggregates statistics (naive Bayes) |

### Worked example: an inverted index

An inverted index lists, for each word, the documents that contain it; it is the heart of a search engine. With three tiny documents:

- doc1: "nepal cloud", doc2: "cloud storage", doc3: "nepal storage cloud".

*Map* emits (nepal, 1), (cloud, 1) for doc1; (cloud, 2), (storage, 2) for doc2; (nepal, 3), (storage, 3), (cloud, 3) for doc3. After the shuffle the reducers receive: cloud: [1, 2, 3], nepal: [1, 3], storage: [2, 3]. *Reduce* writes each list. A query for "nepal AND cloud" intersects the lists [1, 3] and [1, 2, 3] and returns documents 1 and 3.

### When MapReduce is a poor fit

1. **Iterative algorithms** (PageRank to convergence, machine learning): each iteration is a full job that writes its result to disk and reads it back. Frameworks that keep data in memory between steps (Apache Spark) are far faster.
2. **Low-latency or interactive queries:** starting a job takes seconds to minutes.
3. **Small data:** the start-up overhead exceeds the compute; a single machine is simpler and faster.
4. **Tightly coupled computation** with heavy communication between parts (many scientific simulations): these need message passing (MPI).
5. **Streaming:** continuous event streams need stream processors rather than batch jobs.

## 8.4 Parallel efficiency of MapReduce

A MapReduce job has four stages that run one after another: **map**, **shuffle**, **reduce** and writing the output. Inside each stage the tasks are parallel. If there are *m* map tasks and *s* map slots (a slot is one task that can run at a time on the cluster), the map stage runs in **waves**: ceil(m / s) rounds, each lasting as long as its slowest task.

A cost model for the job time is therefore:

T(job) = waves(map) × t(map) + t(shuffle) + waves(reduce) × t(reduce)

The following program evaluates a typical job: 1,000 map tasks of 60 seconds on 100 map slots, a 120-second shuffle, and 50 reduce tasks of 40 seconds on 25 reduce slots. The serial time is the sum of all the task times on one processor (no shuffle is needed on a single machine).

```python
import math
m, t_map, s_map = 1000, 60, 100
r, t_red, s_red = 50, 40, 25
shuffle = 120

map_waves = math.ceil(m / s_map)
red_waves = math.ceil(r / s_red)
t_parallel = map_waves * t_map + shuffle + red_waves * t_red
t_serial = m * t_map + r * t_red
speedup = t_serial / t_parallel
print(f"map waves {map_waves} x {t_map}s = {map_waves * t_map}s")
print(f"shuffle {shuffle}s")
print(f"reduce waves {red_waves} x {t_red}s = {red_waves * t_red}s")
print(f"parallel time {t_parallel}s, serial time {t_serial}s")
print(f"speedup {speedup:.1f}, efficiency on {s_map} slots {speedup / s_map * 100:.1f}%")

# a straggler in the last map wave
slow = 300
without_backup = (map_waves - 1) * t_map + slow
backup_finish = map_waves * t_map + t_map          # backup starts when the normal tasks finish
with_backup = min(without_backup, backup_finish)
print(f"straggler: map stage {without_backup}s without backup, {with_backup}s with speculative backup")
print(f"job time {without_backup + shuffle + red_waves * t_red}s vs {with_backup + shuffle + red_waves * t_red}s")
```
```output
map waves 10 x 60s = 600s
shuffle 120s
reduce waves 2 x 40s = 80s
parallel time 800s, serial time 62000s
speedup 77.5, efficiency on 100 slots 77.5%
straggler: map stage 840s without backup, 660s with speculative backup
job time 1040s vs 860s
```

The job takes 800 seconds instead of 62,000, a speedup of 77.5 and an efficiency of 77.5% on 100 slots. The lost 22.5% has three causes that appear in every real job: the **shuffle** (a serial-looking network stage), the **second reduce wave** that leaves slots idle, and the **start-up and wave rounding** effects. A **straggler**, one task that runs five times slower because of a failing disk or a busy node, would stretch the map stage from 600 to 840 seconds. **Speculative execution** launches a second copy of the slow task on a free node and uses whichever finishes first; here it brings the map stage to 660 seconds.

### Factors that decide efficiency

| Factor | Effect | Remedy |
|---|---|---|
| **Shuffle volume** | The network moves every intermediate pair; it is often the bottleneck | Combiner; compress map output; fewer, bigger keys |
| **Data skew** | One reducer receives far more data than the others and finishes last | Better partitioner; split hot keys; sampling |
| **Task granularity** | Too few big tasks leave nodes idle; too many tiny tasks waste start-up time | Choose splits near the file block size (64 to 256 MB) |
| **Stragglers** | One slow task delays the whole stage | Speculative execution; replace unhealthy nodes |
| **Data locality** | Reading a block over the network is slower than reading it locally | Schedule the map task on a node that holds the block |
| **Job start-up** | Seconds to minutes of scheduling and container start | Reuse containers; batch small jobs |
| **Number of reducers** | Too few means long reducers; too many means many small output files | About 0.95 to 1.75 times the reduce slots is a common guide |

### The effect of a combiner, in numbers

Suppose each of 1,000 mappers emits 1,000,000 word pairs, but only 20,000 distinct words occur in its split, and one pair takes about 16 bytes.

```python
mappers, pairs_each, distinct, bytes_per_pair = 1000, 1_000_000, 20_000, 16
no_comb = mappers * pairs_each * bytes_per_pair
with_comb = mappers * distinct * bytes_per_pair
print(f"without combiner: {mappers * pairs_each:,} pairs, {no_comb / 1e9:.1f} GB shuffled")
print(f"with combiner:    {mappers * distinct:,} pairs, {with_comb / 1e9:.2f} GB shuffled")
print(f"reduction: {(1 - with_comb / no_comb) * 100:.0f}%")
```
```output
without combiner: 1,000,000,000 pairs, 16.0 GB shuffled
with combiner:    20,000,000 pairs, 0.32 GB shuffled
reduction: 98%
```

Because the network is shared by all tasks, cutting the shuffle by 98% usually matters more than making the map code faster. A combiner is legal only when the reduce function is associative and commutative; computing an *average* needs the combiner to emit (sum, count) pairs, not partial averages.

## 8.5 MapReduce infrastructure

### Google's design

The original system ran on thousands of cheap commodity machines. Its parts were:

- **Google File System (GFS):** a distributed file system storing large files as 64 MB chunks, each replicated (usually three times) on different machines (Ghemawat, Gobioff and Leung, 2003).
- **A master:** accepts jobs, splits them into map and reduce tasks, assigns tasks to workers, tracks their state and re-executes failed ones.
- **Workers:** machines that run map and reduce tasks. The master prefers to run a map task **on the machine that stores its chunk** (or on one in the same rack), so that the input is read locally.

### Hadoop

**Apache Hadoop** is the open-source implementation, begun by Doug Cutting and Mike Cafarella and driven by Yahoo. Its core is three layers:

| Layer | Component | Role |
|---|---|---|
| Storage | **HDFS** (Hadoop Distributed File System) | Stores files as blocks (default 128 MB) replicated on several **DataNodes**; the **NameNode** keeps the metadata (file-to-block map, locations) |
| Resource management | **YARN** | A **ResourceManager** allocates containers; a **NodeManager** on each machine runs them; an **ApplicationMaster** per job negotiates resources |
| Processing | **MapReduce** (and later Spark, Tez) | Runs the map and reduce tasks in YARN containers |

Around the core grew an ecosystem: **Hive** (SQL on Hadoop), **Pig** (a data-flow language), **HBase** (a column database on HDFS), **Sqoop** (import from relational databases), **Flume** and **Kafka** (data ingestion), **ZooKeeper** (coordination) and **Spark** (in-memory processing, which has largely replaced raw MapReduce for iterative and interactive work).

### What happens when a job runs

1. The client submits the job; the input files are divided into **input splits**, usually one per HDFS block.
2. The scheduler starts map tasks, preferring nodes that hold the block (**data locality**).
3. Each map task reads its split, runs the map function and buffers the output in memory; when the buffer fills it **spills** a sorted file to the local disk, partitioned by reducer (the combiner may run here).
4. Reducers **fetch** their partitions from every mapper over the network (the shuffle), **merge** the sorted pieces and run the reduce function.
5. Reducers write the output to HDFS, one file per reducer (`part-00000`, `part-00001`, ...).

### Fault tolerance

- Workers send **heartbeats**. If a worker stops responding, its running tasks are rescheduled; its *completed map tasks* are also re-run, because their output was on its local disk, which is now unreachable. Completed reduce tasks are not re-run, as their output is already in the replicated file system.
- HDFS replication (default three copies, placed on at least two racks) protects the data itself. If a replica is lost, the NameNode orders a new copy.
- A failure of the master or NameNode was a single point of failure in early versions; modern Hadoop uses a **standby NameNode** and ResourceManager failover.

```python
import math
block_mb, replicas = 128, 3
file_gb = 1
blocks = math.ceil(file_gb * 1024 / block_mb)
print(f"1 GB file: {blocks} blocks, {blocks * replicas} block replicas, {file_gb * replicas} GB raw storage")

tb = 1
splits = math.ceil(tb * 1024 * 1024 / block_mb)
slots, task_s = 100, 60
waves = math.ceil(splits / slots)
print(f"1 TB input: {splits} splits = {splits} map tasks; on {slots} slots: {waves} waves, about {waves * task_s / 3600:.2f} hours of map time")
```
```output
1 GB file: 8 blocks, 24 block replicas, 3 GB raw storage
1 TB input: 8192 splits = 8192 map tasks; on 100 slots: 82 waves, about 1.37 hours of map time
```

A 1 GB file thus occupies 24 block replicas and 3 GB of raw disk, a **3x storage overhead** that buys durability and locality (compare the erasure-coding saving in Unit 3). A 1 TB input creates 8,192 map tasks, which 100 slots run in 82 waves, about 1.4 hours; ten times more slots (9 waves) would bring that down to about 9 minutes, until the shuffle and reduce stages dominate (Amdahl's law again).

### MapReduce in the cloud

Cloud providers offer MapReduce-style processing as a managed service so that customers need not run a cluster: **Amazon EMR**, **Azure HDInsight** and **Google Dataproc** start Hadoop or Spark clusters on demand, read data from object storage instead of HDFS, and are billed per second. The **elasticity** of Unit 1 matters here: a nightly job can rent 200 nodes for one hour instead of owning 200 machines all year, and the cluster is deleted when the job ends.

## 8.6 Seeing the ideas: the dataflow and the limits of speedup

Figure 8.1 follows the word-count example of section 8.2 through every stage. Figure 8.2 plots Amdahl's law for three parallel fractions.

```svgfig label="8.1" caption="MapReduce dataflow for the word-count example of section 8.2 with two reducers. Maps emit (word, 1); the shuffle sends each key to one reducer (here cloud and scales to reducer 0, fast and moves to reducer 1) and groups the values; reducers sum and write the output."
f = Fig(580, 214)
sp = ["cloud moves fast", "fast cloud scales", "cloud cloud cloud"]
for i, t in enumerate(sp):
    y = 14 + i * 58
    f.box(4, y, 104, 44, "split " + str(i) + "\n" + t, fill=SAND, stroke=AMBER, size=8.5)
    f.box(128, y, 86, 44, "map " + str(i) + "\n(word, 1)", fill=BLUE, stroke=NAVY, size=9, bold=True)
    f.arrow([(108, y + 22), (128, y + 22)])
    f.arrow([(214, y + 22), (236, 100)])
f.box(236, 14, 100, 160, "shuffle\nand sort\n\ngroup by key,\nmove over\nthe network", fill=ROSE, stroke=RED, size=9.5, bold=True)
f.box(360, 30, 100, 54, "reduce 0\ncloud: [1,1,1,1,1]\nscales: [1]", fill=MINT, stroke=TEAL, size=8.5)
f.box(360, 112, 100, 54, "reduce 1\nfast: [1,1]\nmoves: [1]", fill=MINT, stroke=TEAL, size=8.5)
f.arrow([(336, 57), (360, 57)]); f.arrow([(336, 139), (360, 139)])
f.box(484, 30, 92, 54, "part-00000\ncloud 5\nscales 1", fill=BLUE, stroke=NAVY, size=9)
f.box(484, 112, 92, 54, "part-00001\nfast 2\nmoves 1", fill=BLUE, stroke=NAVY, size=9)
f.arrow([(460, 57), (484, 57)]); f.arrow([(460, 139), (484, 139)])
f.text(290, 200, "input splits (HDFS blocks)  >  map  >  shuffle  >  reduce  >  output files in HDFS", size=9.5, color=NAVY, bold=True)
```

```svgfig label="8.2" caption="Amdahl's law. With 90%, 95% and 99% parallel work the speedup flattens at 10, 20 and 100. At 64 processors the three curves reach 8.8, 15.4 and 39.3. The serial fraction, not the machine count, sets the limit."
f = Fig(580, 214)
ax = Axes(f, 56, 14, 480, 160, (0, 64), (0, 45))
ax.grid(16, 15)
ax.axes("processors p", "speedup S")
ax.curve(lambda p: 1 / ((1 - 0.90) + 0.90 / max(p, 1)), 1, 64, color=AMBER, label="f = 0.90", lx=ax.X(46), ly=ax.Y(5))
ax.curve(lambda p: 1 / ((1 - 0.95) + 0.95 / max(p, 1)), 1, 64, color=RED, label="f = 0.95", lx=ax.X(46), ly=ax.Y(20))
ax.curve(lambda p: 1 / ((1 - 0.99) + 0.99 / max(p, 1)), 1, 64, color=TEAL, label="f = 0.99", lx=ax.X(51), ly=ax.Y(42))
ax.curve(lambda p: p, 1, 45, color=SLATE, dash=True, label="ideal S = p", lx=ax.X(30), ly=ax.Y(41))
f.text(290, 206, "Limit 1/(1 - f): 10, 20 and 100. Speedup per processor falls as p grows.", size=10, color=NAVY, bold=True)
```

## 8.7 Summary and exercises

Parallel computing divides work across processors; speedup S = T1/Tp and efficiency E = S/p are limited by the serial fraction (Amdahl: S ≤ 1/(1 − f)). MapReduce fixes the shape of a data-parallel job as map, shuffle and sort, and reduce over key/value pairs, with an optional combiner and a partitioner. It suits large batch jobs (word count, inverted index, log analysis, joins) and suits iterative, interactive and tightly coupled jobs poorly. Job time follows from waves, shuffle and stragglers, and is improved by combiners, locality, good partitioning and speculative execution. Hadoop provides HDFS (blocks, replication, NameNode and DataNodes), YARN (containers) and MapReduce, and clouds offer them as managed, per-second services.

1. Define parallel computing and explain why it is needed. Distinguish data, task and pipeline parallelism.
2. State Flynn's taxonomy with an example of each class.
3. Define speedup and efficiency. State Amdahl's law and find the speedup limit for f = 0.8.
4. Using the formula, compute the speedup and efficiency for f = 0.95 on 16 processors.
5. Explain the map, shuffle and reduce phases with a word-count example.
6. What are a combiner and a partitioner? When is a combiner not allowed?
7. Write the map and reduce outputs for an inverted index of the three documents in section 8.3, and answer the query "storage AND cloud".
8. List five applications of MapReduce and three situations in which it is a poor choice.
9. A job has 600 map tasks of 30 s on 60 slots, a 90 s shuffle and 20 reduce tasks of 50 s on 20 slots. Find the parallel time, serial time, speedup and efficiency.
10. Explain stragglers and speculative execution, and the effect of skewed keys.
11. Describe the architecture of HDFS and the job flow in Hadoop MapReduce.
12. A 512 MB file is stored in HDFS with 64 MB blocks and replication 3. How many blocks and replicas, and how much raw storage?
13. Explain how MapReduce tolerates the failure of a worker, including why completed map tasks are re-run.
14. How do EMR, HDInsight and Dataproc use cloud elasticity for MapReduce jobs?

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain Amdahl's law. A program is 95% parallelisable. Find the speedup on 16 processors and the maximum possible speedup.**

*Introduction.* Parallel speedup is limited by the part of the program that must run serially (section 8.1 and Figure 8.2).

*Law.* If f is the parallel fraction, S(p) = 1 / ((1 − f) + f / p).

*Calculation.*

1. S(16) = 1 / (0.05 + 0.95 / 16) = 1 / (0.05 + 0.059375) = 1 / 0.109375 = **9.14**.
2. Efficiency = 9.14 / 16 = **57.1%**.
3. Maximum (p → infinity): 1 / 0.05 = **20**.

*Interpretation.* Sixteen processors give less than ten times the speed, and no number of processors can give more than twenty. Reducing the serial fraction is more valuable than adding machines; MapReduce keeps the serial part small.

*Conclusion.* The serial fraction sets the ceiling; Gustafson's law reminds us that larger problems on larger clusters keep efficiency acceptable.

**Q2 (5 marks). Explain the MapReduce model with the word-count example.**

*Introduction.* MapReduce is a programming model for processing very large data sets on a cluster using two user functions on key/value pairs (section 8.2, Figure 8.1).

*Phases.*

1. **Split:** the input is divided into splits, one map task each.
2. **Map:** for each word emit (word, 1). For "cloud moves fast" the output is (cloud, 1), (moves, 1), (fast, 1).
3. **Shuffle and sort:** pairs with the same key go to the same reducer, grouped: cloud: [1, 1, 1, 1, 1], fast: [1, 1], moves: [1], scales: [1] for the three-document example.
4. **Reduce:** sum each list: cloud 5, fast 2, moves 1, scales 1.

*Optimisation.* A combiner sums locally before the shuffle, cutting shuffled data (for the example of section 8.4 from 16 GB to 0.32 GB, a 98% reduction).

*Conclusion.* The programmer writes only map and reduce; the framework handles distribution, grouping, scheduling and failure.

**Q3 (10 marks). Describe Hadoop's MapReduce infrastructure, the job flow and the fault tolerance. Compute the HDFS storage for a 1 GB file with 128 MB blocks and replication 3.**

*Introduction.* Hadoop is the open-source implementation of Google's GFS and MapReduce for clusters of commodity machines (section 8.5).

*Components.*

| Layer | Component | Role |
|---|---|---|
| Storage | HDFS: NameNode and DataNodes | Blocks of 128 MB, replicated; the NameNode holds metadata |
| Resources | YARN: ResourceManager, NodeManager, ApplicationMaster | Allocates containers for tasks |
| Processing | MapReduce | Runs map and reduce tasks |

*Job flow.* Input splits (one per block) are given to map tasks, preferably on the node holding the block (data locality). Map output is partitioned, sorted and spilled to local disk, with an optional combiner. Reducers fetch their partitions (the shuffle), merge, reduce and write part files to HDFS.

*Fault tolerance.* Heartbeats detect failed workers; their running tasks and their *completed map tasks* (whose output was on the lost local disk) are re-executed; completed reducers are not repeated because the output is already replicated in HDFS. HDFS re-replicates lost blocks. Speculative execution handles stragglers. A standby NameNode removes the single point of failure.

*Calculation.* A 1 GB file is 1,024 MB / 128 MB = **8 blocks**. With replication 3 that is 8 × 3 = **24 block replicas** and **3 GB** of raw storage, a 3x overhead that buys durability and locality.

*Conclusion.* Hadoop gives a fault-tolerant, scalable platform; cloud services such as EMR provide it on demand with per-second billing.

**Q4 (10 marks). A MapReduce job has 1,000 map tasks of 60 s on 100 map slots, a 120 s shuffle and 50 reduce tasks of 40 s on 25 reduce slots. Compute the job time, speedup and efficiency, and discuss the effect of a straggler and how to improve efficiency.**

*Introduction.* Job time is the sum of the waves of map, the shuffle and the waves of reduce (section 8.4).

*Calculation.*

1. Map waves = 1,000 / 100 = 10, so 10 × 60 = **600 s**.
2. Shuffle = **120 s**.
3. Reduce waves = 50 / 25 = 2, so 2 × 40 = **80 s**.
4. Parallel time = 600 + 120 + 80 = **800 s**.
5. Serial time = 1,000 × 60 + 50 × 40 = **62,000 s**.
6. Speedup = 62,000 / 800 = **77.5**; efficiency = 77.5 / 100 = **77.5%**.

*Straggler.* If one map task in the last wave takes 300 s instead of 60 s, the map stage becomes 9 × 60 + 300 = 840 s and the job 1,040 s. With **speculative execution**, a backup starts when the normal tasks finish (at 600 s) and ends at 660 s, so the job takes 860 s.

*Improvements.* Use a combiner and compression to shrink the shuffle; improve the partitioner or split hot keys against skew; use splits near the block size; schedule for data locality; replace unhealthy nodes; tune the number of reducers.

*Conclusion.* Efficiency loss comes from the shuffle, idle slots in partial waves and stragglers; attack each in turn.
