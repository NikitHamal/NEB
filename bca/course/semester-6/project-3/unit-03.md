---
subject: Project III
grade: BCA Semester 6
unit: 3
title: Storing and Analysing Sensor Data: Cleaning, Anomalies and a Forecast
area: BCA 356 · Project III · Unit 3
---

A sensor project becomes useful only when the stream of numbers is turned into a decision. This unit builds the server side of KhetSense: a time-series table that refuses bad rows, a cleaning step that handles gaps and spikes, a detector that notices a dead or crazy node, and a simple forecast that says whether the farmer should water tomorrow. All data are simulated with fixed seeds and every output below comes from a real run.

::: key What this unit gives you
- A pipeline from message to advice, with a figure, and a SQLite schema that makes inserts safe to repeat.
- A cleaning script: range check, spike flag, short-gap interpolation and long-gap flag.
- A robust anomaly detector and a silent-node alert.
- A drying-curve forecast compared with a naive baseline, and an irrigation rule table.
:::

## 3.1 The pipeline from message to advice

Data should pass through the same steps every time, and each step should be testable on its own.

```svgfig label="3.1" caption="KhetSense data pipeline. A message is validated and stored once; a cleaning step produces a tidy series; analysis finds anomalies and forecasts; the rule engine turns the forecast into plain-word advice for the app."
f = Fig(580, 150)
names = ["Ingest\nmessage", "Validate\nrange, id", "Store\n(SQLite)", "Clean\nseries", "Analyse +\nforecast", "Rule engine\nadvice"]
for i, n in enumerate(names):
    x = 6 + i * 96
    f.box(x, 45, 86, 60, n, fill=(BLUE if i % 2 == 0 else SOFT), stroke=(NAVY if i < 3 else TEAL), size=10, color=NAVY)
    if i < 5:
        f.arrow([(x + 86, 75), (x + 96, 75)], color=NAVY)
f.text(145, 130, "reject bad rows", size=10, color=RED)
f.text(440, 130, "advice in plain words", size=10, color=TEAL)
```

## 3.2 Storing readings safely

A good schema makes wrong data impossible. The table below uses a **primary key on (node, id)** so that a retried message cannot create a duplicate, and a **CHECK** constraint so that an impossible moisture (such as 120 percent) is refused. The script stores seven days of simulated data from three nodes, where 8 percent of messages are lost, and 5 percent of the delivered ones arrive twice because of QoS 1 retries.

```python
import sqlite3, random
random.seed(3)
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE reading(id INTEGER NOT NULL, node INTEGER NOT NULL, ts INTEGER NOT NULL,
                     moisture REAL CHECK(moisture BETWEEN 0 AND 100), PRIMARY KEY(node, id));
CREATE INDEX ix_node_ts ON reading(node, ts);""")
sent = dup = bad = 0
for node in (1, 2, 3):
    for i in range(7 * 96):                      # 96 readings per day for 7 days
        if random.random() < 0.08: continue      # message lost on the way
        m = round(34 - 0.035 * (i % 192) + random.gauss(0, 0.6), 1)
        if node == 3 and i == 100: m = 120.0     # a faulty value
        copies = 2 if random.random() < 0.05 else 1
        for _ in range(copies):
            sent += 1
            try: db.execute("INSERT INTO reading VALUES (?,?,?,?)", (i, node, i * 15, m))
            except sqlite3.IntegrityError as e:
                if "UNIQUE" in str(e): dup += 1
                else: bad += 1
print(f"messages received {sent}, duplicates refused {dup}, out-of-range refused {bad}")
for node, n, first, last in db.execute("SELECT node, COUNT(*), MIN(ts), MAX(ts) FROM reading GROUP BY node"):
    print(f"node {node}: {n} of 672 stored ({100 * (672 - n) / 672:.1f}% missing)")
gap = db.execute("""SELECT node, MAX(ts - prev) / 15 FROM (SELECT node, ts, LAG(ts) OVER (PARTITION BY node ORDER BY ts) AS prev
                    FROM reading) WHERE prev IS NOT NULL GROUP BY node""").fetchall()
print("longest gap in readings (steps between stored rows):", gap)
```
```output
messages received 1923, duplicates refused 78, out-of-range refused 2
node 1: 609 of 672 stored (9.4% missing)
node 2: 615 of 672 stored (8.5% missing)
node 3: 619 of 672 stored (7.9% missing)
longest gap in readings (steps between stored rows): [(1, 3), (2, 3), (3, 3)]
```
## 3.3 Cleaning a series

