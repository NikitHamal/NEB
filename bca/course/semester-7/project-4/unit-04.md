---
subject: Project IV
grade: BCA Semester 7
unit: 4
title: Deployment: Serving, Testing, Monitoring Drift and Privacy
area: BCA 404 · Project IV · Unit 4
---

A model in a notebook helps nobody. A teacher cannot open a notebook, and no one will notice when it quietly goes wrong next semester. This unit turns the Unit 3 model into a small **service**, protects it with **automated tests**, adds a **drift monitor** that tells the college when to worry, and sets out the **privacy rules** that a system about students must follow. Everything runs with Python and NumPy only, so that you can reproduce it on a laptop.

::: key What this unit gives you
- How to save a model as a small JSON file and wrap it in a `predict` function that **validates its input**.
- A suite of eight automated tests with real PASS lines.
- A drift monitor using the **population stability index (PSI)**, run on three new batches: no drift, covariate drift, and concept drift.
- A privacy and security checklist, deployment options for a college, and eight deployment habits.
:::

## 4.1 From notebook to service

A deployed model needs three things: the **artefact** (weights, scaling numbers, threshold, version), a **function** that applies them exactly as in training, and **guards** that refuse bad input. The JSON file below is the artefact. It is human-readable, tiny and carries the means and standard deviations learned from the training rows, so the service scales new students in the same way.

```python
import numpy as np
rng = np.random.default_rng(404)
n = 600
ability = rng.normal(0, 1, n)
attend = np.clip(78 + 4.5*ability + rng.normal(0, 10, n), 30, 100)
internal = np.clip(24 + 5*ability + 0.08*(attend-78) + rng.normal(0, 3.5, n), 0, 40)
assign = np.clip(80 + 6*ability + rng.normal(0, 14, n), 0, 100)
gpa = np.clip(2.9 + 0.45*ability + rng.normal(0, 0.3, n), 1.5, 4.0)
commute = rng.gamma(2.0, 20, n)
valley = rng.random(n) < 0.6
z = -2.0 - 0.05*(attend-78) - 0.18*(internal-24) - 0.01*(assign-80) - 0.8*(gpa-2.9) + 0.006*(commute-40)
risk = rng.random(n) < 1/(1+np.exp(-z))
X = np.column_stack([attend, internal, assign, gpa, commute])
y = risk.astype(int)
rs = np.random.default_rng(11)
tr, va, te = [], [], []
for cls in (0, 1):
    idx = rs.permutation(np.where(y == cls)[0])
    a, b = int(0.6 * len(idx)), int(0.8 * len(idx))
    tr += list(idx[:a]); va += list(idx[a:b]); te += list(idx[b:])
tr, va, te = map(np.array, (tr, va, te))
mu, sd = X[tr].mean(axis=0), X[tr].std(axis=0)
Z = (X - mu) / sd
def sigmoid(t): return 1 / (1 + np.exp(-t))
def fit(Z, y, lr=0.2, steps=400, l2=0.0, log=None):
    w = np.zeros(Z.shape[1]); b = 0.0
    for i in range(steps):
        p = sigmoid(Z @ w + b); g = p - y
        if log is not None and i in log:
            loss = -np.mean(y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12))
            print(f"step {i:3d}  loss {loss:.4f}")
        w -= lr * (Z.T @ g / len(y) + l2 * w); b -= lr * g.mean()
    return w, b
def auc(score, label):
    order = np.argsort(score)
    ranks = np.empty(len(score)); ranks[order] = np.arange(1, len(score) + 1)
    pos = label == 1
    return (ranks[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (~pos).sum())
import json, os, tempfile, time
w, b = fit(Z[tr], y[tr])
model = {"version": "2026.1", "features": ["attendance", "internal", "assignment", "prev_gpa", "commute"],
         "mean": mu.round(4).tolist(), "std": sd.round(4).tolist(), "weights": w.round(5).tolist(),
         "bias": round(float(b), 5), "threshold": 0.40}
path = os.path.join(tempfile.mkdtemp(), "model.json")
json.dump(model, open(path, "w"), indent=1)
print("saved", os.path.basename(path), os.path.getsize(path), "bytes; keys:", sorted(model))
M = json.load(open(path))
RANGES = {"attendance": (0, 100), "internal": (0, 40), "assignment": (0, 100), "prev_gpa": (0, 4), "commute": (0, 240)}
def predict(rec, M=M):
    for k in M["features"]:
        if k not in rec: return {"error": f"missing field: {k}"}
        lo, hi = RANGES[k]
        if not (lo <= rec[k] <= hi): return {"error": f"{k} out of range [{lo}, {hi}]: {rec[k]}"}
    x = (np.array([rec[k] for k in M["features"]]) - M["mean"]) / M["std"]
    p = float(sigmoid(x @ np.array(M["weights"]) + M["bias"]))
    return {"risk": round(p, 3), "flag": p >= M["threshold"], "model": M["version"]}
print(predict({"attendance": 55, "internal": 12, "assignment": 40, "prev_gpa": 2.0, "commute": 90}))
print(predict({"attendance": 92, "internal": 33, "assignment": 95, "prev_gpa": 3.6, "commute": 20}))
print(predict({"attendance": 120, "internal": 30, "assignment": 80, "prev_gpa": 3.0, "commute": 30}))
print(predict({"attendance": 80, "internal": 30}))
recs = [dict(zip(M["features"], map(float, r))) for r in X[:400]]
t0 = time.perf_counter()
for r in recs * 3: predict(r)
ms = (time.perf_counter() - t0) / (len(recs) * 3) * 1000
print("served", len(recs) * 3, "predictions; mean latency below 1 ms:", ms < 1.0)
```
```output
saved model.json 361 bytes; keys: ['bias', 'features', 'mean', 'std', 'threshold', 'version', 'weights']
{'risk': 0.905, 'flag': True, 'model': '2026.1'}
{'risk': 0.004, 'flag': False, 'model': '2026.1'}
{'error': 'attendance out of range [0, 100]: 120'}
{'error': 'missing field: assignment'}
served 1200 predictions; mean latency below 1 ms: True
```

