---
subject: Cyber Security and Ethical Hacking
grade: BCA Semester 7
unit: 6
title: Intrusion Detection, Alert Statistics, Incident Response and Digital Forensics
hours: 6
area: BCA 401 · Cyber Security and Ethical Hacking · Unit 6
---

Prevention fails sometimes, so security teams also detect and respond. A security operations centre receives thousands of alerts a day from sensors that watch networks and hosts, and its analysts must decide which few deserve attention. The statistics of detection are deeply counter-intuitive: a detector that is right 99 times out of 100 can still be wrong most of the time when it raises an alarm. Once an incident is confirmed, a disciplined response lifecycle and careful evidence handling decide whether the organisation recovers cleanly and can prove what happened.

::: key What this unit gives you
- IDS, IPS and SIEM: types, placement and detection methods.
- The confusion matrix: TPR, FPR, precision, accuracy and F1.
- The base-rate fallacy, shown by Bayes' rule and by numbers, and what it means for alert design.
- The incident response lifecycle, and digital forensics with SHA-256 hashing and a tamper-evident chain of custody.
:::

## 6.1 Detection systems

An **intrusion detection system (IDS)** watches activity and raises alerts; an **intrusion prevention system (IPS)** sits inline and can also block. A **network IDS** inspects traffic at a tap or mirror port; a **host IDS** (and modern endpoint detection and response, EDR) inspects processes, files, logs and system calls on a machine. A **SIEM** (security information and event management) collects logs from all sources, normalises and correlates them and presents alerts and dashboards.

Detection methods:

- **Signature-based:** compare activity with patterns of known-bad behaviour. Accurate for known issues and silent on new ones.
- **Anomaly-based:** learn a baseline of normal behaviour and flag deviations. It can catch novel activity but produces more false alarms.
- **Stateful and behavioural rules:** for example, many failed logins followed by a success from one address, or an administrator account used at an unusual hour.

Placement matters: sensors at network boundaries, between internal zones (to see lateral movement) and on critical hosts; and their data must be protected and time-synchronised so that events from different sources can be ordered.

## 6.2 The confusion matrix

Every alert decision falls into one of four cells:

| | **Actually malicious** | **Actually benign** |
|---|---|---|
| **Alert raised** | True positive (TP) | False positive (FP) |
| **No alert** | False negative (FN) | True negative (TN) |

Derived measures:

- **True positive rate (TPR, recall, sensitivity)** = TP ÷ (TP + FN): the share of real attacks detected.
- **False positive rate (FPR)** = FP ÷ (FP + TN): the share of benign events wrongly flagged.
- **Precision (positive predictive value)** = TP ÷ (TP + FP): the share of alerts that are real.
- **Accuracy** = (TP + TN) ÷ total, and **F1** = 2TP ÷ (2TP + FP + FN), the harmonic mean of precision and recall.

## 6.3 The base-rate fallacy

Suppose a detector has TPR 99% and FPR 1%, which sounds excellent. Monitor 100,000 events of which only 100 are malicious (a prevalence of 0.1%, realistic for security data). By **Bayes' rule**, the probability that an alert is real is

::: key Bayes' rule for alerts
P(malicious | alert) = TPR × p ÷ (TPR × p + FPR × (1 − p)), where *p* is the prevalence of malicious events.
:::

