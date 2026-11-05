---
subject: Cloud Computing
grade: BCA Semester 8
unit: 5
title: Microservices, Kubernetes, Autoscaling and Queueing Theory
hours: 7
area: BCA 451 · Cloud Computing · Unit 5
---

Once capacity is elastic, the application must be built to use it. Large systems are therefore split into small, independently deployed services, packaged as containers and run by an orchestrator that restarts failures and adds replicas when load rises. Whether those replicas arrive in time, and how long requests wait while they do, is not guesswork: it follows from a scaling formula and from queueing theory. This unit covers both the architecture and the arithmetic.

::: key What this unit gives you
- Monolith versus microservices, with the trade-offs and resilience patterns.
- Kubernetes architecture: control plane, nodes, core objects and the reconcile loop.
- The Horizontal Pod Autoscaler formula with a traced example.
- Little's Law, the M/M/1 queue and serverless concurrency.
:::

## 5.1 Monolith to microservices

A **monolith** is one deployable unit: simple to build, test and debug, but it must be scaled, released and failed as a whole. **Microservices** divide the system into small services, each owning its data and a single business capability (orders, payments, catalogue), communicating through APIs or events.

Benefits: independent deployment and scaling, technology freedom, fault isolation, team autonomy. Costs: network calls replace function calls (latency, partial failure), data consistency across services needs patterns such as the **saga** (a sequence of local transactions with compensating actions) rather than one ACID transaction, and operational complexity rises sharply (service discovery, tracing, versioning). A well-factored monolith is often the right start for a small team.

Resilience patterns: **timeouts and retries with exponential backoff and jitter**, **circuit breakers** (stop calling a failing dependency to let it recover), **bulkheads** (separate resource pools so one slow dependency cannot exhaust all threads), an **API gateway** at the edge and a **service mesh** for uniform security and telemetry between services. Observability rests on logs, metrics and distributed traces tied together by a correlation ID.

## 5.2 Kubernetes architecture

**Kubernetes** (K8s) is the standard open-source container orchestrator. A cluster has a **control plane** and a set of **worker nodes**.

- **kube-apiserver:** the front door; every client and component talks to it through a REST API.
- **etcd:** the consistent key-value store (Raft-based) holding all cluster state.
- **kube-scheduler:** assigns unscheduled Pods to nodes by resource requests, affinity, taints and tolerations.
- **kube-controller-manager:** runs control loops (Deployment, ReplicaSet, Node, and others).
- **cloud-controller-manager:** integrates with the provider (load balancers, volumes).
- On each node: **kubelet** (runs Pods and reports status), **kube-proxy** (Service networking rules) and a **container runtime** (containerd or CRI-O).

Core objects: a **Pod** is the smallest unit, one or more containers sharing network and storage; a **ReplicaSet** keeps a number of Pod copies running; a **Deployment** manages ReplicaSets and rolling updates; a **Service** gives a stable virtual IP and DNS name to a changing set of Pods; an **Ingress** routes external HTTP traffic; **ConfigMap** and **Secret** inject configuration; a **StatefulSet** gives stable identity and storage to stateful workloads; a **DaemonSet** runs one Pod per node.

::: key The reconcile loop
Kubernetes is **declarative**. You state the *desired* state (three replicas of this image); controllers continually compare it with the *observed* state and act to close the gap. A crashed Pod is replaced not because someone detects the crash but because the observed count drifted from the declared one.
:::

## 5.3 Horizontal Pod Autoscaler

The **HPA** adjusts the replica count of a Deployment from observed metrics (CPU, memory, or custom metrics). For a target value per Pod, the controller computes:

::: key HPA formula
**desiredReplicas = ⌈ currentReplicas × currentMetric ÷ targetMetric ⌉**, clamped to [minReplicas, maxReplicas]. If the ratio of current to target is within a **tolerance** (default 0.1) of 1.0, no scaling occurs.
:::

Scale-down additionally uses a **stabilization window** (default 300 seconds), taking the highest recommendation in the window to avoid flapping; scale-up is faster by default. The program traces four evaluations for a target average CPU of 60% with bounds 2 to 10 replicas.