*Reading the output.* The model file is only 361 bytes and holds seven keys. The first student (attendance 55, internal marks 12, assignment 40, GPA 2.0) gets a risk of **0.905** and is flagged; the second (attendance 92, internal 33, assignment 95, GPA 3.6) gets **0.004** and is not. The third request has an attendance of 120 and the fourth lacks four fields, and both are **rejected with a clear message** instead of silently producing a number. A mean latency below 1 millisecond over 1,200 predictions easily meets objective O5 (under 100 ms). The exact time depends on the machine, so the script prints only whether it is below the limit.

Each reply carries the **model version** (2026.1). When a student asks "why was I flagged?" or when results change after retraining, the version tells the team which model produced which answer.

```svgfig label="4.1" caption="Life of one prediction request. The service validates the record, scales it with the stored means and deviations, scores it with the stored weights, compares it with the threshold and returns the risk, the flag and the model version. Every request is logged without names."
f = Fig(580, 215)
f.box(8, 80, 88, 56, "Request\nJSON record", fill=BLUE, stroke=NAVY, size=10.5, color=NAVY)
f.box(116, 80, 88, 56, "1 Validate\nrange, fields", fill=SOFT, stroke=RED, size=10.5, color=NAVY)
f.box(224, 80, 88, 56, "2 Scale\nz-score", fill=SOFT, stroke=TEAL, size=10.5, color=NAVY)
f.box(332, 80, 88, 56, "3 Score\nsigmoid", fill=SOFT, stroke=AMBER, size=10.5, color=NAVY)
f.box(440, 80, 130, 56, "4 Reply\nrisk, flag, version", fill=BLUE, stroke=NAVY, size=10.5, color=NAVY)
for x in (96, 204, 312, 420):
    f.arrow([(x, 108), (x + 20, 108)], color=NAVY)
f.box(224, 6, 196, 40, "model.json: mean, std,\nweights, bias, threshold", fill="#fde68a", stroke=AMBER, size=10, color=NAVY)
f.arrow([(322, 46), (268, 80)], color=AMBER)
f.arrow([(322, 46), (376, 80)], color=AMBER)
f.box(116, 165, 130, 36, "error: 400 + message", fill="#fecaca", stroke=RED, size=10, color=NAVY)
f.arrow([(160, 136), (160, 165)], color=RED)
f.box(380, 165, 190, 36, "log: time, version, risk (no names)", fill=SOFT, stroke=NAVY, size=10, color=NAVY)
f.arrow([(505, 136), (505, 165)], color=NAVY)
```