```python
total, malicious = 100000, 100
tpr, fpr = 0.99, 0.01
tp = round(malicious * tpr)
fn = malicious - tp
fp = round((total - malicious) * fpr)
tn = total - malicious - fp
precision = tp / (tp + fp)
accuracy = (tp + tn) / total
f1 = 2 * tp / (2 * tp + fp + fn)
print(f"events {total}, malicious {malicious}: TP={tp} FN={fn} FP={fp} TN={tn}")
print(f"TPR {tp / (tp + fn) * 100:.2f}%, FPR {fp / (fp + tn) * 100:.2f}%, precision {precision * 100:.2f}%, accuracy {accuracy * 100:.2f}%, F1 {f1:.4f}")
prev = malicious / total
bayes = tpr * prev / (tpr * prev + fpr * (1 - prev))
print(f"P(malicious | alert) via Bayes: {bayes * 100:.2f}%")
```
```output
events 100000, malicious 100: TP=99 FN=1 FP=999 TN=98901
TPR 99.00%, FPR 1.00%, precision 9.02%, accuracy 99.00%, F1 0.1653
P(malicious | alert) via Bayes: 9.02%
```
The detector finds 99 of the 100 real events but also raises 999 false alarms on benign traffic, so only 9.02% of alerts are real. **Accuracy is 99%**, a number that is nearly meaningless here: a "detector" that never alerts would also score 99.9%. The Bayes calculation gives the same 9.02% as the counted precision, confirming that the arithmetic is consistent. The lesson is that a low base rate can drown a good detector in false positives, so judge detectors by **precision and recall at the real prevalence**, not by accuracy.

How strongly does the false-positive rate matter? And what does it cost in analyst time? The next program varies FPR and converts alerts to hours at an assumed 5 minutes per alert.

```python
total, malicious, tp = 100000, 100, 99
benign = total - malicious
p1 = tp / (tp + benign * 0.001)
p2 = tp / (tp + benign * 0.0001)
print(f"precision at FPR 0.10%: {p1 * 100:.2f}%; at FPR 0.01%: {p2 * 100:.2f}%")
alerts = tp + round(benign * 0.01)
print(f"daily alerts {alerts}, analyst effort {alerts * 5 / 60:.1f} hours at 5 min each")
```
```output
precision at FPR 0.10%: 49.77%; at FPR 0.01%: 90.83%
daily alerts 1098, analyst effort 91.5 hours at 5 min each
```
Cutting FPR tenfold to 0.1% lifts precision to 49.77%, and to 0.01% lifts it to 90.83%. At the original 1% FPR the team gets 1,098 alerts a day, about 91.5 analyst-hours of triage: more than a whole shift of several people, which is how **alert fatigue** sets in and real alerts get ignored. Practical remedies are tuning rules to your environment, raising alerts on *correlated* evidence (several weak signals together) rather than each one, risk-based alerting that weights by asset value, allow-listing known-good activity, and automating routine triage with playbooks (SOAR).

## 6.4 Incident response lifecycle

An **incident** is an event that actually or potentially jeopardises confidentiality, integrity or availability. NIST SP 800-61 describes a lifecycle with four phases (a newer revision re-expresses them using the NIST Cybersecurity Framework functions):

1. **Preparation:** a written plan and policy, a trained response team with roles and contacts, tooling (logging, forensic kits, backups), communication templates and regular exercises (tabletops).
2. **Detection and analysis:** identify and validate the incident, determine scope and severity, preserve evidence, and decide who must be told.
3. **Containment, eradication and recovery:** limit the spread (isolate hosts, disable accounts) while balancing evidence and business needs; remove the cause (patch, rebuild, rotate credentials); restore from clean backups and monitor closely.
4. **Post-incident activity:** a blameless review within days, lessons learned, updated controls and metrics such as time to detect and time to recover.

Report incidents as the law, contracts and sector regulators require. In Nepal that can involve the Nepal Police Cyber Bureau for criminal matters, the national CERT for technical coordination and the sector regulator (for banks, Nepal Rastra Bank). Legal context is covered in Unit 7.

## 6.5 Digital forensics

**Digital forensics** collects, preserves, analyses and presents electronic evidence so that it stands up to scrutiny. Core principles: *do not alter the original*; work on verified copies; document every step; and keep a clear **chain of custody**. Collect evidence in order of **volatility** (RFC 3227): CPU registers and cache, memory, network state and running processes, then disk, remote logs and archival media. Use **write blockers** when imaging a drive, and record the make, serial number, time and person.

The key tool is the cryptographic hash. A **SHA-256** digest of the evidence image, taken at acquisition and recomputed later, proves it has not changed: any single-bit change gives a completely different digest. A **chain-of-custody log** records each handover (who, what, when). To make the log itself tamper-evident, each entry can include the hash of the *previous entry*, forming a hash chain: altering any earlier record changes every later hash.