```python
target, min_r, max_r = 60, 2, 10
steps = [(4, 90), (6, 30), (3, 63), (3, 300)]
for i, (cur, metric) in enumerate(steps, 1):
    note = ""
    if abs(metric / target - 1) <= 0.10:
        want = cur
        note = " (within 10% tolerance)"
    else:
        want = -(-cur * metric // target)
        if want > max_r:
            note = f", capped at {max_r}"
    print(f"step {i}: {cur} replicas, metric {metric}% vs target {target}% -> desired {want}{note}")
```
```output
step 1: 4 replicas, metric 90% vs target 60% -> desired 6
step 2: 6 replicas, metric 30% vs target 60% -> desired 3
step 3: 3 replicas, metric 63% vs target 60% -> desired 3 (within 10% tolerance)
step 4: 3 replicas, metric 300% vs target 60% -> desired 15, capped at 10
```
Step 1: 4 × 90 ÷ 60 = 6, so the HPA scales out to 6. Step 2: at 6 replicas and 30% load, 6 × 30 ÷ 60 = 3 (scale-in, subject to the stabilization window). Step 3 shows the tolerance: 63% is only 5% above target, so no change, although the raw formula would give ⌈3 × 63 ÷ 60⌉ = 4 replicas and cause constant small changes. Step 4: a spike to 300% asks for 15, but the maximum of 10 caps it.

::: caution
The HPA reacts to *measured* load, so it lags (metrics scrape interval, Pod start time, image pull). Capacity for sudden spikes needs headroom, a higher minimum, or event-driven scaling. The HPA also needs CPU or memory *requests* defined on Pods because utilisation is measured relative to the request.
:::

## 5.4 Little's Law and the M/M/1 queue

**Little's Law** relates the three quantities of any stable system: **L = λ × W**, where L is the average number of items in the system, λ the average arrival rate and W the average time each item spends in the system. It needs no assumptions about the distribution of arrivals or service times, only stability.

The **M/M/1 queue** models one server with Poisson arrivals (rate λ) and exponential service times (rate μ). Utilisation is ρ = λ ÷ μ, and for ρ < 1:

- average number in system L = ρ ÷ (1 − ρ);
- average number waiting Lq = ρ² ÷ (1 − ρ);
- average time in system W = 1 ÷ (μ − λ);
- average waiting time Wq = ρ × W.

```python
lam, mu = 80, 100                       # requests per second arriving, capacity of one worker
rho = lam / mu
L = rho / (1 - rho)
Lq = rho * rho / (1 - rho)
W = 1 / (mu - lam)
Wq = rho * W
print(f"rho {rho:.3f}, L {L:.3f}, Lq {Lq:.3f}, W {W * 1000:.1f} ms, Wq {Wq * 1000:.1f} ms")
print(f"Little check: lambda*W = {lam * W:.3f}")
```
```output
rho 0.800, L 4.000, Lq 3.200, W 50.0 ms, Wq 40.0 ms
Little check: lambda*W = 4.000
```
A worker running at 80% utilisation holds four requests on average, with a mean response time of 50 ms of which 40 ms is waiting; the service time alone is 10 ms. The Little check confirms λ × W = 80 × 0.05 = 4 = L. The curve is nonlinear: raising arrivals to 95 per second (ρ = 0.95) gives L = 19 and W = 200 ms, four times slower for a 19% increase in load. This is why autoscalers target utilisation of 50% to 70%, not 95%.

## 5.5 Serverless and concurrency

In **Function as a Service**, a platform starts a function instance per concurrent request (reusing warm instances), scales to zero when idle, and bills per request and per millisecond of execution. A **cold start** is the delay to create a new execution environment (runtime start, code load, initialisation), ranging from tens of milliseconds to seconds depending on language, package size and VPC attachment. Mitigations include smaller packages, provisioned concurrency and lighter runtimes. Little's Law gives the required concurrency directly: **concurrency = arrival rate × duration**.

```python
rate, dur, limit = 500, 0.2, 1000
conc = rate * dur
print(f"concurrency needed {round(conc)} ({rate} req/s x {dur} s)")
print(f"utilisation of {limit} limit: {conc / limit * 100:.1f}%")
```
```output
concurrency needed 100 (500 req/s x 0.2 s)
utilisation of 1000 limit: 10.0%
```
At 500 requests per second with a 200 ms duration the platform must run 100 instances at once, 10% of a 1,000 default account concurrency limit. Cutting duration to 100 ms halves it. Providers throttle requests above the limit, and the bill is proportional to total execution time, so optimising function duration cuts both cost and concurrency.

::: example Choosing between Kubernetes and serverless
A steady API with predictable load and long-lived connections suits Kubernetes with an HPA. A bursty image-resize job triggered by uploads, idle most of the day, suits functions. Many systems use both.
:::