Stored data still contains gaps and spikes. The cleaning rules should be **written down**, applied in a fixed order, and counted so that the report can say how much data was changed. The rules used here are: (1) discard values outside 0 to 60; (2) flag a value as a spike if it differs from the median of its 5 neighbours by more than 4 robust standard deviations (MAD method); (3) fill gaps of up to 4 missing steps by straight-line interpolation; (4) leave longer gaps as missing and flag them.

```python
import numpy as np, warnings
warnings.filterwarnings("ignore")                # all-NaN windows inside the long gap are expected
rng = np.random.default_rng(21)
n = 96
x = 30 - 0.04 * np.arange(n) + rng.normal(0, 0.5, n)
x[[20, 55, 80]] += [14, -12, 16]                 # three spikes
x[[10, 11, 40, 41, 42, 43, 44, 45, 46, 70]] = np.nan   # short gap, long gap, single gap
x[5] = 250                                       # impossible value

out = x.copy()
bad_range = (out < 0) | (out > 60)
out[bad_range] = np.nan                          # rule 1: range
med = np.array([np.nanmedian(out[max(0, i - 2):i + 3]) for i in range(n)])
res = out - med
mad = np.nanmedian(abs(res - np.nanmedian(res))) * 1.4826
spike = abs(res) > 4 * mad
out[spike] = np.nan                              # rule 2: spikes become missing
filled = 0
i = 0
while i < n:
    if np.isnan(out[i]):
        j = i
        while j < n and np.isnan(out[j]): j += 1
        if (j - i) <= 4 and i > 0 and j < n:     # rule 3: short gap, interpolate
            out[i:j] = np.interp(range(i, j), [i - 1, j], [out[i - 1], out[j]]); filled += j - i
        i = j
    else: i += 1
print(f"range-rejected: {int(bad_range.sum())}, spikes flagged at steps {[int(k) for k in np.where(spike)[0]]}, interpolated points: {filled}")
print(f"still missing (long gaps): {int(np.isnan(out).sum())} of {n}")
truth = 30 - 0.04 * np.arange(n)
ok = ~np.isnan(out)
print(f"mean error of cleaned series vs truth: {np.mean(abs(out[ok] - truth[ok])):.2f} points")
```
```output
range-rejected: 1, spikes flagged at steps [20, 55, 80], interpolated points: 7
still missing (long gaps): 7 of 96
mean error of cleaned series vs truth: 0.35 points
```
**Reading the storage output.** Of 1,923 messages received, 78 were duplicates and were refused by the primary key, and 2 copies of the faulty 120 percent value were refused by the CHECK constraint, so the database holds only valid, unique readings. The three nodes stored 609, 615 and 619 of 672 readings (7.9 to 9.4 percent missing, close to the 8 percent loss set in the simulation), and no gap is longer than three steps, which means at most two readings in a row are missing. Those gaps are short enough to interpolate. In a real project, report the missing percentage per node, because it measures the health of the network.

**Reading the cleaning output.** One impossible value was rejected by the range rule; the three real spikes at steps 20, 55 and 80 were flagged and nothing else was; seven points (the two-step gap, the single gap and the removed values) were filled by interpolation; and the seven-step gap was left missing on purpose. The cleaned series is within 0.35 points of the truth. With a threshold of 3 robust standard deviations the same code also flagged three normal readings, so **the threshold is a design choice** and should be tuned on a day of data and stated in the report.