```python
import hashlib

def h(b):
    return hashlib.sha256(b).hexdigest()

evidence = b"disk-image-bytes-0001"
ev_hash = h(evidence)
print(f"evidence SHA-256 (first 16 hex): {ev_hash[:16]}")

log = [("Officer Rai", "seized laptop"), ("Lab tech Karki", "imaged disk"), ("Analyst Thapa", "analysis copy")]

def build(entries):
    prev, chain = "0" * 64, []
    for who, act in entries:
        cur = h((prev + who + "|" + act + "|" + ev_hash).encode())
        chain.append(cur)
        prev = cur
    return chain

stored = build(log)
def verify(entries):
    return build(entries) == stored

print(f"custody chain entries: {len(stored)}, verified: {verify(log)}")
edited = list(log)
edited[1] = ("Lab tech Karki", "imaged disk (note edited)")
print(f"after editing entry 2: verified {verify(edited)}")
```
```output
evidence SHA-256 (first 16 hex): e756a790143143e7
custody chain entries: 3, verified: True
after editing entry 2: verified False
```
The evidence digest was independently recomputed with the `sha256sum` utility during checking. The untouched log verifies, and editing even one note in entry 2 makes verification fail, so the change is detected. Real practice adds signed forms, trusted timestamps and secure storage of the stored chain; the hash chain is the core idea behind tamper-evident logs, including the audit logs that the Cloud Computing course (Unit 6) recommends sending to a separate, write-protected account.

::: caution
Hashing proves that evidence has **not changed since it was hashed**, not that it was handled correctly before that moment. Hash at the earliest possible point, and never run analysis tools on the original.
:::

## 6.6 Seeing the ideas: forensic hardware, sensor placement, the confusion matrix, the incident cycle and the custody chain

Digital forensics begins with hardware that protects evidence. Plate 6.1 shows two devices used by examiners: a write blocker that lets a disk be read but never written, and a stand-alone disk imager that makes the exact copy that analysis will use.

```photogrid label="6.1" cols="2" ratio="1.45" caption="Forensic hardware. (a) A Tableau write blocker between a SATA hard disk and the examiner's computer: it allows read commands and blocks writes, so the original evidence cannot be altered. (b) A forensic disk imager with a touch screen copying a disk bit for bit; the copy is hashed so that its integrity can be proved later."
@ photo id="bca401/writeblocker" cap="Write blocker with SATA disk"
fit 1.45
focus 0.5 0.5
@ photo id="bca401/imager" cap="Forensic disk imager"
fit 1.45
focus 0.5 0.5
```

```svgfig label="6.1" caption="Where detection sensors sit. A network IDS watches a mirror port at the boundary and between zones, host agents watch critical servers, and all events flow to a time-synchronised log collector where analysts triage the alerts."
f = Fig(580, 214)
f.box(6, 78, 80, 50, "Internet", fill=ROSE, stroke=RED, bold=True, size=10.5)
f.box(110, 84, 64, 38, "Firewall", fill=SAND, stroke=AMBER, bold=True, size=10)
f.box(200, 20, 116, 50, "DMZ servers\n+ host agent", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(200, 136, 116, 50, "Internal zone\n+ host agents", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(200, 78, 116, 50, "Switch with\nmirror (SPAN) port", fill="#f1f5f9", stroke=SLATE, size=9.5, bold=True)
f.box(340, 78, 90, 50, "Network IDS\n(sensor)", fill=ROSE, stroke=RED, size=10, bold=True)
f.box(462, 78, 110, 50, "Log collector\nSIEM + analysts", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.arrow([(86, 103), (110, 103)]); f.arrow([(174, 103), (200, 103)])
f.arrow([(316, 103), (340, 103)], dash=True, label="copy", lpos=(328, 70))
f.arrow([(430, 103), (462, 103)], color=RED, label="alerts", lpos=(446, 70))
f.arrow([(316, 45), (517, 78)], color=NAVY, dash=True)
f.arrow([(316, 161), (517, 128)], color=TEAL, dash=True)
f.text(290, 206, "Synchronise clocks (NTP) so events from every source line up", size=10, color=NAVY, bold=True)
```