## 5.6 Seeing the ideas: the cluster, the autoscaler, the monolith and the queue

Queueing theory looks abstract until you stand in a line. Plate 5.1 sets a real ticket queue beside the M/M/1 curve that predicts what happens to waiting time as a server gets busier.

```photogrid label="5.1" cols="2" ratio="1.25" caption="Queues are everywhere. (a) People waiting at ticket counters in a railway station: if arrivals approach the speed at which the counters serve, the line grows without limit. (b) The M/M/1 curve L = rho / (1 - rho): at 80% utilisation a worker holds 4 requests, at 95% it holds 19, so the last few percent of utilisation cost the most waiting."
@ photo id="bca451/queue" cap="Ticket queue at a station"
fit 1.25
focus 0.5 0.5
@ svg cap="Requests in system versus utilisation"
f = Fig(300, 256)
ax = Axes(f, 40, 14, 245, 180, (0, 1), (0, 20))
ax.grid(0.2, 5)
ax.axes("", "")
ax.curve(lambda r: r / (1 - r), 0, 0.955, color=NAVY)
ax.pt(0.8, 4, "rho 0.8: L = 4", dx=-8, dy=-16, anchor="end")
ax.pt(0.95, 19, "rho 0.95: L = 19", dx=-8, dy=4, anchor="end")
f.text(165, 226, "utilisation rho = lambda / mu", size=10, color=SLATE)
f.text(165, 244, "L = average requests in the system", size=10, color=SLATE)
```

```svgfig label="5.1" caption="Kubernetes architecture. The control plane (API server, etcd, scheduler, controller manager) stores desired state and decides placement; each worker node runs a kubelet, kube-proxy and a container runtime that start the Pods. Every component talks to the API server."
f = Fig(580, 250)
f.box(8, 8, 564, 100, "", fill="#f8fafc", stroke=NAVY)
f.text(80, 22, "Control plane", size=10.5, color=NAVY, bold=True)
f.box(150, 34, 130, 36, "kube-apiserver\n(front door, REST)", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(20, 34, 100, 36, "etcd\n(cluster state)", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.box(310, 34, 110, 36, "kube-scheduler\n(pick a node)", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(440, 34, 120, 36, "controller-manager\n(reconcile loops)", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.arrow([(120, 52), (150, 52)], both=True)
f.arrow([(280, 52), (310, 52)], both=True)
f.arrow([(420, 52), (440, 52)], both=True)
f.text(290, 98, "kubectl and CI/CD send desired state here", size=9.5, color=SLATE)
for i, nm in enumerate(["Worker node 1", "Worker node 2", "Worker node 3"]):
    x = 8 + i * 192
    f.box(x, 124, 180, 118, "", fill="#ecfdf5", stroke=TEAL)
    f.text(x + 90, 138, nm, size=10, color=TEAL, bold=True)
    f.box(x + 8, 148, 76, 24, "kubelet", fill=BLUE, stroke=NAVY, size=9.5)
    f.box(x + 96, 148, 76, 24, "kube-proxy", fill=BLUE, stroke=NAVY, size=9.5)
    f.box(x + 8, 178, 164, 20, "container runtime (containerd)", fill=SAND, stroke=AMBER, size=9)
    f.box(x + 8, 204, 50, 30, "Pod", fill=ROSE, stroke=RED, size=9.5)
    f.box(x + 66, 204, 50, 30, "Pod", fill=ROSE, stroke=RED, size=9.5)
    f.box(x + 124, 204, 48, 30, "Pod", fill=ROSE, stroke=RED, size=9.5)
    f.arrow([(x + 90, 124), (215, 108)], dash=True, color=SLATE)
```

```svgfig label="5.2" caption="The Horizontal Pod Autoscaler in action. With a target of 50% CPU, 4 replicas running at 90% give ceil(4 x 90 / 50) = ceil(7.2) = 8 replicas. After the surge, 8 replicas at 30% give ceil(8 x 30 / 50) = ceil(4.8) = 5 replicas. The controller repeats this calculation every cycle."
f = Fig(580, 180)
S = [("Normal", 4, 50, MINT, TEAL), ("Surge: CPU 90%", 4, 90, ROSE, RED), ("After scale-out", 8, 45, MINT, TEAL), ("Quiet: CPU 30%", 8, 30, SAND, AMBER), ("After scale-in", 5, 48, MINT, TEAL)]
for i, (t, n, cpu, fl, st) in enumerate(S):
    x = 8 + i * 114
    f.text(x + 52, 14, t, size=10, color=NAVY, bold=True)
    for k in range(n):
        f.box(x + (k % 4) * 26, 24 + (k // 4) * 30, 22, 24, "", fill=fl, stroke=st)
    f.text(x + 52, 96, "%d Pods" % n, size=10.5, color=st, bold=True)
    f.text(x + 52, 112, "CPU %d%%" % cpu, size=10, color=SLATE)
    if i < 4: f.arrow([(x + 104, 50), (x + 118, 50)])
f.text(290, 144, "desired = ceil( current replicas x current metric / target metric )", size=10.5, color=NAVY, bold=True)
f.text(290, 164, "inside the 0.1 tolerance band around the target, nothing changes", size=10, color=SLATE)
```