## 3.4 Anomaly detection and silent nodes

Cleaning handles single bad values. **Anomaly detection** handles a sensor that has gone bad. Three simple rules find most field faults: a node is **silent** if its newest reading is more than 8 steps (2 hours) old; it is **stuck** if its last 12 readings are identical; and it **jumps** if two consecutive readings differ by more than 5 points. The script applies the rules to six simulated nodes at the end of a day.

```python
import numpy as np
rng = np.random.default_rng(4)
T = 96                                            # now = step 96
def day(): return 30 - 0.05 * np.arange(T) + rng.normal(0, 0.4, T)
nodes = {k: day() for k in range(1, 7)}
nodes[4][40:] = 17.3                              # stuck sensor
nodes[5] = nodes[5][:60]                          # went silent at step 60
nodes[6][70] += 18                                # jump (could be rain or fault)
for k, x in nodes.items():
    alerts = []
    if T - len(x) > 8: alerts.append(f"SILENT for {T - len(x)} steps ({(T - len(x)) * 15 // 60} h {(T - len(x)) * 15 % 60} min)")
    if np.ptp(x[-12:]) == 0: alerts.append("STUCK (12 identical readings)")
    if np.max(abs(np.diff(x))) > 5: alerts.append(f"JUMP of {np.max(abs(np.diff(x))):.1f} points")
    print(f"node {k}: {'; '.join(alerts) if alerts else 'ok'}")
```
```output
node 1: ok
node 2: ok
node 3: ok
node 4: STUCK (12 identical readings); JUMP of 10.5 points
node 5: SILENT for 36 steps (9 h 0 min)
node 6: JUMP of 17.8 points
```
A jump is not always a fault: rain really raises soil moisture. So a jump is reported to the owner as a **warning**, and it is suppressed when the weather node reports rain at that time. Combining two sources to explain an anomaly is a good idea for the Project III report.

## 3.5 Forecasting tomorrow's moisture

Soil dries along a smooth curve towards a minimum value, so a simple model fitted on the last 24 readings can predict the next morning. The script simulates 14 days with rain events, then every evening at 18:00 (from day 4) predicts the moisture 48 steps (12 hours) ahead with three methods: **persistence** (tomorrow equals now), a **straight line** through the last 24 readings, and an **exponential drying curve** (a line through the logarithm of moisture minus the 12 percent floor). Rain cannot be predicted from soil data, and a rain jump inside the 6-hour fitting window would spoil the curve, so evenings with rain in either period are left out and reported as a limitation.

```python
import numpy as np
rng = np.random.default_rng(9)
N = 14 * 96
m = np.zeros(N); m[0] = 38
rain = set(rng.choice(range(100, N - 60), 4, replace=False))      # 4 rain events
for i in range(1, N):
    m[i] = m[i - 1] - 0.0045 * (m[i - 1] - 12) + (12 if i in rain else 0)
y = m + rng.normal(0, 0.4, N)                                     # measured values
FLOOR, H = 12, 48
errs = {"persistence": [], "line": [], "exponential": []}
dry_cases = 0
decisions_ok = decisions = 0
for d in range(3, 14):
    i = d * 96 + 72                                               # 18:00
    if i + H >= N: continue
    if any(r in range(i - 24, i + H + 1) for r in rain): continue  # skip rain in the window or the horizon
    dry_cases += 1
    w = y[i - 23:i + 1]; t = np.arange(24)
    p_line = np.polyval(np.polyfit(t, w, 1), 23 + H)
    p_exp = FLOOR + np.exp(np.polyval(np.polyfit(t, np.log(np.maximum(w - FLOOR, 0.5)), 1), 23 + H))
    for k, p in (("persistence", y[i]), ("line", p_line), ("exponential", p_exp)):
        errs[k].append(abs(p - y[i + H]))
    decisions += 1; decisions_ok += (p_exp < 22) == (y[i + H] < 22)
print(f"evaluation cases (no rain in the last 6 h or next 12 h): {dry_cases}")
for k, e in errs.items(): print(f"{k:12s} mean error {np.mean(e):.2f} points, worst {np.max(e):.2f}")
print(f"water / skip advice from the exponential forecast agreed with the real outcome in {decisions_ok} of {decisions} cases")
```
```output
evaluation cases (no rain in the last 6 h or next 12 h): 6
persistence  mean error 1.31 points, worst 2.83
line         mean error 0.74 points, worst 1.94
exponential  mean error 0.58 points, worst 1.45
water / skip advice from the exponential forecast agreed with the real outcome in 6 of 6 cases
```
**Reading the anomaly output.** Nodes 1 to 3 pass. Node 4 is flagged STUCK (and also JUMP, because the stuck value of 17.3 began after the series fell from about 28, a step of 10.5 points), node 5 has been SILENT for 36 steps (9 hours), and node 6 shows a single jump of 17.8 points that the owner must check against the weather node. A real alert system should send at most one message per fault per day, otherwise farmers will mute it.