```photogrid label="4.1" cols="2" ratio="1.1" caption="Where a capstone service can live. (a) A technician at a server rack: a college server room is one option, and the person responsible for it must be told about the project's privacy rules. (b) Three deployment levels for SikshyaSignal, from a laptop demo to a college server to a free cloud tier, with the privacy risk and effort of each."
@ photo id="bca306/tech" cap="Technician at a server rack"
fit 1.1
focus 0.5 0.5
call 0.5 0.85 0.5 0.65 "college server room"
@ svg cap="Three deployment levels"
f = Fig(300, 270)
f.box(20, 10, 260, 70, "1 Laptop demo\nlocalhost, simulated data\neffort low, privacy risk none", fill=BLUE, stroke=NAVY, size=11, color=NAVY)
f.box(20, 100, 260, 70, "2 College server\nsystemd service, real data\nIT admin, backups, access list", fill=SOFT, stroke=TEAL, size=11, color=NAVY)
f.box(20, 190, 260, 70, "3 Free cloud tier\nonly with consent and\nno personal data leaving Nepal", fill="#fde68a", stroke=AMBER, size=11, color=NAVY)
f.arrow([(150, 80), (150, 100)], color=NAVY)
f.arrow([(150, 170), (150, 190)], color=NAVY)
```

## 4.2 Automated tests: eight checks that run in a second

Tests are what separate a service from a script. They run in a second, catch mistakes immediately and, in the defence, prove that the student has thought about failure. The eight tests below cover the model maths, the saved file, the guards and the expected direction of the model's behaviour. Each yields one `PASS` or `FAIL` line.

```python
import numpy as np
rng = np.random.default_rng(404)
n = 600
ability = rng.normal(0, 1, n)
attend = np.clip(78 + 4.5*ability + rng.normal(0, 10, n), 30, 100)
internal = np.clip(24 + 5*ability + 0.08*(attend-78) + rng.normal(0, 3.5, n), 0, 40)
assign = np.clip(80 + 6*ability + rng.normal(0, 14, n), 0, 100)
gpa = np.clip(2.9 + 0.45*ability + rng.normal(0, 0.3, n), 1.5, 4.0)
commute = rng.gamma(2.0, 20, n)
valley = rng.random(n) < 0.6
z = -2.0 - 0.05*(attend-78) - 0.18*(internal-24) - 0.01*(assign-80) - 0.8*(gpa-2.9) + 0.006*(commute-40)
risk = rng.random(n) < 1/(1+np.exp(-z))
X = np.column_stack([attend, internal, assign, gpa, commute])
y = risk.astype(int)
rs = np.random.default_rng(11)
tr, va, te = [], [], []
for cls in (0, 1):
    idx = rs.permutation(np.where(y == cls)[0])
    a, b = int(0.6 * len(idx)), int(0.8 * len(idx))
    tr += list(idx[:a]); va += list(idx[a:b]); te += list(idx[b:])
tr, va, te = map(np.array, (tr, va, te))
mu, sd = X[tr].mean(axis=0), X[tr].std(axis=0)
Z = (X - mu) / sd
def sigmoid(t): return 1 / (1 + np.exp(-t))
def fit(Z, y, lr=0.2, steps=400, l2=0.0, log=None):
    w = np.zeros(Z.shape[1]); b = 0.0
    for i in range(steps):
        p = sigmoid(Z @ w + b); g = p - y
        if log is not None and i in log:
            loss = -np.mean(y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12))
            print(f"step {i:3d}  loss {loss:.4f}")
        w -= lr * (Z.T @ g / len(y) + l2 * w); b -= lr * g.mean()
    return w, b
def auc(score, label):
    order = np.argsort(score)
    ranks = np.empty(len(score)); ranks[order] = np.arange(1, len(score) + 1)
    pos = label == 1
    return (ranks[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (~pos).sum())
import json, os, tempfile
w, b = fit(Z[tr], y[tr])
model = {"version": "2026.1", "features": ["attendance", "internal", "assignment", "prev_gpa", "commute"],
         "mean": mu.round(4).tolist(), "std": sd.round(4).tolist(), "weights": w.round(5).tolist(),
         "bias": round(float(b), 5), "threshold": 0.40}
path = os.path.join(tempfile.mkdtemp(), "model.json")
json.dump(model, open(path, "w"), indent=1)
M = json.load(open(path))
RANGES = {"attendance": (0, 100), "internal": (0, 40), "assignment": (0, 100), "prev_gpa": (0, 4), "commute": (0, 240)}
def predict(rec, M=M):
    for k in M["features"]:
        if k not in rec: return {"error": f"missing field: {k}"}
        lo, hi = RANGES[k]
        if not (lo <= rec[k] <= hi): return {"error": f"{k} out of range [{lo}, {hi}]: {rec[k]}"}
    x = (np.array([rec[k] for k in M["features"]]) - M["mean"]) / M["std"]
    p = float(sigmoid(x @ np.array(M["weights"]) + M["bias"]))
    return {"risk": round(p, 3), "flag": p >= M["threshold"], "model": M["version"]}
good = {"attendance": 70, "internal": 20, "assignment": 70, "prev_gpa": 2.8, "commute": 40}
def tests():
    yield "sigmoid(0) is 0.5", sigmoid(0.0) == 0.5
    yield "risk is between 0 and 1 for 600 students", all(0 <= predict(dict(zip(M["features"], map(float, r))))["risk"] <= 1 for r in X)
    yield "saved model matches in-memory weights", np.allclose(M["weights"], w, atol=1e-4)
    yield "more attendance lowers risk", predict({**good, "attendance": 95})["risk"] < predict({**good, "attendance": 50})["risk"]
    yield "higher internal marks lower risk", predict({**good, "internal": 35})["risk"] < predict({**good, "internal": 8})["risk"]
    yield "out-of-range attendance is rejected", "error" in predict({**good, "attendance": 130})
    yield "missing field is rejected", "error" in predict({"attendance": 70})
    yield "same input gives the same answer", predict(good) == predict(good)
passed = 0
for name, ok in tests():
    passed += bool(ok)
    print("PASS" if ok else "FAIL", "-", name)
print(f"{passed} of 8 tests passed")
```
```output
PASS - sigmoid(0) is 0.5
PASS - risk is between 0 and 1 for 600 students
PASS - saved model matches in-memory weights
PASS - more attendance lowers risk
PASS - higher internal marks lower risk
PASS - out-of-range attendance is rejected
PASS - missing field is rejected
PASS - same input gives the same answer
8 of 8 tests passed
```