```svgfig label="5.3" caption="Monolith versus microservices. The monolith is one deployable unit with one shared database; microservices are separate services with their own data behind an API gateway, and a circuit breaker stops calls to a failing dependency so one fault does not bring down the system."
f = Fig(580, 212)
f.text(100, 14, "Monolith", size=11.5, color=NAVY, bold=True)
f.box(14, 24, 172, 100, "", fill=BLUE, stroke=NAVY)
for i, t in enumerate(["Orders", "Payments", "Catalogue"]):
    f.box(24, 32 + i * 28, 152, 24, t, fill="#ffffff", stroke=NAVY, size=10)
f.box(14, 138, 172, 30, "One shared database", fill=SAND, stroke=AMBER, size=10)
f.text(100, 200, "scale, release and fail together", size=10, color=RED)
f.text(390, 14, "Microservices", size=11.5, color=NAVY, bold=True)
f.box(220, 78, 76, 36, "API\ngateway", fill=BLUE, stroke=NAVY, bold=True, size=10)
for i, t in enumerate(["Orders", "Payments", "Catalogue"]):
    y = 26 + i * 52
    f.box(340, y, 90, 30, t, fill=MINT, stroke=TEAL, size=10)
    f.box(460, y, 108, 30, "own database", fill=SAND, stroke=AMBER, size=9.5)
    f.arrow([(296, 96), (340, y + 15)])
    f.arrow([(430, y + 15), (460, y + 15)])
f.box(300, 160, 150, 26, "circuit breaker opens on failure", fill=ROSE, stroke=RED, size=9)
f.text(480, 200, "scale and release independently", size=10, color=TEAL)
```

### 5.6.1 Eight benefits of Kubernetes for cloud applications

1. **Self-healing.** If a container or a node fails, Kubernetes starts replacements automatically because the observed state no longer matches the declared state. A payment service stays up without a person watching it at night. Health checks also restart containers that hang.
2. **Automatic scaling.** The Horizontal Pod Autoscaler adds Pods when load rises and removes them when it falls. A ticket-booking site for a festival can grow within minutes. Nodes can be added by a cluster autoscaler as well.
3. **Rolling updates and rollbacks.** A Deployment replaces old Pods with new ones gradually, so users see no downtime. If the new version fails its checks, one command returns to the old version. Releases become routine instead of risky.
4. **Service discovery and load balancing.** A Service gives a stable name and address to a changing set of Pods. Other services call it by name and traffic is spread across the healthy Pods. Developers do not track individual IP addresses.
5. **Declarative configuration.** The whole system is described in YAML files that can be stored in Git and reviewed. The same files rebuild the system in another region. This is the idea of infrastructure as code.
6. **Efficient resource use.** The scheduler packs Pods onto nodes by their CPU and memory requests, so servers are well filled. Fewer machines are needed for the same work. Namespaces and quotas stop one team from taking everything.
7. **Portability.** The same manifests run on any major cloud and on a college's own servers. A company can move from one provider to another with much less rework. This reduces vendor lock-in.
8. **Rich ecosystem.** Tools for monitoring, logging, service mesh, secrets and CI/CD plug into Kubernetes. Skills learnt for one project apply to many employers. Open standards keep the knowledge useful for years.