```svgfig label="6.2" caption="The base-rate fallacy in numbers (100,000 events, 100 malicious, TPR 99%, FPR 1%). The detector catches 99 of 100 real events but also raises 999 false alarms, so only 99 of 1,098 alerts are real: precision 9.02%, although accuracy is 99.00%."
f = Fig(580, 218)
f.text(110, 12, "Confusion matrix", size=11, color=NAVY, bold=True)
f.text(80, 30, "alert", size=10, color=SLATE, bold=True); f.text(170, 30, "no alert", size=10, color=SLATE, bold=True)
f.box(40, 36, 80, 56, "TP = 99", fill=MINT, stroke=TEAL, bold=True, size=11); f.box(130, 36, 80, 56, "FN = 1", fill=SAND, stroke=AMBER, bold=True, size=11)
f.box(40, 96, 80, 56, "FP = 999", fill=ROSE, stroke=RED, bold=True, size=11); f.box(130, 96, 80, 56, "TN = 98,901", fill="#f1f5f9", stroke=SLATE, bold=True, size=10)
f.text(22, 66, "bad", size=10, color=SLATE, bold=True); f.text(22, 126, "good", size=10, color=SLATE, bold=True)
f.text(400, 12, "The 1,098 alerts", size=11, color=NAVY, bold=True)
f.box(240, 36, 330 * 99 / 1098, 40, "", fill=MINT, stroke=TEAL)
f.box(240 + 330 * 99 / 1098, 36, 330 * 999 / 1098, 40, "999 false alarms (91%)", fill=ROSE, stroke=RED, bold=True, size=10)
f.text(255, 90, "99 real", size=10, color=TEAL, bold=True, anchor="start")
f.box(240, 110, 330, 42, "P(malicious | alert) = TPR x p / (TPR x p + FPR x (1 - p))\n= 0.99 x 0.001 / (0.99 x 0.001 + 0.01 x 0.999) = 9.02%", fill="#f8fafc", stroke=SLATE, size=10)
f.box(40, 168, 530, 40, "Lower the FPR, not just raise the TPR: at FPR 0.10% precision is 49.77%, at 0.01% it is 90.83%", fill=BLUE, stroke=NAVY, bold=True, size=10.5)
```

```svgfig label="6.3" caption="The NIST incident response lifecycle (SP 800-61). Lessons from post-incident activity feed back into preparation, so the cycle improves with every incident."
f = Fig(580, 214)
ph = [(20, 24, "1  Preparation", "policy, team, tools,\nbackups, contacts", BLUE, NAVY), (310, 24, "2  Detection and analysis", "alerts, triage, scope,\nseverity, evidence", SAND, AMBER), (310, 130, "3  Containment, eradication, recovery", "isolate, remove cause,\nrestore from clean backups", ROSE, RED), (20, 130, "4  Post-incident activity", "report, lessons learned,\nupdate controls", MINT, TEAL)]
for (x, y, t, s, fl, st) in ph:
    f.box(x, y, 250, 70, t + "\n" + s, fill=fl, stroke=st, size=10.5, bold=True)
f.arrow([(270, 59), (310, 59)]); f.arrow([(435, 94), (435, 130)]); f.arrow([(310, 165), (270, 165)]); f.arrow([(145, 130), (145, 94)])
f.text(290, 110, "cycle", size=10, color=SLATE)
```