*Reading the output.* All 8 tests pass. Three of them deserve attention. The **"more attendance lowers risk"** and **"higher internal marks lower risk"** tests are *behaviour* tests: they check that the model moves in the sensible direction, which would fail if a sign were flipped or the scaling were forgotten. The **round-trip test** compares the saved weights with the in-memory ones, so a bug in saving or loading shows up. The two **rejection tests** protect the service from bad data. Add one new test every time a bug is found; the test suite is the memory of everything that has gone wrong.

## 4.3 Monitoring: how the college knows when the model is going stale

A model is trained on last year's students, but it works on next year's. When the new students differ, the model can fail silently. Two different problems hide under the word **drift**.

- **Covariate drift:** the *inputs* change. After a term of online classes, attendance is lower and more spread out. The model sees unfamiliar inputs.
- **Concept drift:** the *relationship* between inputs and outcome changes. Perhaps students now log in but do not engage, so attendance no longer predicts failure.

Inputs can be watched at once, because they arrive every day. The common tool is the **population stability index (PSI)**: cut the training values into ten equal-count bins, count the share of new values in each bin, and add up (new share − old share) × ln(new share ÷ old share). A rule of thumb: **PSI below 0.1 is stable, 0.1 to 0.25 deserves a look, above 0.25 means a major shift**. Outcomes (who actually failed) arrive only at the end of the term, so performance can be checked only then.

The script simulates three new batches of 300 students and prints the PSI of each feature and the model's performance, using the frozen Unit 3 weights and threshold 0.40.