**Reading the forecast output.** On the six evenings that qualified, persistence had a mean error of 1.31 points, the straight line 0.74 and the exponential curve 0.58 (worst case 1.45). The exponential model wins because soil really dries along a curve that flattens. The water-or-skip advice agreed with the real next-morning outcome on 6 of 6 evenings. **Be honest about the limits:** six cases is a small test, rain was excluded, and the data are simulated. A real report should run the same code on at least 30 days of field data and quote the result with those cautions.

## 3.6 From forecast to advice

Farmers need words, not decimals. The rule engine converts the forecast morning moisture into one of four messages. The thresholds here are **illustrative** and must be set with the agriculture officer for the real crop and soil.

```photogrid label="3.1" cols="2" ratio="1.0" caption="From landscape to rule. (a) Hill terraces in central Nepal: each terrace is a separate plot with its own soil depth and slope, so each needs its own node and its own thresholds. (b) The four advice bands applied to the forecast moisture at 06:00."
@ photo id="bca356/terrace" cap="Terraced hill farms in Nepal"
fit 1.0
focus 0.5 0.45
call 0.5 0.9 0.5 0.7 "One node per terrace"
@ svg cap="Advice bands"
f = Fig(300, 300)
f.box(20, 20, 130, 60, "Above 35:\nskip, soil is wet", fill=BLUE, stroke=NAVY, size=11, color=NAVY)
f.box(20, 90, 130, 60, "25 to 35: fine,\ncheck tomorrow", fill=SOFT, stroke=TEAL, size=11, color=NAVY)
f.box(20, 160, 130, 60, "18 to 25:\nwater soon", fill=SOFT, stroke=AMBER, size=11, color=NAVY)
f.box(20, 230, 130, 60, "Below 18:\nwater now", fill=BLUE, stroke=RED, size=11, color=NAVY)
f.arrow([(150,50),(200,50)], color=NAVY)
f.arrow([(150,120),(200,120)], color=NAVY)
f.arrow([(150,190),(200,190)], color=NAVY)
f.arrow([(150,260),(200,260)], color=NAVY)
f.text(250, 40, "no action", size=10, color=NAVY)
f.text(250, 110, "no action", size=10, color=NAVY)
f.text(250, 180, "notify", size=10, color=AMBER)
f.text(250, 250, "alert", size=10, color=RED)
```

Two safeguards make the advice safe. **Rain override:** if the weather node or forecast shows at least 5 mm of rain in the next 12 hours, "water soon" is changed to "skip, rain expected". **Staleness rule:** if the newest reading is older than 2 hours, the app shows "no recent data" and no advice, because advice from old data is worse than no advice.

## 3.7 Eight uses of data analysis in KhetSense