```svgfig label="6.4" caption="A hash-chained chain-of-custody log. Each entry stores the previous entry's hash, so editing the note in entry 2 changes its hash and breaks the link in entry 3. The verification run in section 6.5 returned True for the untouched log and False after one edit."
f = Fig(580, 188)
for i, (t, fl, st) in enumerate([("Entry 1\nseized laptop, bagged\nprev = 0000...", MINT, TEAL), ("Entry 2\nimaged by analyst\nprev = hash(entry 1)", MINT, TEAL), ("Entry 3\nimage hashed, stored\nprev = hash(entry 2)", MINT, TEAL)]):
    f.box(8 + i * 192, 14, 176, 70, t, fill=fl, stroke=st, size=10, bold=True)
    if i < 2:
        f.arrow([(184 + i * 192, 49), (200 + i * 192, 49)], color=NAVY)
f.box(200, 98, 176, 30, "edited note in entry 2", fill=ROSE, stroke=RED, bold=True, size=10)
f.arrow([(288, 98), (288, 84)], color=RED)
f.arrow([(376, 56), (392, 56)], color=RED, dash=True)
f.box(8, 140, 564, 42, "Hash of entry 2 changes, so entry 3 no longer matches: verification fails.\nHash evidence at the earliest moment and work only on verified copies.", fill=BLUE, stroke=NAVY, size=10)
```

### 6.6.1 Eight good practices for incident response and forensics

1. **Prepare before anything happens.** Write an incident plan, name an owner and keep contact numbers current. A hospital should know in advance who calls the IT head and who calls the police. Practice with a table-top exercise twice a year.
2. **Collect and protect logs.** Send logs to a central, protected server with synchronised clocks. Attackers often delete local logs first. A central copy lets the team rebuild the timeline.
3. **Triage by impact.** Rank alerts by the value of the asset and the severity of the event. Analysts cannot read 1,098 alerts a day. Start with alerts on payment, identity and database systems.
4. **Contain first, then investigate.** Isolate the infected machine from the network but keep it powered if memory evidence is needed. Cutting the network stops spread. Wiping too early destroys evidence.
5. **Preserve evidence.** Use a write blocker, make a bit-for-bit image and record its SHA-256 hash. Work only on copies. Evidence that cannot be proven unchanged is weak in court.
6. **Keep a chain of custody.** Record who held the evidence, when and why, with each entry linked to the last. A broken chain lets the other side question the evidence. Hash-chained logs make tampering detectable.
7. **Communicate carefully.** Tell the right people at the right time: management, affected users, the bank, and the authorities such as the Nepal Police Cyber Bureau. Use one spokesperson. Rumours spread faster than facts.
8. **Learn and improve.** After recovery, hold a blameless review and fix root causes. Update detection rules, backups and training. The same incident should never surprise the team twice.

## 6.7 Summary and exercises

Detection quality is measured by TPR, FPR and precision at the real base rate; Bayes' rule shows why a low prevalence yields mostly false alarms; incident response follows preparation, detection and analysis, containment, eradication and recovery, and post-incident learning; and forensic work depends on hashing, volatility order and an auditable chain of custody.

1. Compute TPR, FPR and precision for TP=45, FN=5, FP=200, TN=9,750.
2. A detector has TPR 95% and FPR 2% where prevalence is 0.5%. Compute P(malicious | alert).
3. Why is accuracy a poor metric for intrusion detection? Give an example.
4. List the four incident response phases and one activity in each.
5. Explain order of volatility with a list of five evidence sources.
6. Describe how a hash chain makes a custody log tamper-evident, and what it cannot prove.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is the base-rate fallacy? Show with a numerical example why a 99% accurate detector can still give mostly false alarms.**

*Introduction.* The base-rate fallacy is the mistake of judging a detector only by its true-positive and false-positive rates while ignoring how rare the real events are. In security data malicious events are very rare, so even a small false-positive rate produces a flood of false alarms (section 6.3).

*Example.* A detector has a true-positive rate (TPR) of 99% and a false-positive rate (FPR) of 1%. It monitors 100,000 events of which 100 are malicious (prevalence 0.1%).

| | Alert | No alert | Total |
|---|---|---|---|
| Malicious | TP = 99 | FN = 1 | 100 |
| Benign | FP = 999 | TN = 98,901 | 99,900 |

*Calculation (Figure 6.2).* Alerts = 99 + 999 = 1,098. By Bayes' rule, P(malicious | alert) = 0.99 x 0.001 / (0.99 x 0.001 + 0.01 x 0.999) = 0.00099 / 0.01098 = 9.02%. Accuracy is (99 + 98,901) / 100,000 = 99.00%, a number that hides the problem.