```python
import numpy as np
rng = np.random.default_rng(404)
n = 600
ability = rng.normal(0, 1, n)
attend = np.clip(78 + 4.5*ability + rng.normal(0, 10, n), 30, 100)
internal = np.clip(24 + 5*ability + 0.08*(attend-78) + rng.normal(0, 3.5, n), 0, 40)
assign = np.clip(80 + 6*ability + rng.normal(0, 14, n), 0, 100)
gpa = np.clip(2.9 + 0.45*ability + rng.normal(0, 0.3, n), 1.5, 4.0)
commute = rng.gamma(2.0, 20, n)
valley = rng.random(n) < 0.6
z = -2.0 - 0.05*(attend-78) - 0.18*(internal-24) - 0.01*(assign-80) - 0.8*(gpa-2.9) + 0.006*(commute-40)
risk = rng.random(n) < 1/(1+np.exp(-z))
X = np.column_stack([attend, internal, assign, gpa, commute])
y = risk.astype(int)
rs = np.random.default_rng(11)
tr, va, te = [], [], []
for cls in (0, 1):
    idx = rs.permutation(np.where(y == cls)[0])
    a, b = int(0.6 * len(idx)), int(0.8 * len(idx))
    tr += list(idx[:a]); va += list(idx[a:b]); te += list(idx[b:])
tr, va, te = map(np.array, (tr, va, te))
mu, sd = X[tr].mean(axis=0), X[tr].std(axis=0)
Z = (X - mu) / sd
def sigmoid(t): return 1 / (1 + np.exp(-t))
def fit(Z, y, lr=0.2, steps=400, l2=0.0, log=None):
    w = np.zeros(Z.shape[1]); b = 0.0
    for i in range(steps):
        p = sigmoid(Z @ w + b); g = p - y
        if log is not None and i in log:
            loss = -np.mean(y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12))
            print(f"step {i:3d}  loss {loss:.4f}")
        w -= lr * (Z.T @ g / len(y) + l2 * w); b -= lr * g.mean()
    return w, b
def auc(score, label):
    order = np.argsort(score)
    ranks = np.empty(len(score)); ranks[order] = np.arange(1, len(score) + 1)
    pos = label == 1
    return (ranks[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (~pos).sum())
def make(m, seed, att_shift=0.0, extra=0.0, ac=0.05, sc=0.01):
    r = np.random.default_rng(seed)
    ab = r.normal(0, 1, m)
    at = np.clip(78 + att_shift + 4.5*ab + r.normal(0, 10 + extra, m), 30, 100)
    it = np.clip(24 + 5*ab + 0.08*(at-78) + r.normal(0, 3.5, m), 0, 40)
    asg = np.clip(80 + 6*ab + r.normal(0, 14, m), 0, 100)
    gp = np.clip(2.9 + 0.45*ab + r.normal(0, 0.3, m), 1.5, 4.0)
    cm = r.gamma(2.0, 20, m)
    zz = -2.0 - ac*(at-78) - 0.18*(it-24) - sc*(asg-80) - 0.8*(gp-2.9) + 0.006*(cm-40)
    return np.column_stack([at, it, asg, gp, cm]), (r.random(m) < 1/(1+np.exp(-zz))).astype(int)
def psi(a, bb, bins=10):
    edges = np.quantile(a, np.linspace(0, 1, bins + 1)); edges[0], edges[-1] = -np.inf, np.inf
    pa = np.histogram(a, edges)[0] / len(a); pb = np.histogram(bb, edges)[0] / len(bb)
    pa, pb = np.clip(pa, 1e-4, None), np.clip(pb, 1e-4, None)
    return float(np.sum((pb - pa) * np.log(pb / pa)))
w, b = fit(Z[tr], y[tr])
batches = {"same-year batch": make(300, 21), "online-term batch": make(300, 22, att_shift=-9, extra=4),
           "online + new behaviour": make(300, 23, att_shift=-9, extra=4, ac=0.0, sc=0.05)}
feat = ["attendance", "internal", "assignment", "prev_gpa", "commute"]
for nm, (Xn, yn) in batches.items():
    p = sigmoid(((Xn - mu) / sd) @ w + b)
    flag = p >= 0.40
    print(f"== {nm}: actual fail rate {yn.mean():.1%}, mean predicted risk {p.mean():.1%}")
    print("   PSI:", {k: round(psi(X[tr][:, j], Xn[:, j]), 3) for j, k in enumerate(feat)})
    print(f"   AUC {auc(p, yn):.3f}  precision {yn[flag].mean():.2f}  recall {flag[yn == 1].mean():.2f}")
```
```output
== same-year batch: actual fail rate 23.0%, mean predicted risk 21.4%
   PSI: {'attendance': 0.043, 'internal': 0.086, 'assignment': 0.049, 'prev_gpa': 0.067, 'commute': 0.028}
   AUC 0.876  precision 0.66  recall 0.65
== online-term batch: actual fail rate 30.0%, mean predicted risk 31.8%
   PSI: {'attendance': 0.64, 'internal': 0.056, 'assignment': 0.04, 'prev_gpa': 0.037, 'commute': 0.056}
   AUC 0.861  precision 0.64  recall 0.70
== online + new behaviour: actual fail rate 25.0%, mean predicted risk 31.7%
   PSI: {'attendance': 0.598, 'internal': 0.055, 'assignment': 0.04, 'prev_gpa': 0.047, 'commute': 0.066}
   AUC 0.761  precision 0.49  recall 0.65
```

*Reading the output.* The **same-year batch** is calm: all PSIs are below 0.09, AUC is 0.876, and the mean predicted risk (21.4 percent) is close to the actual failure rate (23.0 percent). In the **online-term batch**, the attendance PSI jumps to **0.640**, far above 0.25, so the monitor raises an alarm, yet the model still works: AUC 0.861, precision 0.64, recall 0.70, and predicted risk (31.8 percent) matches the actual rate (30.0 percent). This is a lesson in itself: **an alarm means investigate, not retrain automatically**. In the third batch the relationship has also changed. Attendance PSI is again high (0.598), and now the damage is real: AUC falls to **0.761**, precision to 0.49, and the model predicts a 31.7 percent failure rate while the true rate is 25.0 percent. Only the end-of-term outcome check can reveal this second case, which is why Figure 1.1 includes a feedback arrow.