1. **Water saving.** Comparing readings with the rule shows which days irrigation was not needed. If 4 of 10 mornings were already wet, as in the problem statement, skipping those days saves about 35 percent of the water. The cooperative can then state the saving in litres and rupees.
2. **Early dryness warning.** The drying-curve forecast looks 12 hours ahead, so the farmer is warned in the evening rather than finding wilted plants in the morning. This is the main benefit over simply showing the current value.
3. **Fault detection.** Stuck, silent and jumping nodes are found by simple rules within hours. Without them a dead node shows a flat line for weeks and the farmer trusts a false value.
4. **Network health.** The percentage of missing readings per node shows where Wi-Fi is weak. A node with 20 percent missing may need a better antenna position or a relay node.
5. **Battery planning.** A falling battery-voltage series predicts the day a node will die. The owner replaces the cell during a planned visit instead of losing data during a dry spell.
6. **Crop advice by plot.** Averages per terrace reveal that the upper terraces dry faster than the lower ones. The extension officer can recommend more frequent, lighter watering for them.
7. **Evidence for funding.** A seven-day chart with before and after figures is a stronger proposal to a ward office or an NGO than a promise. Clean data with a stated missing percentage makes the evidence credible.
8. **Teaching and research.** Stored, cleaned data can be shared (without personal details) with the college agriculture department for study. A documented cleaning method lets others repeat and trust the analysis.

```photogrid label="3.2" cols="2" ratio="1.2" caption="Forecasting needs a fair test. (a) A rain gauge records one number a day, and a few months of such numbers are all a farmer has to forecast tomorrow. (b) A synthetic soil-moisture series with a slow 60-day wetting and drying cycle plus noise of 2.5 points (fixed seed) was split in two: the first 60 days chose the smoothing constant (a = 0.5), and the last 60 days, never seen during the choice, were used to score three forecasts by mean absolute error. Copying yesterday gives 2.83 points of error, a 7-day average 2.54 and exponential smoothing 2.5; the best method here is smoothing a=0.50. The series is simulated, so the ranking is a lesson in method, not a claim about real fields: with real KhetSense data the same split must be repeated, and a method that wins only on the data it was tuned on has proved nothing."
@ photo id="bcapj/raingauge" cap="A rain gauge: the daily measurement series begins here"
fit 1.2
focus 0.5 0.5
@ svg cap="Three forecasts on 60 unseen days"
import numpy as np
rng = np.random.default_rng(2081)
n = 120
t = np.arange(n)
y = 30 + 5 * np.sin(2 * np.pi * t / 60) + rng.normal(0, 2.5, n)
def ses(a, alpha):
    s = a[0]
    out = [s]
    for v in a[:-1]:
        s = alpha * v + (1 - alpha) * s
        out.append(s)
    return np.array(out)
mae = lambda p, a: float(np.mean(np.abs(p - a)))
alphas = [i / 20 for i in range(1, 20)]
best_a = min(alphas, key=lambda a: mae(ses(y[:60], a)[1:], y[1:60]))
tr, te = slice(60, n), y[60:]
naive = y[59:n - 1]
ma7 = np.array([y[i - 7:i].mean() for i in range(60, n)])
sm = ses(y, best_a)[60:]
e = {"naive": mae(naive, te), "7-day mean": mae(ma7, te), "smoothing a=%.2f" % best_a: mae(sm, te)}
best = min(e, key=e.get)
assert best.startswith('smoothing')
facts = dict(best=best, e1=round(e["naive"], 2), e2=round(e["7-day mean"], 2), e3=round(list(e.values())[2], 2), a=best_a)
f = Fig(300, 236)
f.text(150, 12, "next-day moisture, mean absolute error", size=10.5, color=NAVY, bold=True)
x0, y0, W, H = 10, 90, 280, 60
for i in range(60, n):
    pass
sc = lambda v: y0 - (v - 20) / 20 * H
for i in range(61, n):
    X0, X1 = x0 + (i - 61) / 59 * W, x0 + (i - 60) / 59 * W
    f.line(X0, sc(y[i - 1]), X1, sc(y[i]), color=NAVY, sw=1.6)
    f.line(X0, sc(naive[i - 61]), X1, sc(naive[i - 60]), color=RED, sw=0.9)
f.text(150, 106, "blue actual, red naive (copy yesterday)", size=10.5, color=SLATE)
vals = list(e.items())
mx = max(e.values())
for i, (k, v) in enumerate(vals):
    yy = 122 + i * 32
    f.text(8, yy + 10, k, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.box(112, yy, v / mx * 130, 22, "", fill="#bbf7d0" if k == best else "#fde68a", stroke=SLATE, r=3, sw=1)
    f.text(118 + v / mx * 130, yy + 11, "%.2f" % v, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
f.text(150, 232, "winner: %s" % best, size=10.5, color=TEAL, bold=True)
```