*Meaning.* Only about 1 alert in 11 is real. At 5 minutes per alert, the team spends about 91.5 hours a day on triage.

*Remedy.* Reduce FPR rather than only raise TPR. At FPR 0.10% precision rises to 49.77%, and at 0.01% to 90.83%. Tune rules, whitelist known-good activity and combine signals before alerting.

**Q2 (5 marks). Explain the incident response lifecycle with the actions in each phase.**

*Introduction.* An incident is an event that actually or potentially harms confidentiality, integrity or availability. NIST SP 800-61 describes a four-phase lifecycle that organisations follow so that they respond in an orderly way rather than panic (section 6.4 and Figure 6.3).

1. **Preparation.** Write the incident response policy, form and train the team, set up logging and backups, and keep contact lists. This phase decides how well the other three go.
2. **Detection and analysis.** Alerts from IDS, logs and user reports are triaged. The team confirms whether it is a real incident, finds its scope and severity and starts collecting evidence.
3. **Containment, eradication and recovery.** Contain the damage by isolating hosts or blocking accounts, remove the root cause such as malware or a stolen credential, and restore systems from clean backups while watching for reinfection.
4. **Post-incident activity.** Hold a lessons-learned meeting, write a report and update controls and training.

| Phase | Key output |
|---|---|
| Preparation | Plan, tools, trained team |
| Detection and analysis | Confirmed incident, scope, evidence |
| Containment, eradication, recovery | Systems cleaned and restored |
| Post-incident | Report, improved controls |

*Conclusion.* The arrow from lessons learned back to preparation makes the lifecycle a cycle; each incident leaves the organisation stronger.

**Q3 (10 marks). Explain digital forensics: the principles, the process, and how chain of custody and hashing preserve the integrity of evidence.**

*Introduction.* Digital forensics is the identification, preservation, analysis and presentation of digital evidence in a way that is acceptable to a court or a disciplinary panel. Because digital data is easy to change, the process is designed to prove that the evidence has not changed (section 6.5).

*Principles.* Never work on the original, document every action, and be able to repeat the result with the same tools. The examiner must be able to explain each step to a non-technical judge.

*Process.*

1. **Identification and seizure.** Decide what could hold evidence: laptops, phones, servers, cloud accounts and logs. Photograph the scene and label each item.
2. **Preservation.** Connect the disk through a **write blocker** and create a bit-for-bit image with a forensic imager (Plate 6.1). Compute the SHA-256 hash of the original and of the copy; equal hashes show that the copy is exact.
3. **Analysis.** Examine only the verified copy: files, deleted data, logs, browser history and timelines. Volatile data such as memory is captured first because it disappears at power-off.
4. **Reporting and presentation.** Write findings with the methods, tools and hash values so another examiner can verify them.

*Hashing.* A SHA-256 digest is a 256-bit fingerprint of the data. Changing one bit changes the digest completely. In the worked example the evidence digest began e756a790143143e7. A hash proves the data has not changed *since it was hashed*, so it must be taken at the earliest possible moment.

*Chain of custody.* A chain-of-custody log records who held the evidence, when, where and why. In the hash-chained log of Figure 6.4, each entry contains the hash of the previous entry. The 3-entry log verified as True; after one note in entry 2 was edited it verified False, because entry 3 no longer matched. This makes silent tampering detectable.

| Element | Purpose |
|---|---|
| Write blocker | Stops writes to original disk |
| Bit-for-bit image | Exact working copy |
| SHA-256 hash | Proves integrity |
| Custody log | Proves who handled it |
| Documentation | Allows repetition by others |

*Legal link.* In Nepal, electronic records are accepted as evidence under the Electronic Transactions Act 2063, but their value depends on this proof of integrity and handling (Unit 7).

*Conclusion.* Good forensics combines technical tools with careful paperwork. Without hashing and custody records even correct findings can be rejected.