```svgfig label="4.2" caption="Drift monitor results for three batches. Left: attendance PSI against the 0.10 and 0.25 limits; both online-term batches are far over the red line. Right: model AUC; it holds up under covariate drift (0.861) and drops under concept drift (0.761). Input drift is an alarm; the outcome check decides whether to retrain."
f = Fig(580, 240)
f.text(150, 16, "Attendance PSI", size=11, color=NAVY, bold=True)
f.text(440, 16, "Model AUC", size=11, color=NAVY, bold=True)
f.line(40, 200, 270, 200, color=SLATE); f.line(330, 200, 560, 200, color=SLATE)
for yv, lab in ((0.25, "0.25"), (0.10, "0.10")):
    yy = 200 - yv * 220
    f.line(40, yy, 270, yy, color=RED if yv == 0.25 else AMBER, dash=True)
    f.text(34, yy, lab, size=9, color=SLATE, anchor="end", vmid=True)
for i, (v, lab) in enumerate(((0.043, "same year"), (0.640, "online"), (0.598, "online +\nnew behaviour"))):
    h = min(v, 0.7) * 220 * 0.9
    x = 60 + i * 72
    f.box(x, 200 - h, 44, h, "", fill=BLUE if v < 0.25 else "#fecaca", stroke=NAVY if v < 0.25 else RED)
    f.text(x + 22, 200 - h - 8, f"{v:.3f}", size=9.5, color=NAVY, bold=True)
    f.text(x + 22, 214, lab.split("\n")[0], size=9.5, color=NAVY)
    if "\n" in lab: f.text(x + 22, 226, lab.split("\n")[1], size=9.5, color=NAVY)
for i, (v, lab) in enumerate(((0.876, "same year"), (0.861, "online"), (0.761, "online +\nnew behaviour"))):
    h = (v - 0.5) * 380
    x = 350 + i * 72
    f.box(x, 200 - h, 44, h, "", fill=BLUE if v > 0.8 else "#fecaca", stroke=NAVY if v > 0.8 else RED)
    f.text(x + 22, 200 - h - 8, f"{v:.3f}", size=9.5, color=NAVY, bold=True)
    f.text(x + 22, 214, lab.split("\n")[0], size=9.5, color=NAVY)
    if "\n" in lab: f.text(x + 22, 226, lab.split("\n")[1], size=9.5, color=NAVY)
```

## 4.4 Privacy, consent and security

SikshyaSignal holds information about identifiable young people, and its output may influence how they are treated. That brings duties that a hobby project does not have. Nepal's Individual Privacy Act 2075 and the Electronic Transactions Act 2063 treat personal information and its misuse as legal matters; this book gives pointers, not legal advice, and a real deployment needs the college's legal and IT officers.

| Principle | What it means for SikshyaSignal | Practical step |
|---|---|---|
| Purpose limitation | data is used only to support students | write the purpose in the consent notice |
| Data minimisation | collect only the five needed columns | no names, religion, caste or phone numbers |
| Consent and notice | students know what is used and why | notice at admission; right to ask |
| Access control | only named teachers see the list | login, roles, access log |
| Security | stored safely, transmitted safely | encrypted disk, HTTPS, hashed ids |
| Retention | not kept longer than needed | delete risk scores after the term |
| Human review | the score never decides alone | teacher meets the student first |
| Accountability | someone owns mistakes | named owner, complaint route, model version in every reply |

*Special care with labels.* A flag such as "at risk" can stick to a student like a stamp. The system should store the risk score only for the current term, show it only to the student's mentor, and never put it on a transcript or share it with employers.

## 4.5 Deployment options and the run file

For the defence a laptop is enough, but the report should explain the path to a real college. On a college server the usual steps are: install Python and the pinned library versions, copy the code and `model.json`, run the service under a process manager so that it restarts after a crash, put it behind HTTPS, and schedule a nightly backup of the logs. A container makes the environment repeatable. The file below is a typical **Dockerfile** for the service; it is shown for explanation and is not run in this book.

```text
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY service.py model.json ./
EXPOSE 8000
USER nobody
CMD ["python", "service.py"]
```

Pinning library versions in `requirements.txt` (for example `numpy==2.1.0`) matters because two versions can produce slightly different numbers. The README must also say which Python version was used, which seed generates the data, and the exact commands for running the tests and the demo.