```photogrid label="5.2" cols="2" ratio="1.2" caption="Scaling without flapping. (a) Turnstiles at a metro station: staff open more gates when the queue grows, but do not close them the moment it shortens. (b) The Kubernetes autoscaler rule, desired pods = ceil(current pods x current CPU / target CPU), was run for 12 minutes of a spiky load (200 to 1,400 requests a second; a pod is assumed to serve 100 a second at full CPU; the target is 50 per cent). Reacting to every minute changes the pod count 10 times, while keeping the highest recommendation of the last three minutes before scaling down changes it only 6 times with the same peak of 29 pods; both react immediately to growth. The minutes above 80 per cent CPU in the stabilised run, 3, show the price of scaling up one minute late. All load numbers are invented for the exercise."
@ photo id="bcacloud/turnstile" cap="Turnstiles: open more gates when the queue grows"
fit 1.2
focus 0.5 0.5
@ svg cap="Autoscaler with and without a cool-down"
import math
load = [200, 200, 500, 900, 1400, 1400, 1100, 600, 300, 800, 300, 200]
CAP, TARGET = 100.0, 50.0
def run(window):
    pods = 2
    rec = []
    out = []
    for L in load:
        cpu = L / (pods * CAP) * 100
        want = max(1, math.ceil(pods * cpu / TARGET))
        rec.append(want)
        pods = max(rec[-window:]) if want < pods else want
        out.append((pods, cpu))
    return out
a = run(1)
b = run(3)
chg = lambda o: sum(1 for i in range(1, len(o)) if o[i][0] != o[i - 1][0])
ca, cb = chg(a), chg(b)
assert cb < ca and max(p for p, _ in a) == max(p for p, _ in b)
over = sum(1 for p, c in b if c > 80)
facts = dict(peak=max(p for p, _ in b), ca=ca, cb=cb, over=over)
f = Fig(300, 236)
f.text(150, 12, "load (req/s) and pods per minute, target 50% CPU", size=10.5, color=NAVY, bold=True)
x0, y0, W, H = 24, 130, 262, 92
bw = W / 12
for i, L in enumerate(load):
    h = L / 1400 * H
    f.box(x0 + i * bw + 1, y0 - h, bw - 2, h, "", fill="#e5e7eb", stroke="#94a3b8", r=0, sw=0.5)
def steps(o, col, sw, dy):
    for i in range(12):
        yy = y0 - o[i][0] / 32 * H + dy
        f.line(x0 + i * bw, yy, x0 + (i + 1) * bw, yy, color=col, sw=sw)
        if i:
            yp = y0 - o[i - 1][0] / 32 * H + dy
            f.line(x0 + i * bw, yp, x0 + i * bw, yy, color=col, sw=sw)
steps(a, RED, 1.4, 0)
steps(b, NAVY, 2.4, 0)
f.line(x0, y0, x0 + W, y0, color=SLATE)
f.text(150, 146, "minutes 1 to 12", size=10.5, color=SLATE)
f.text(150, 166, "red: no cool-down, %d scale changes" % ca, size=10.5, color=RED, bold=True)
f.text(150, 184, "blue: 3-min cool-down, %d changes" % cb, size=10.5, color=NAVY, bold=True)
f.text(150, 204, "peak %d pods; minutes above 80%% CPU: %d" % (max(p for p, _ in b), over), size=10.5, color=TEAL, bold=True)
f.text(150, 222, "pods = ceil(pods x CPU / target)", size=10.5, color=SLATE)
```

## 5.7 Summary and exercises

Microservices trade simplicity for independence; Kubernetes reconciles desired and observed state; the HPA scales replicas by ⌈current × metric ÷ target⌉ within tolerance and bounds; Little's Law and M/M/1 show why queues explode near full utilisation, and give serverless concurrency directly.

1. List the control-plane components of Kubernetes and the role of each.
2. Apply the HPA formula: 5 replicas, CPU 84%, target 70%, bounds 2 to 12. What is the outcome? What if CPU is 74%?
3. Explain why the HPA has a tolerance and a scale-down stabilization window.
4. For λ = 45 req/s and μ = 50 req/s compute ρ, L and W for M/M/1.
5. A function runs 300 ms at 200 invocations per second. What concurrency is needed?
6. Give two advantages and two disadvantages of microservices for a five-person team.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Compare monolithic and microservice architectures.**

*Introduction.* A monolith is one deployable unit; microservices split the system into small services that each own one business capability and their data (Figure 5.3).

| Point | Monolith | Microservices |
|---|---|---|
| Deployment | One unit, whole release | Each service separately |
| Scaling | Whole application | Only the busy service |
| Fault isolation | One bug can stop all | Failure contained |
| Technology | One stack | Different stack per service |
| Data | One shared database | Database per service |
| Complexity | Simple to build and debug | Network calls, distributed tracing |
| Best for | Small teams, early stage | Large teams, fast-changing systems |