## Formula and fact sheet

- Primary key (node, id) makes retried inserts harmless; CHECK constraints refuse impossible values.
- MAD-based spike rule: |x − median| > k × 1.4826 × MAD; state k.
- Interpolate short gaps only; leave long gaps missing and flagged.
- Exponential drying: moisture − floor = (m0 − floor) × e^(−k t); fit a line to ln(moisture − floor).
- Compare every forecast with a naive baseline (persistence).

## Chapter summary

- The pipeline validates, stores once, cleans, analyses and then advises; each step is testable.
- Constraints in the database refused 78 duplicates and the impossible value; 8 to 9 percent of readings were missing and recorded as such.
- The cleaning rules flagged exactly the three true spikes and left the long gap missing.
- Stuck, silent and jumping nodes are detected by three simple rules, with rain used to explain jumps.
- The exponential forecast beat persistence (0.58 against 1.31 points) on a small simulated test, and the rule engine turns it into four plain messages.

## Practice

1. Why is `(node, id)` a better primary key than `id` alone?
2. What does the CHECK constraint in the schema prevent?
3. List the four cleaning rules in the order they were applied.
4. Why are long gaps not interpolated?
5. Define a stuck node and a silent node.
6. Why is a jump reported as a warning and not as a fault?
7. Why must a forecast be compared with persistence?
8. A node should report 96 readings a day and stored 84. What percentage is missing?
9. The soil floor is 12, the moisture is 28 and k = 0.0045 per step. Find the moisture after 48 steps.
10. Which advice band applies to a forecast of 22, and what changes if 8 mm of rain is expected?

::: note Answers and worked solutions
**1.** Each node numbers its own readings from 0, so the same id occurs on many nodes; the pair is unique.
**2.** It refuses moisture below 0 or above 100, which are impossible values.
**3.** Range check, spike flag, interpolate short gaps, flag long gaps.
**4.** A long gap hides real events such as rain or irrigation; inventing values would be false data.
**5.** Stuck: the last 12 readings are identical. Silent: no reading for more than 8 steps (2 hours).
**6.** Rain can really raise moisture sharply; the weather node is checked before calling it a fault.
**7.** A model that cannot beat "tomorrow equals now" adds no value.
**8.** (96 − 84) ÷ 96 × 100 = 12.5 percent.
**9.** 12 + (28 − 12) × e^(−0.0045 × 48) = 12 + 16 × 0.8057 = 24.9.
**10.** 18 to 25: "water soon"; with 8 mm of rain (at least 5 mm) the advice becomes "skip, rain expected".
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is data cleaning? Describe the cleaning steps applied to a soil-moisture series, with the results.**

*Introduction.* Data cleaning is the planned process of finding and treating wrong, missing or inconsistent values before analysis. Sensor data always needs it, because noise, loose wires and lost messages are normal in the field.

*Steps in order.*