## 4.6 Eight deployment habits that prevent embarrassing failures

1. **Validate every input.** Reject out-of-range, missing and wrongly typed values with a clear message, as the service did for attendance 120. Silent acceptance of nonsense is the most common production bug. Add a test for each rule.
2. **Version the model.** Put a version in the file and in every reply, and keep old versions. When a student challenges a flag from last term, the team can reproduce it. Without versions, results cannot be explained.
3. **Test the saved model, not only the training code.** The round-trip test proved the file loads and agrees with memory. Many failures come from saving or loading, not from learning. Run all tests before every release.
4. **Log requests without names.** Log time, model version and risk, but never name, phone or roll number. Logs are what you use to debug and to monitor drift; they must not become a second leak of personal data.
5. **Monitor inputs daily and outcomes each term.** PSI on inputs is quick, while the performance check needs the final results. Write both into the calendar. An alarm triggers investigation, as the online-term batch showed.
6. **Decide the retraining rule in advance.** Write down "retrain when AUC on the term's outcomes drops by 0.05 or more, or PSI is above 0.25 and AUC drops". A rule prepared in calm time avoids panic and arguments later.
7. **Keep a human fallback.** If the service is down or the model is retired, teachers must still be able to do their job with the attendance register. Describe the manual process in the report.
8. **Plan the exit.** Say how data and models will be deleted when the project ends or the student leaves. A capstone that ignores the end of its own data's life has an unfinished privacy chapter.

## Formula and fact sheet

| Item | Formula or fact |
|---|---|
| Model artefact | weights, bias, feature order, means, standard deviations, threshold, version |
| PSI | Σ (new share − old share) × ln(new share ÷ old share), over ten equal-count bins |
| PSI guide | below 0.10 stable; 0.10 to 0.25 look closer; above 0.25 major shift |
| Covariate drift | the inputs change |
| Concept drift | the input-to-outcome relationship changes |
| Calibration check | mean predicted risk versus actual failure rate |
| Privacy principles | purpose, minimisation, consent, access, security, retention, review, accountability |

## Chapter summary

- Save the model as a small versioned file and wrap it in a function that **validates input** and returns the model version.
- Eight fast tests, including behaviour tests and a save-load round trip, make the service trustworthy.
- **Drift** has two forms: inputs change (covariate) or the relationship changes (concept). PSI watches inputs; only outcomes reveal concept drift.
- An alarm means **investigate**; retrain by a rule written in advance.
- A system about students needs **consent, minimisation, access control, retention limits and human review**.
- Describe deployment honestly: laptop demo, college server, cloud tier, and a manual fallback.

## Practice

1. List the items stored in `model.json` and say why the means and standard deviations must be included.
2. Why did the service reject a record with attendance 120?
3. What is a behaviour test? Give one example from Section 4.2.
4. State the PSI formula and the three ranges of the usual rule of thumb.
5. Explain the difference between covariate drift and concept drift with one example each.
6. In the online-term batch the attendance PSI was 0.640 but the AUC stayed at 0.861. What should the college do?
7. In the third batch the model predicted 31.7 percent failures but the true rate was 25.0 percent. What does that tell you?
8. Why should logs not contain student names?
9. Name four of the privacy principles in Section 4.4 and give a practical step for each.
10. Write a retraining rule for SikshyaSignal in one sentence.

::: note Answers and worked solutions
**1.** Weights, bias, feature names, means, standard deviations, threshold, version. The service must scale a new student with the same numbers used in training or every score is wrong.
**2.** The valid range in the data sheet is 0 to 100; 120 is impossible and would give a meaningless score, so the service returns an error.
**3.** A test that checks the model moves in the expected direction, for example more attendance lowers risk or higher internal marks lower risk.
**4.** PSI = Σ (new − old) × ln(new ÷ old). Below 0.10 stable, 0.10 to 0.25 watch, above 0.25 major shift.
**5.** Covariate: attendance falls after online classes (inputs differ). Concept: attendance no longer predicts failure because students log in without engaging (relationship differs).
**6.** Investigate and check the outcome measures; because AUC and calibration are still good, keep the model but continue to monitor.
**7.** The model over-predicts risk; the relationship has changed, so a retraining or recalibration is needed.
**8.** Logs are often copied and shared; names in them would create a second leak of personal data.
**9.** Example: purpose limitation (consent notice), minimisation (no names or caste), access control (roles and an access log), retention (delete scores after the term).
**10.** "Retrain when term-end AUC falls by 0.05 or more below the validation value, or when attendance PSI is above 0.25 and AUC has fallen."
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain how a trained model is turned into a small service and why automated tests are important. Use the early-warning example.**