*Resilience patterns.* Timeouts, retries with backoff, circuit breakers, bulkheads and an API gateway keep one slow service from bringing down others. *Example:* an online shop can scale only the catalogue service during a Dashain sale. *Conclusion:* start with a well-structured monolith and split into microservices when team size and scale demand it.

**Q2 (5 marks). Explain the Horizontal Pod Autoscaler with a calculation.**

The **HPA** changes the number of Pod replicas of a Deployment from observed metrics such as CPU use, using

**desiredReplicas = ceil( currentReplicas x currentMetric / targetMetric )**

clamped between minReplicas and maxReplicas. No change is made while the ratio is within a tolerance of 0.1 of 1.0, which avoids flapping (Figure 5.2).

*Calculation.* A web Deployment has 4 replicas, a target of 50% CPU and a measured average of 90%. Desired = ceil(4 x 90 / 50) = ceil(7.2) = **8**. After the surge, 8 replicas at 30% give ceil(8 x 30 / 50) = ceil(4.8) = **5**. A stabilisation window delays scale-in so a short dip does not remove Pods too early. *Conclusion:* the HPA keeps the metric near its target, matching capacity to demand automatically.

**Q3 (5 marks). State Little's Law and analyse an M/M/1 queue with arrival rate 90 requests/s and service rate 100 requests/s.**

**Little's Law:** L = lambda x W for any stable system, where L is the average number in the system, lambda the arrival rate and W the average time spent in it. It needs no assumption about the arrival pattern.

*M/M/1 results.* Utilisation rho = lambda / mu = 90 / 100 = 0.9. Average number in system L = rho / (1 - rho) = 0.9 / 0.1 = **9**. Waiting in queue Lq = rho^2 / (1 - rho) = 0.81 / 0.1 = **8.1**. Time in system W = 1 / (mu - lambda) = 1 / 10 = **0.1 s = 100 ms**. Waiting time Wq = rho x W = **90 ms**. Check: lambda x W = 90 x 0.1 = 9 = L.

Compared with the book's 80% case (L = 4, W = 50 ms), a 12.5% rise in load doubles the response time (Plate 5.1). *Conclusion:* keep utilisation well below 100%, usually below 70 to 80%, and scale out before the curve turns steep.

**Q4 (10 marks). Explain Kubernetes: its architecture, main objects and the reconcile loop. Compare it with serverless for running cloud workloads.**

*Introduction.* **Kubernetes** (K8s) is an open-source container orchestrator that schedules containers on a cluster, keeps them healthy, scales them and exposes them as services. It grew from Google's internal system Borg and is now the industry standard.

*Architecture (Figure 5.1).* The **control plane** has the *kube-apiserver* (the REST front door), *etcd* (consistent store of cluster state), the *scheduler* (chooses a node for each new Pod from resource requests, affinity and taints) and the *controller manager* (runs control loops). Each **worker node** runs a *kubelet* (starts and watches Pods), *kube-proxy* (Service networking rules) and a container runtime such as containerd.

*Core objects.* A **Pod** is the smallest unit: one or more containers sharing network and storage. A **ReplicaSet** keeps a set number of Pods running. A **Deployment** manages ReplicaSets and rolling updates. A **Service** gives a stable address to changing Pods. An **Ingress** routes external HTTP traffic. **ConfigMaps** and **Secrets** hold configuration; **PersistentVolumes** hold data.

*Reconcile loop.* Kubernetes is declarative: you state the desired state (three replicas) and controllers repeatedly compare it with the observed state and act. A crashed Pod is replaced because the count drifted, not because someone detected the crash. The HPA adds scaling: 4 Pods at 90% CPU with a 50% target become ceil(7.2) = 8 (Figure 5.2).

| Point | Kubernetes | Serverless (FaaS) |
|---|---|---|
| Unit | Container Pod | Function |
| Servers | You manage cluster size | None to manage |
| Scaling | HPA, minutes | Per request, seconds, to zero |
| Billing | Nodes while running | Per request and millisecond |
| Cold start | Rare | Present |
| Best for | Steady APIs, long connections | Bursty, event-driven jobs |

*Benefits.* Self-healing, autoscaling, rolling updates, service discovery, declarative configuration, efficient packing, portability and ecosystem (see the eight points above). *Limitations.* Operational complexity and learning curve; small projects may prefer a managed platform. *Conclusion.* Kubernetes turns a fleet of machines into one programmable platform driven by desired state; many systems use it for steady services and serverless for bursty jobs.
