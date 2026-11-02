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

## 5.6 Summary and exercises

Microservices trade simplicity for independence; Kubernetes reconciles desired and observed state; the HPA scales replicas by ⌈current × metric ÷ target⌉ within tolerance and bounds; Little's Law and M/M/1 show why queues explode near full utilisation, and give serverless concurrency directly.

1. List the control-plane components of Kubernetes and the role of each.
2. Apply the HPA formula: 5 replicas, CPU 84%, target 70%, bounds 2 to 12. What is the outcome? What if CPU is 74%?
3. Explain why the HPA has a tolerance and a scale-down stabilization window.
4. For λ = 45 req/s and μ = 50 req/s compute ρ, L and W for M/M/1.
5. A function runs 300 ms at 200 invocations per second. What concurrency is needed?
6. Give two advantages and two disadvantages of microservices for a five-person team.