*Introduction.* A trained model is only a set of numbers. To be useful it must be saved, loaded by a program that applies it exactly as in training, and protected against bad input.

*Steps.*

1. **Save the artefact.** The weights, bias, feature order, training means and standard deviations, threshold and version are written to a 361-byte JSON file.
2. **Write `predict`.** It checks that all five fields are present and in range, scales them with the stored means, applies the weights and sigmoid, and returns the risk, the flag and the model version.
3. **Reject bad input.** Attendance 120 or a record with missing fields returns an error message instead of a score.
4. **Log safely.** Time, version and risk are logged without names.

*Why tests matter.* Eight tests ran and passed in one second. They check the sigmoid, the range of the risk, the save–load round trip, the direction of the model (more attendance gives less risk), and the rejection of bad input. A change that breaks any one of these shows up at once, before a teacher sees a wrong list.

*Conclusion.* A small versioned service with validation and tests is evidence that the project works beyond the author's laptop, and it is the first thing a careful examiner asks to see.

**Q2 (5 marks). What is data drift? Distinguish covariate drift from concept drift and explain how the population stability index is used to monitor it.**

*Introduction.* A model is trained on past data but used on future data. When the future differs, performance can fall without any error message. This change is called drift.

*Types.* **Covariate drift** means the inputs change, for example attendance falls after a term of online classes. **Concept drift** means the relationship between inputs and outcome changes, for example attendance no longer predicts failure because students log in without engaging.

*PSI.* Split the training values into ten equal-count bins and compute Σ (new share − old share) × ln(new share ÷ old share). Below 0.10 is stable, 0.10 to 0.25 needs a look, and above 0.25 is a major shift.

*Example.* In the online-term batch the attendance PSI was 0.640, yet the AUC was still 0.861 and the predicted failure rate (31.8 percent) matched the actual rate (30.0 percent), so the model stayed in service. In the third batch the PSI was 0.598 and the AUC fell to 0.761, with predictions of 31.7 percent against an actual 25.0 percent, so the model needed retraining.

*Conclusion.* PSI gives a daily warning about inputs, but only a comparison with real outcomes decides whether to retrain.

**Q3 (10 marks). Discuss the deployment, monitoring and privacy requirements of a student-risk prediction system in a Nepali college. Include the service design, testing, drift monitoring, retraining rule, privacy principles and human oversight.**

*Introduction.* A system that scores students affects real people, so deployment is more than starting a program. SikshyaSignal needs a reliable service, honest monitoring and strong privacy safeguards, all described in the report.

*1. Service design.* Store the model as a versioned JSON file and expose a `predict` function that validates input, scales with the stored means and deviations, scores, applies the threshold and returns risk, flag and version (Figure 4.1). Bad input gets a clear error.

*2. Testing.* Run eight automated tests (maths, round trip, behaviour, rejection) before each release. Add a test for every bug found.

*3. Deployment levels.* Demonstrate on a laptop with simulated data; for a real college use a server managed by the IT officer, with HTTPS, a process manager, backups and pinned library versions, ideally in a container. Use a cloud service only with consent and no personal data leaving the college.

*4. Monitoring.* Calculate PSI daily on each feature and compare mean predicted risk with the real failure rate each term. Alarms mean investigation, as in the online-term batch where PSI was 0.640 but AUC stayed at 0.861.

*5. Retraining rule.* Retrain when term-end AUC falls by 0.05 or more below the validation value, or when PSI is above 0.25 and AUC has fallen. The third batch (AUC 0.761) would trigger it.

*6. Privacy.* Apply purpose limitation, minimisation, consent, access control, secure storage, retention limits, human review and accountability (Section 4.4), following the spirit of the Individual Privacy Act 2075 and the Electronic Transactions Act 2063. Use random ids and keep logs free of names.

*7. Human oversight.* The score is advice to a mentor, who meets the student before any action. Students can ask what is recorded and challenge it. If the service is down, the manual register process continues.

| Requirement | Evidence in the report |
|---|---|
| Service | versioned file, validation, example requests |
| Tests | eight PASS lines |
| Monitoring | PSI table and outcome check |
| Retraining | written rule with numbers |
| Privacy | principle table with steps |
| Oversight | human review and fallback plan |

*Conclusion.* A capstone that treats deployment as a responsibility, with versioning, tests, monitoring and privacy built in, shows the maturity expected of a graduate who will build systems that affect people.