1. **Range check.** Values outside 0 to 60 percent are impossible and are set to missing. One value of 250 was rejected.
2. **Spike detection.** Each point is compared with the median of its five neighbours; a difference of more than 4 robust standard deviations (MAD method) marks a spike. It flagged the three real spikes at steps 20, 55 and 80 and nothing else.
3. **Short-gap interpolation.** Gaps of up to 4 steps are filled by a straight line between the neighbours; seven points were filled.
4. **Long-gap flagging.** The seven-step gap was left missing and flagged, because inventing data would hide real events.

*Result.* The cleaned series was within 0.35 points of the true values.

*Why record it.* Counting every change makes the cleaning transparent, and the threshold (4 here; 3 gave false flags) is stated so that others can repeat it.

*Conclusion.* Written, ordered and counted cleaning rules turn noisy readings into evidence without hiding the gaps.

**Q2 (5 marks). Explain three rules to detect faulty sensor nodes. Why is one of them reported as a warning only?**

*Introduction.* Single bad values are cleaned, but a whole node can fail. Simple rules, run at the end of each day or every hour, find most field faults without any machine learning.

*The rules.*

1. **Silent node.** The newest reading is more than 8 steps (2 hours) old. Cause: dead battery, lost Wi-Fi or crashed code. In the test, node 5 had been silent for 9 hours.
2. **Stuck node.** The last 12 readings are identical (peak-to-peak range zero). Cause: a frozen program or disconnected probe. Node 4 held 17.3 after step 40.
3. **Jump.** Two consecutive readings differ by more than 5 points. Node 6 showed a 17.8-point jump.

*Why a warning.* A jump can be real: heavy rain can raise moisture quickly. The system therefore checks the weather node and shows a warning unless rain explains it, and the owner decides. Stuck and silent faults are physical impossibilities, so they are reported as faults.

*Conclusion.* Three cheap rules, with rain used as context, detect the main failure types and keep false alarms low enough that farmers keep trusting them.

**Q3 (10 marks). Design the server-side data pipeline of an IoT soil-monitoring system. Explain storage, validation, cleaning, analysis, forecasting and advice, with results from your tests.**

*Introduction.* The server receives small messages from many nodes over an unreliable network and must turn them into safe storage and useful advice. The pipeline of Figure 3.1 does this in six steps, each testable alone. The example is KhetSense with 6 soil nodes.

*1. Ingest and validate.* Messages arrive by MQTT with QoS 1, so duplicates are possible. The server checks that the fields exist and the values are plausible.

*2. Store safely.* A SQLite table has the primary key (node, id) and a CHECK constraint on 0 to 100. In the test, 78 duplicates and the impossible value of 120 were refused automatically. Missing readings (7.9 to 9.4 percent per node) are simply absent, never stored as zero.

*3. Clean.* Range check, MAD spike flag (threshold stated), interpolation of gaps up to 4 steps, flagging of longer gaps. The cleaned series was within 0.35 points of the truth.

*4. Detect anomalies.* Silent, stuck and jump rules find faulty nodes; rain from the weather node explains genuine jumps.

*5. Forecast.* An exponential drying curve fitted on the last 6 hours predicts the moisture 12 hours ahead. On the qualified evenings its mean error was 0.58 points, against 1.31 for persistence and 0.74 for a straight line.

*6. Advise.* The forecast is mapped to four messages (skip, fine, water soon, water now), with a rain override and a staleness rule that withholds advice when data are older than 2 hours.

| Step | Risk handled | Result |
|---|---|---|
| Store | duplicates, bad values | 78 + 2 refused |
| Clean | spikes, gaps | error 0.35 |
| Forecast | late warning | error 0.58 |
| Advise | stale data | no advice after 2 h |

*Limits.* The data are simulated, six test cases are few, and the thresholds must be set with an agriculture officer.

*Conclusion.* A clear, layered server pipeline with constraints, documented cleaning and a baseline-checked forecast makes sensor data trustworthy and the final advice defensible in the viva.
