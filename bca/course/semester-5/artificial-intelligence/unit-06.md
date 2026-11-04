---
subject: Artificial Intelligence
grade: BCA Semester 5
unit: 6
title: Expert Systems and Machine Vision
hours: 4
area: BCA 302 · Artificial Intelligence · Unit 6
---

When a patient arrives with a fever and a rash, a good doctor does not search a graph; she applies hundreds of remembered rules of the form "if this and this, then probably that". An **expert system** puts such rules in a program, separate from the engine that applies them, so the knowledge of a scarce human specialist can be copied, explained and used at any hour. **Machine vision** gives computers eyes: it turns a grid of pixel numbers into edges, objects and decisions. Both are classic applications that combine the ideas of the earlier units.

::: key What this unit gives you
- What an expert system is; its architecture, the inference engine and development stages; certainty factors.
- Machine vision: the steps from image acquisition to recognition, with a worked edge-detection example.
- Applications and limits of both.
:::

## 6.1 Expert systems

An **expert system (ES)** is a program that solves problems in a narrow domain at the level of a human expert, using a body of expert knowledge held in an explicit **knowledge base**. Famous examples: **DENDRAL** (1960s, infers molecular structure from mass-spectrometer data), **MYCIN** (1970s, diagnoses blood infections and recommends antibiotics from about 600 rules; its evaluation found its advice comparable with specialists', though it was never used clinically), **XCON/R1** (configures computer orders for DEC, with thousands of rules, saving the company a great deal of money) and **PROSPECTOR** (mineral exploration). Modern descendants are business-rule engines, tax and loan-eligibility advisers and clinical decision-support tools.

### Characteristics

Expert systems are **domain-specific**, **knowledge-based** (knowledge separated from the reasoning engine), able to **explain** their conclusions (*why* are you asking this? *how* did you reach that?), able to reason with **uncertain** and incomplete information, and **modifiable** by editing rules without rewriting the program.

### Architecture

| Component | Role |
|---|---|
| Knowledge base | domain facts and rules (usually IF–THEN) |
| Working memory (fact base) | the facts of the current case |
| Inference engine | matches rules to facts and decides which rule to fire; forward or backward chaining, conflict resolution |
| User interface | asks questions, shows conclusions |
| Explanation facility | shows the chain of rules behind an answer |
| Knowledge acquisition module | helps the knowledge engineer enter and test rules |

The people involved are the **domain expert** (who has the knowledge), the **knowledge engineer** (who encodes it) and the **user**. **Expert system shells** (CLIPS, Jess, Drools) provide the engine, interface and explanation, leaving only the knowledge base to be written.

### Inference: forward and backward chaining

Forward chaining (Unit 3) suits **monitoring and diagnosis from symptoms**: start from the observed facts and derive what follows. Backward chaining suits **hypothesis testing**: start from a goal ("is it flu?") and ask only the questions that matter. **Conflict resolution** picks one rule when several can fire: highest priority, most specific, most recent facts, or first listed.

::: example Forward chaining on a small diagnosis rule base
Rules: R1 IF fever AND cough THEN flu_suspect. R2 IF flu_suspect AND body_ache THEN flu. R3 IF flu THEN advise_rest_and_fluids. R4 IF rash AND fever THEN measles_suspect. Facts: fever, cough, body_ache.

Cycle 1: R1 fires (fever, cough), adding flu_suspect. R4 cannot fire (no rash). Cycle 2: R2 fires, adding flu. Cycle 3: R3 fires, adding advise_rest_and_fluids. Cycle 4: nothing new, stop. measles_suspect is never derived. The program at the end runs exactly this.
:::

### Reasoning with uncertainty: certainty factors

Expert knowledge is rarely certain. MYCIN used **certainty factors** (CF) between −1 (certainly false) and +1 (certainly true), 0 meaning no evidence.

- A rule `IF A AND B THEN C` with rule certainty CF_r gives CF(C) = CF_r × min(CF(A), CF(B)) (for OR use max).
- Two rules supporting the same conclusion with CF₁ and CF₂ (both positive) combine as **CF = CF₁ + CF₂ (1 − CF₁)**; for CF₁ = 0.6 and CF₂ = 0.5, CF = 0.6 + 0.5 × 0.4 = **0.8**: independent evidence reinforces, but never exceeds 1.
- Evidence of opposite signs combines as (CF₁ + CF₂) / (1 − min(|CF₁|, |CF₂|)); for 0.6 and −0.4 this gives 0.2 / 0.6 = **0.333**.

For premises with CF 0.8 and 0.6 and a rule with CF_r = 0.9: CF = 0.9 × min(0.8, 0.6) = **0.54**. Certainty factors are heuristic and not true probabilities; Bayesian networks (Unit 3) are the principled alternative.

### Stages of expert-system development

1. **Identification**: define the problem, the experts, the resources and the goals; decide whether an ES is suitable (a narrow, well-understood domain with a real expert who is available).
2. **Conceptualisation**: find the key concepts, relations and the problem-solving strategy.
3. **Formalisation**: choose a representation (rules, frames) and a tool or shell.
4. **Implementation**: encode the knowledge base and the interface; build a prototype quickly and grow it.
5. **Testing and evaluation**: compare against expert judgement and real cases, refine rules, check coverage and conflicts.
6. **Maintenance**: update rules as the domain changes; an ES whose knowledge ages is dangerous.

### Advantages and limitations

Advantages: consistent decisions, availability, preservation of rare expertise, explanations, training value. Limitations: the **knowledge-acquisition bottleneck** (experts find it hard to state what they know), **brittleness** at the edge of the domain (the system does not know what it does not know), no common sense, no learning unless added, and maintenance cost as the rule base grows into thousands of interacting rules. These are the reasons expert systems were overtaken by machine learning for perception-like tasks, though rules remain strong where transparency and legal accountability matter.

## 6.2 Machine vision

**Computer or machine vision** extracts information from images and video so that a machine can act on it. A **digital image** is a grid of **pixels**, each a number: 0–255 for an 8-bit grey level (0 black, 255 white), or three numbers for red, green and blue. A 1920 × 1080 colour image has 2,073,600 pixels and 6,220,800 numbers (about 6 MB uncompressed).

### Steps of machine vision

1. **Image acquisition**: a camera or scanner captures the scene; lighting, resolution and lens matter as much as software.
2. **Preprocessing**: improve the image: noise removal (smoothing filters, the median filter), contrast enhancement (histogram equalisation), resizing, conversion to grey.
3. **Segmentation**: divide the image into regions or objects: **thresholding** (pixel > T becomes foreground), **edge detection**, **region growing**, clustering.
4. **Feature extraction**: measure properties of each region: area, perimeter, shape, colour histogram, texture, corners.
5. **Classification and recognition**: decide what each object is, using rules or a learned classifier (k-NN, a neural network; **convolutional neural networks** learn the features themselves).
6. **Interpretation and action**: understand the scene (a count, a defect, a name, a position) and act: reject a part, open a gate, report a result.

Vision is described at three levels: **low-level** (pixels in, pixels out: filtering, edges), **mid-level** (regions, shapes, motion) and **high-level** (objects, scenes, meaning).

### Edge detection by convolution

An **edge** is a place where brightness changes quickly. A **filter (kernel)** is a small matrix slid over the image; at each position the products of kernel and pixels are summed (**convolution**). The Sobel kernels respond to horizontal and vertical brightness changes:

Gx = [[−1, 0, 1], [−2, 0, 2], [−1, 0, 1]]  and  Gy = [[−1, −2, −1], [0, 0, 0], [1, 2, 1]].

The edge strength is √(Gx² + Gy²).

::: example A vertical edge
A 5 × 5 image has every row 0, 0, 10, 10, 10: a dark band on the left, a bright one on the right, and a vertical edge between columns 1 and 2 (columns numbered 0 to 4). Filtering the interior pixels, centred on columns 1, 2 and 3: for column 1 the left neighbours (column 0) are 0 and the right ones (column 2) are 10, so Gx = (10 − 0) × (1 + 2 + 1) = **40**; for column 2 the left side (column 1) is 0 and the right side (column 3) is 10, again **40**; for column 3 both sides are 10, so Gx = **0**. Gy = 0 everywhere because each column is constant vertically. The result [40, 40, 0] marks the edge, two pixels wide because the 3 × 3 kernel straddles it from either side, and shows nothing in the flat bright region.
:::

### Applications

Quality inspection in factories (finding defects at line speed), optical character recognition (including Devanagari scripts and number plates), face detection and recognition, medical imaging (spotting tumours or retinal disease), traffic monitoring, agriculture (plant disease from leaf photos, crop counting from drone images), robot navigation and self-driving cars, document scanning and satellite image analysis (landslide and flood mapping, important for Nepal). Concerns: **privacy** and surveillance, **bias** (face recognition accuracy differs across groups), and the need for human oversight of high-stakes decisions.

### Challenges

Variation in lighting, viewpoint, scale and occlusion; the vast number of object classes; 3-D structure inferred from 2-D projection; the need for large labelled datasets; adversarial examples (tiny, deliberate pixel changes that fool a classifier).

## Practising the commands

The first program is a small forward-chaining inference engine with certainty factors, running the rule base of Section 6.1.

```python
rules = [("R1", {"fever", "cough"}, "flu_suspect"), ("R2", {"flu_suspect", "body_ache"}, "flu"),
         ("R3", {"flu"}, "advise_rest_and_fluids"), ("R4", {"rash", "fever"}, "measles_suspect")]
facts = {"fever", "cough", "body_ache"}; cycle = 0
while True:
    fired = [(n, c) for n, p, c in rules if p <= facts and c not in facts]
    if not fired: break
    cycle += 1; name, concl = fired[0]; facts.add(concl)
    print("cycle", cycle, "fire", name, "->", concl)
print("final facts:", sorted(facts), "| measles derived:", "measles_suspect" in facts)
combine = lambda a, b: a + b * (1 - a) if a >= 0 and b >= 0 else (a + b) / (1 - min(abs(a), abs(b)))
print("CF combine 0.6, 0.5 ->", round(combine(0.6, 0.5), 3), "| 0.6, -0.4 ->", round(combine(0.6, -0.4), 3))
print("rule CF 0.9 with premises 0.8, 0.6 ->", round(0.9 * min(0.8, 0.6), 2))
```
```output
cycle 1 fire R1 -> flu_suspect
cycle 2 fire R2 -> flu
cycle 3 fire R3 -> advise_rest_and_fluids
final facts: ['advise_rest_and_fluids', 'body_ache', 'cough', 'fever', 'flu', 'flu_suspect'] | measles derived: False
CF combine 0.6, 0.5 -> 0.8 | 0.6, -0.4 -> 0.333
rule CF 0.9 with premises 0.8, 0.6 -> 0.54
```
The second program applies the Sobel filter to the 5 × 5 image of Section 6.2 and thresholds the result.

```python
import math
image = [[0, 0, 10, 10, 10] for _ in range(5)]
GX = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]; GY = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
def conv(img, k, r, c): return sum(k[i][j] * img[r + i - 1][c + j - 1] for i in range(3) for j in range(3))
print("Gx:")
for r in range(1, 4): print([conv(image, GX, r, c) for c in range(1, 4)])
print("edge strength:")
for r in range(1, 4): print([round(math.hypot(conv(image, GX, r, c), conv(image, GY, r, c))) for c in range(1, 4)])
edges = [["#" if math.hypot(conv(image, GX, r, c), conv(image, GY, r, c)) > 20 else "." for c in range(1, 4)] for r in range(1, 4)]
print("thresholded (> 20):"); print("\n".join("".join(row) for row in edges))
print("pixels in a 1920x1080 colour image:", 1920 * 1080, "numbers:", 1920 * 1080 * 3)
```
```output
Gx:
[40, 40, 0]
[40, 40, 0]
[40, 40, 0]
edge strength:
[40, 40, 0]
[40, 40, 0]
[40, 40, 0]
thresholded (> 20):
##.
##.
##.
pixels in a 1920x1080 colour image: 2073600 numbers: 6220800
```
## 6.3 Seeing the ideas: expert systems and machine vision

This section ties each idea of the unit to a picture and to a computed figure. Plate 6.1 shows the people and machines behind the first expert systems, and Figures 6.1 to 6.6 run the architecture, forward and backward chaining, certainty factors, the development stages and the cost of a growing rule base. Plates 6.2 and 6.3 show how images are formed and captured, and Figures 6.7 to 6.13 treat an image as numbers, then clean, segment and filter it, with a small convolutional network and a fair way to score the result. Plates 6.4 and 6.5 show vision at work on satellite and medical images. Every number in a caption was printed by the figure code.

```photogrid label="6.1" cols="4" ratio="1.0" caption="Where expert systems came from. (a) Edward Shortliffe (CC0), who at Stanford built MYCIN, the blood-infection adviser with about 600 rules. (b) A DEC VAX 11/780 (CC BY-SA 3.0): XCON, also called R1, checked and completed orders for computers of the VAX family at DEC. (c) A hyperbolic quadrupole mass analyser (CC BY-SA 3.0), the kind of instrument whose spectra DENDRAL interpreted to propose molecular structures. (d) A hospital ward with a central monitoring station (US Navy, public domain): alarm and monitoring software applies stored rules to patient data, the same style of reasoning."
@ photo id="bca302/shortliffe" cap="Shortliffe: MYCIN"
fit 1.0
focus 0.5 0.5
@ photo id="bca302/vax" cap="VAX 11/780 that XCON configured"
fit 1.0
focus 0.5 0.5
@ photo id="bca302/massspec" cap="Mass analyser (DENDRAL data)"
fit 1.0
focus 0.5 0.5
@ photo id="bca302/icu" cap="Central monitoring of patients"
fit 1.0
focus 0.4 0.5
```

```svgfig label="6.1" caption="An expert system. The knowledge engineer interviews the domain expert and enters the rules through the acquisition module into the knowledge base. The inference engine matches the rules against the facts in working memory, the interface talks to the user, and the explanation facility shows why a question was asked and how a result was reached. Because the knowledge base is separate from the engine, new rules make a new expert system."
f = Fig(580, 262)
f.text(290, 14, "an expert system: knowledge kept apart from the engine", size=11.5, color=NAVY, bold=True)
f.box(8, 34, 104, 36, "Domain expert", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(8, 112, 104, 36, "Knowledge\nengineer", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(60, 70), (60, 112)], color=AMBER, label="interviews", lpos=(88, 96), lsize=9.5)
f.box(140, 112, 130, 36, "Knowledge acquisition\nmodule", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.arrow([(112, 130), (140, 130)], color=SLATE)
f.box(140, 34, 130, 50, "Knowledge base\nIF-THEN rules", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.arrow([(205, 112), (205, 84)], color=SLATE)
f.box(310, 34, 120, 50, "Inference engine\nmatch, fire, chain", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.arrow([(270, 59), (310, 59)], color=SLATE, both=True)
f.box(310, 112, 120, 36, "Working memory\n(facts of this case)", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.arrow([(370, 84), (370, 112)], color=SLATE, both=True)
f.box(310, 184, 120, 40, "Explanation facility\nwhy? how?", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
f.arrow([(370, 184), (370, 148)], color=SLATE, dash=True)
f.box(468, 34, 104, 50, "User interface\nquestions, advice", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.arrow([(430, 59), (468, 59)], color=SLATE, both=True)
f.box(468, 112, 104, 36, "User", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(520, 84), (520, 112)], color=SLATE, both=True)
f.arrow([(430, 204), (520, 204), (520, 148)], color=SLATE, dash=True)
f.text(8, 196, "Examples: MYCIN, about 600 rules", size=9.5, color=SLATE, anchor="start")
f.text(8, 212, "XCON/R1, thousands of rules", size=9.5, color=SLATE, anchor="start")
f.text(8, 228, "Shells: CLIPS, Jess, Drools", size=9.5, color=SLATE, anchor="start")
f.text(290, 250, "change the rules and the same engine gives a new expert system", size=10, color=NAVY, bold=True)
```

```svgfig label="6.2" caption="Forward chaining run by the figure code on the rules R1 to R4. In case A (fever, cough, body_ache) R1, R2 and R3 fire in three cycles and the run ends with 6 facts; measles_suspect is never derived. In case B, with rash added, two rules are eligible in each of the first three cycles and one in the fourth, so the first eligible rule in the list fires each time; 4 rules fire and the run ends with 8 facts."
f = Fig(580, 262)
rules = [("R1", {"fever", "cough"}, "flu_suspect"), ("R2", {"flu_suspect", "body_ache"}, "flu"),
         ("R3", {"flu"}, "advise_rest"), ("R4", {"rash", "fever"}, "measles_suspect")]
def run(facts):
    facts = set(facts); log = []
    while True:
        el = [r for r in rules if r[1] <= facts and r[2] not in facts]
        if not el:
            log.append((None, [], None)); break
        pick = el[0]; facts.add(pick[2])
        log.append((pick, [r[0] for r in el], pick[2]))
    return log, facts
A, fa = run({"fever", "cough", "body_ache"})
B, fb = run({"fever", "cough", "body_ache", "rash"})
assert [x[0][0] for x in A[:-1]] == ["R1", "R2", "R3"] and "measles_suspect" not in fa and len(fa) == 6
assert [x[0][0] for x in B[:-1]] == ["R1", "R2", "R3", "R4"] and [len(x[1]) for x in B[:-1]] == [2, 2, 2, 1] and len(fb) == 8
f.text(290, 14, "forward chaining run in the figure code (first eligible rule fires)", size=11.5, color=NAVY, bold=True)
def panel(x0, title, facts, log, fin):
    f.text(x0 + 135, 38, title, size=10.5, color=TEAL, bold=True)
    f.text(x0, 56, "start: " + facts, size=9.5, color=SLATE, anchor="start")
    for i, (pick, el, new) in enumerate(log):
        y = 70 + i * 30
        if pick is None:
            f.box(x0, y, 270, 24, "%d  no rule is eligible: stop" % (i + 1), fill=SOFT, stroke="#94a3b8", size=9.5, color=SLATE, anchor="start")
        else:
            f.box(x0, y, 270, 24, "%d  eligible %s: fire %s, add %s" % (i + 1, ", ".join(el), pick[0], new), fill=MINT, stroke=TEAL, size=9.5, color=SLATE, anchor="start")
    f.text(x0, 70 + len(log) * 30 + 8, fin, size=9.5, color=NAVY, bold=True, anchor="start")
panel(8, "case A: no rash", "fever, cough, body_ache", A, "end: %d facts, no measles_suspect" % len(fa))
panel(300, "case B: rash as well", "fever, cough, body_ache, rash", B, "end: %d facts, 4 rules fired" % len(fb))
f.text(290, 252, "the conflict set shrinks 2, 2, 2, 1: listing order is the conflict-resolution rule", size=10, color=SLATE)
```

```svgfig label="6.3" caption="Backward chaining on the same rules. To prove flu the engine asks about fever, cough and body_ache in that order, 3 questions. If fever is no it asks only 1 question, and for the goal measles with rash = no it also asks only 1. Forward chaining would first need all 4 symptom answers."
f = Fig(580, 250)
rules = {"flu": [["flu_suspect", "body_ache"]], "flu_suspect": [["fever", "cough"]], "measles_suspect": [["rash", "fever"]]}
def prove(goal, ans, asked):
    if goal in rules:
        for body in rules[goal]:
            if all(prove(g, ans, asked) for g in body):
                return True
        return False
    if goal not in asked:
        asked.append(goal)
    return ans[goal]
yes = {"fever": True, "cough": True, "body_ache": True, "rash": False}
cases = []
for goal, ans, label in [("flu", yes, "goal flu, all answers yes"), ("flu", dict(yes, fever=False), "goal flu, fever = no"),
                         ("measles_suspect", yes, "goal measles, rash = no")]:
    asked = []; r = prove(goal, ans, asked); cases.append((label, asked, r))
assert [len(c[1]) for c in cases] == [3, 1, 1] and [c[2] for c in cases] == [True, False, False]
f.text(150, 14, "goal tree for flu", size=11.5, color=NAVY, bold=True)
f.box(95, 28, 110, 30, "flu", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(20, 96, 120, 30, "flu_suspect", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(170, 96, 110, 30, "body_ache?", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(130, 58), (80, 96)], color=SLATE); f.arrow([(170, 58), (225, 96)], color=SLATE)
f.box(2, 164, 80, 30, "fever?", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(98, 164, 80, 30, "cough?", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(60, 126), (42, 164)], color=SLATE); f.arrow([(100, 126), (138, 164)], color=SLATE)
for (cx, cy, n) in [(14, 158, 1), (110, 158, 2), (182, 90, 3)]:
    f.circle(cx, cy, 8, fill=RED, stroke=RED, label=str(n), size=9.5, color="#ffffff")
f.text(150, 220, "red numbers: the order of the questions;", size=9.5, color=SLATE)
f.text(150, 234, "the AND of a rule stops at its first false part", size=9.5, color=SLATE)
f.text(430, 14, "questions asked (forward chaining needs all 4)", size=11, color=NAVY, bold=True)
for i, (label, asked, r) in enumerate(cases):
    y = 40 + i * 70
    f.text(310, y, label, size=10, color=TEAL, bold=True, anchor="start")
    for k in range(4):
        on = k < len(asked)
        f.box(310 + k * 62, y + 10, 54, 22, asked[k] if on else "not asked", fill=SAND if on else SOFT, stroke=AMBER if on else "#cbd5e1", size=9.5 if on else 9.5, color=SLATE if on else "#64748b")
    f.text(310, y + 48, "%d of 4 asked, conclusion: %s" % (len(asked), "flu proved" if r else "not proved"), size=9.5, color=NAVY, bold=True, anchor="start")
```

```svgfig label="6.4" caption="Certainty factors computed. A rule with CF 0.9 and premises 0.8 and 0.6 gives 0.9 x 0.6 = 0.54. Two supporting rules with 0.6 and 0.5 give 0.6 + 0.5 x 0.4 = 0.80. Opposite evidence 0.6 and -0.4 gives 0.2 / 0.6 = 0.333. In the graph the teal line is the combined CF for CF1 = 0.6 as CF2 grows from 0 to 1: it rises from 0.6 to 1 and never passes 1."
f = Fig(580, 262)
cf_and = 0.9 * min(0.8, 0.6)
cf_same = 0.6 + 0.5 * (1 - 0.6)
cf_opp = (0.6 + (-0.4)) / (1 - min(abs(0.6), abs(-0.4)))
assert round(cf_and, 2) == 0.54 and round(cf_same, 2) == 0.8 and round(cf_opp, 3) == 0.333
f.text(150, 14, "three certainty-factor rules", size=11.5, color=NAVY, bold=True)
rows = [("rule: IF A AND B THEN C", "CF(A) = 0.8, CF(B) = 0.6, CF_r = 0.9", "CF(C) = 0.9 x min(0.8, 0.6) = %.2f" % cf_and, TEAL),
        ("two rules, same sign", "CF1 = 0.6, CF2 = 0.5", "CF = 0.6 + 0.5 x (1 - 0.6) = %.2f" % cf_same, AMBER),
        ("opposite signs", "CF1 = 0.6, CF2 = -0.4", "CF = (0.6 - 0.4) / (1 - 0.4) = %.3f" % cf_opp, RED)]
for i, (t, a, b, c) in enumerate(rows):
    y = 34 + i * 70
    f.box(6, y, 288, 60, "", fill=SOFT, stroke=c)
    f.text(14, y + 14, t, size=10, color=c, bold=True, anchor="start")
    f.text(14, y + 32, a, size=9.5, color=SLATE, anchor="start")
    f.text(14, y + 49, b, size=10, color=NAVY, bold=True, anchor="start")
f.text(440, 14, "evidence reinforces but never passes 1", size=11, color=NAVY, bold=True)
a = Axes(f, 330, 30, 230, 170, (0, 1), (0, 1)); a.grid(0.25, 0.25).axes("CF2 (second rule)", "combined CF")
a.curve(lambda x: 0.6 + x * 0.4, 0, 1, color=TEAL, sw=2.4)
a.curve(lambda x: x, 0, 1, color="#94a3b8", sw=1.2, dash=True)
a.pt(0.5, 0.8, "0.8", color=RED, dx=6, dy=14)
f.text(445, 236, "teal: CF1 = 0.6 plus a second rule CF2", size=9.5, color=TEAL, bold=True)
f.text(445, 250, "dashed: CF2 alone", size=9.5, color=SLATE)
```

```svgfig label="6.5" caption="The six stages of expert-system development. Stages 1 to 4 build the system and stage 5 compares it with the expert and with real cases; the dashed red arrow shows that test results send the knowledge engineer back to the rules. Maintenance never ends, because the domain keeps changing."
f = Fig(580, 232)
f.text(290, 14, "six stages of building an expert system, with a loop of test and refine", size=11.5, color=NAVY, bold=True)
st = [("1 Identification", "problem, expert,\ngoals"), ("2 Conceptualisation", "concepts, relations,\nstrategy"), ("3 Formalisation", "rules or frames,\nchoose a shell"),
      ("4 Implementation", "rules + interface,\nquick prototype"), ("5 Testing", "compare with\nexpert and cases"), ("6 Maintenance", "update rules as\nthe domain changes")]
pos = [(10, 36), (200, 36), (390, 36), (390, 136), (200, 136), (10, 136)]
for (t, d), (x, y) in zip(st, pos):
    f.box(x, y, 180, 62, "", fill=BLUE if int(t[0]) < 5 else MINT, stroke=NAVY if int(t[0]) < 5 else TEAL)
    f.text(x + 90, y + 17, t, size=10.5, color=NAVY, bold=True)
    f.text(x + 90, y + 40, d, size=9.5, color=SLATE)
f.arrow([(190, 67), (200, 67)], color=SLATE); f.arrow([(380, 67), (390, 67)], color=SLATE)
f.arrow([(480, 98), (480, 136)], color=SLATE); f.arrow([(390, 167), (380, 167)], color=SLATE)
f.arrow([(200, 167), (190, 167)], color=SLATE)
f.arrow([(290, 136), (290, 117), (430, 117), (430, 98)], color=RED, dash=True)
f.text(360, 110, "refine rules", size=9.5, color=RED, bold=True)
f.text(290, 224, "Testing sends you back to the rules until the expert and the system agree", size=10, color=SLATE)
```

```svgfig label="6.6" caption="Why large rule bases are hard to maintain. For n rules there are n(n-1)/2 pairs that might overlap, contradict or hide each other: 45 pairs for 10 rules, 4,950 for 100, 179,700 for 600 (about the size of MYCIN) and 1,999,000 for 2,000 rules. Bars are on a log scale."
f = Fig(580, 232)
ns = [10, 100, 600, 2000]
pairs = [n * (n - 1) // 2 for n in ns]
assert pairs == [45, 4950, 179700, 1999000]
f.text(290, 14, "rule pairs that could clash or overlap, n(n-1)/2, on a log scale", size=11.5, color=NAVY, bold=True)
cm = __import__("math")
for i, (n, p) in enumerate(zip(ns, pairs)):
    y = 34 + i * 44
    w = 380 * cm.log10(p) / cm.log10(2000000)
    f.text(8, y + 15, "%d rules" % n, size=10.5, color=NAVY, bold=True, anchor="start")
    f.box(90, y, w, 28, "", fill=[MINT, MINT, SAND, ROSE][i], stroke=[TEAL, TEAL, AMBER, RED][i])
    f.text(90 + w + 8, y + 15, "{:,} pairs".format(p), size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
f.text(8, 214, "MYCIN had about 600 rules: every added rule must be checked against all the others", size=10, color=SLATE, anchor="start")
```

```photogrid label="6.2" cols="3" ratio="0.8" caption="How an image comes to be numbers. (a) A recording by Hubel and Wiesel (CC BY-SA 3.0) of a visual-cortex neuron that fires only for a line of one orientation: the biological idea behind edge detectors. (b) A Bayer filter (CC BY 2.0): the top half is the scene and the bottom half is what the sensor records, one colour per photosite; the camera estimates the other two colours from the neighbours. (c) A phone screen under a microscope (CC BY 3.0): every pixel is built from red, green and blue parts, the same three numbers per pixel that Figure 6.7 shows."
@ photo id="bca302/hubel" cap="Neuron that responds to one orientation"
fit 0.8
focus 0.5 0.5
@ photo id="bca302/bayer" cap="Bayer sensor: one colour per photosite"
fit 0.8
focus 0.5 0.5
@ photo id="bca302/pixels" cap="Screen pixels: red, green, blue"
fit 0.8
focus 0.5 0.5
```

```svgfig label="6.7" caption="A digital image is a grid of numbers. Left: the digit 7 as an 8 x 8 grid of grey levels from 0 (black) to 255 (white); the small differences from 25 and 215 imitate sensor noise. Right: a colour pixel is three numbers, here (220, 30, 40), a strong red. Sizes computed from width x height x bytes per pixel: 307,200 bytes for 640 x 480 grey, 6,220,800 bytes (5.93 MiB) for full HD colour, 36,000,000 bytes (34.33 MiB) for a 12 MP photo and 186,624,000 bytes (177.98 MiB) for one second of raw full HD video at 30 frames per second."
f = Fig(580, 300)
pat = ["........", "#######.", "......#.", ".....#..", "....#...", "...#....", "...#....", "...#...."]
g = lambda v: "#%02x%02x%02x" % (v, v, v)
m = [[(215 if ch == "#" else 25) + (r * 7 + c * 5) % 17 for c, ch in enumerate(row)] for r, row in enumerate(pat)]
f.text(114, 14, "an image is a grid of numbers", size=11.5, color=NAVY, bold=True)
for r in range(8):
    for c in range(8):
        v = m[r][c]
        f.box(10 + c * 26, 28 + r * 26, 26, 26, str(v), fill=g(v), stroke="#94a3b8", size=9.5, color="#ffffff" if v < 110 else "#111827", r=0, sw=0.8, bold=True)
f.text(114, 250, "8 x 8 = 64 grey levels, 0 black to 255 white", size=9.5, color=SLATE)
f.text(114, 266, "each box is one pixel, here the digit 7", size=9.5, color=SLATE)
f.text(400, 14, "a colour pixel is three numbers", size=11.5, color=NAVY, bold=True)
for i, (nm, v, col) in enumerate([("R", 220, "#dc2626"), ("G", 30, "#16a34a"), ("B", 40, "#2563eb")]):
    f.text(250, 40 + i * 20, nm, size=10, color=SLATE, bold=True)
    f.box(262, 31 + i * 20, 180 * v / 255, 14, "", fill=col, stroke=col, r=2)
    f.text(272 + 180 * v / 255, 39 + i * 20, str(v), size=9.5, color=SLATE, bold=True, anchor="start", vmid=True)
f.box(500, 30, 62, 52, "", fill="#dc1e28", stroke=NAVY)
f.text(531, 96, "(220, 30, 40)", size=9.5, color=SLATE, bold=True)
sizes = [("640 x 480 grey", 640 * 480), ("1920 x 1080 colour", 1920 * 1080 * 3), ("4000 x 3000 colour (12 MP)", 4000 * 3000 * 3), ("1 s of full HD video at 30 fps", 1920 * 1080 * 3 * 30)]
assert [s[1] for s in sizes] == [307200, 6220800, 36000000, 186624000]
f.text(250, 128, "uncompressed size = width x height x bytes per pixel", size=10, color=TEAL, bold=True, anchor="start")
for i, (nm, b) in enumerate(sizes):
    y = 142 + i * 36
    f.box(250, y, 320, 30, "", fill=SOFT, stroke="#cbd5e1")
    f.text(258, y + 11, nm, size=9.5, color=NAVY, bold=True, anchor="start")
    f.text(258, y + 23, "{:,} bytes = {:.2f} MiB".format(b, b / 1048576), size=9.5, color=SLATE, anchor="start")
```

```svgfig label="6.8" caption="The first four steps of machine vision on a 12 x 12 image with two bright objects, three salt pixels and two pepper pixels. Thresholding the raw image finds 5 regions: three single-pixel specks and two objects with a hole (areas 15 and 19). After a 3 x 3 median filter the noise is gone and thresholding finds exactly 2 regions of 12 and 16 pixels; the median also rounds their corners, so the measured areas are a little below the true 16 and 20."
f = Fig(580, 262)
g = lambda v: "#%02x%02x%02x" % (v, v, v)
N = 12
img = [[40 for _ in range(N)] for _ in range(N)]
for r in range(2, 6):
    for c in range(2, 6):
        img[r][c] = 200
for r in range(7, 11):
    for c in range(6, 11):
        img[r][c] = 200
for (r, c) in [(0, 9), (5, 0), (11, 2)]:
    img[r][c] = 255
for (r, c) in [(3, 3), (9, 8)]:
    img[r][c] = 0
def median(im):
    out = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            v = sorted(im[min(N - 1, max(0, r + dr))][min(N - 1, max(0, c + dc))] for dr in (-1, 0, 1) for dc in (-1, 0, 1))
            out[r][c] = v[4]
    return out
def comps(b):
    seen = set(); res = []
    for r in range(N):
        for c in range(N):
            if b[r][c] and (r, c) not in seen:
                st = [(r, c)]; seen.add((r, c)); cells = []
                while st:
                    y, x = st.pop(); cells.append((y, x))
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        yy, xx = y + dy, x + dx
                        if 0 <= yy < N and 0 <= xx < N and b[yy][xx] and (yy, xx) not in seen:
                            seen.add((yy, xx)); st.append((yy, xx))
                res.append(cells)
    return res
thr = lambda im: [[1 if v > 120 else 0 for v in row] for row in im]
raw_c = comps(thr(img)); flt = median(img); fb = thr(flt); fc = comps(fb)
areas = sorted(len(c) for c in fc)
assert areas == [12, 16] and len(fc) == 2 and sorted(len(c) for c in raw_c) == [1, 1, 1, 15, 19]
cs = 11
def draw(x0, grid, tint=None):
    for r in range(N):
        for c in range(N):
            f.box(x0 + c * cs, 34 + r * cs, cs, cs, "", fill=g(grid[r][c]), stroke="#e2e8f0", r=0, sw=0.4)
titles = [("1 acquire", "with salt and\npepper noise"), ("2 preprocess", "3 x 3 median\nfilter"), ("3 segment", "threshold at 120\n(1 = object)"), ("4 features", "label regions,\nmeasure area")]
xs = [8, 150, 292, 434]
draw(xs[0], img); draw(xs[1], flt)
draw(xs[2], [[255 if v else 0 for v in row] for row in fb])
lab = [[255] * N for _ in range(N)]
draw(xs[3], lab)
cols = ["#60a5fa", "#fbbf24"]
for k, cells in enumerate(sorted(fc, key=lambda c: min(c))):
    for (y, x) in cells:
        f.box(xs[3] + x * cs, 34 + y * cs, cs, cs, "", fill=cols[k], stroke="#e2e8f0", r=0, sw=0.4)
for i, (t, d) in enumerate(titles):
    f.text(xs[i] + 66, 22, t, size=10.5, color=NAVY, bold=True)
    f.text(xs[i] + 66, 188, d, size=9.5, color=SLATE)
for i in range(3):
    f.arrow([(xs[i] + 134, 100), (xs[i + 1] - 2, 100)], color=SLATE)
sc = sorted(fc, key=lambda c: min(c))
f.text(xs[3] + 66, 222, "A: %d px   B: %d px" % (len(sc[0]), len(sc[1])), size=10, color=RED, bold=True)
f.text(290, 244, "raw image: %d regions (3 specks, 2 objects with a hole); median-filtered: %d regions, corners rounded" % (len(raw_c), len(fc)), size=10, color=NAVY, bold=True)
```

```photogrid label="6.3" cols="4" ratio="1.0" caption="Cameras and sensors that feed a vision system. (a) A pair of automatic number-plate recognition cameras on a pole (CC0). (b) A laptop fingerprint reader (CC0): the small strip images the ridges of a finger. (c) A supermarket barcode scanner (public domain): a barcode is a one-dimensional image read line by line. (d) A traffic officer at a Kathmandu junction (CC BY-SA 4.0), a scene of cars, buses and people that traffic cameras must count and separate."
@ photo id="bca302/alpr" cap="Plate-reading cameras"
fit 1.0
focus 0.5 0.5
call 0.38 0.9 0.43 0.6 "ANPR camera"
@ photo id="bca302/fingerprint" cap="Fingerprint sensor"
fit 1.0
focus 0.5 0.5
call 0.5 0.9 0.5 0.56 "sensor strip"
@ photo id="bca302/pricescan" cap="Barcode scanner"
fit 1.0
focus 0.5 0.5
call 0.72 0.9 0.36 0.53 "barcode"
@ photo id="bca302/trafficktm" cap="Kathmandu junction"
fit 1.0
focus 0.5 0.5
call 0.72 0.9 0.42 0.6 "officer"
```

```svgfig label="6.9" caption="Sobel edge detection by hand and by program. Left: for the 5 x 5 image of the text, Gx at the nine interior pixels is 40, 40, 0 in every row and Gy is 0. Right: for a bright 4 x 4 square on a dark background the edge strength is 40 along the sides, up to 42.4 at the corner pixels of the square, and 0 in the flat middle and the flat background."
f = Fig(580, 270)
g = lambda v: "#%02x%02x%02x" % (v, v, v)
cm = __import__("math")
GX = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]; GY = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
def sobel(im):
    n = len(im); out = []
    for r in range(1, n - 1):
        row = []
        for c in range(1, n - 1):
            gx = sum(GX[i][j] * im[r + i - 1][c + j - 1] for i in range(3) for j in range(3))
            gy = sum(GY[i][j] * im[r + i - 1][c + j - 1] for i in range(3) for j in range(3))
            row.append((gx, gy))
        out.append(row)
    return out
a5 = [[0, 0, 10, 10, 10] for _ in range(5)]
s5 = sobel(a5)
assert [p[0] for p in s5[0]] == [40, 40, 0] and all(p[1] == 0 for row in s5 for p in row)
sq = [[10 if 3 <= r <= 6 and 3 <= c <= 6 else 0 for c in range(10)] for r in range(10)]
s10 = sobel(sq); mag = [[cm.hypot(*p) for p in row] for row in s10]
mx = max(max(r) for r in mag)
f.text(75, 14, "a 5 x 5 image and Gx", size=11, color=NAVY, bold=True)
for r in range(5):
    for c in range(5):
        v = a5[r][c]
        f.box(8 + c * 26, 26 + r * 26, 26, 26, str(v), fill=g(v * 22), stroke="#94a3b8", size=9.5, color="#ffffff" if v < 5 else "#111827", r=0, sw=0.8, bold=True)
f.box(8 + 26, 26 + 26, 78, 78, "", fill="none", stroke=RED, r=0, sw=2)
f.text(75, 168, "red window: centre (1,1)", size=9.5, color=RED, bold=True)
f.text(75, 192, "Gx kernel", size=10, color=TEAL, bold=True)
for i in range(3):
    for j in range(3):
        f.box(36 + j * 26, 200 + i * 20, 26, 20, "%d" % GX[i][j], fill=MINT, stroke=TEAL, size=9.5, r=0, sw=0.8, bold=True)
f.arrow([(142, 90), (172, 90)], color=SLATE)
f.text(215, 14, "Gx at the 9 interior pixels", size=10, color=NAVY, bold=True)
for r in range(3):
    for c in range(3):
        v = s5[r][c][0]
        f.box(176 + c * 30, 26 + r * 30, 30, 30, str(v), fill=SAND if v else SOFT, stroke=AMBER if v else "#94a3b8", size=10, r=0, sw=0.9, bold=True)
f.text(221, 130, "[40, 40, 0] in every row:", size=9.5, color=SLATE)
f.text(221, 144, "the edge is found, and Gy = 0", size=9.5, color=SLATE)
f.text(450, 14, "a bright square: edge strength", size=10.5, color=NAVY, bold=True)
c0 = 14
for r in range(10):
    for c in range(10):
        f.box(300 + c * c0, 26 + r * c0, c0, c0, "", fill=g(sq[r][c] * 25), stroke="#cbd5e1", r=0, sw=0.3)
for r in range(8):
    for c in range(8):
        f.box(450 + c * c0, 26 + 7 + r * c0, c0, c0, "", fill=g(int(255 * mag[r][c] / mx)), stroke="#475569", r=0, sw=0.3)
f.text(370, 180, "image (0 and 10)", size=9.5, color=SLATE)
f.text(520, 180, "edge strength, white = strong", size=9.5, color=SLATE)
f.text(430, 210, "maximum strength %.1f at the corners, 40 along the sides" % mx, size=9.5, color=NAVY, bold=True)
f.text(430, 226, "and 0 in the flat middle and the flat background", size=9.5, color=SLATE)
```

```svgfig label="6.10" caption="Choosing a threshold. The histogram is of 2,000 synthetic pixels (1,400 background around grey level 85 and 600 object pixels around 165, seed 3). Otsu's method tries every level and keeps the one that makes the two groups as different as possible: T = 124. Because the two groups overlap, 110 of the 2,000 pixels (5.5 percent) fall on the wrong side."
f = Fig(580, 262)
rnd = __import__("random"); rnd.seed(3)
clip = lambda v: max(0, min(255, int(round(v))))
bg = [clip(rnd.gauss(85, 25)) for _ in range(1400)]
ob = [clip(rnd.gauss(165, 28)) for _ in range(600)]
allv = bg + ob
hist = [0] * 256
for v in allv:
    hist[v] += 1
tot = len(allv); best = (-1, 0)
for t in range(1, 255):
    w0 = sum(hist[:t + 1]) / tot; w1 = 1 - w0
    if w0 == 0 or w1 == 0:
        continue
    m0 = sum(i * hist[i] for i in range(t + 1)) / sum(hist[:t + 1]); m1 = sum(i * hist[i] for i in range(t + 1, 256)) / sum(hist[t + 1:])
    vb = w0 * w1 * (m0 - m1) ** 2
    if vb > best[0]:
        best = (vb, t)
T = best[1]
wrong = sum(1 for v in bg if v > T) + sum(1 for v in ob if v <= T)
bins = [0] * 16
for v in allv:
    bins[v // 16] += 1
assert 100 < T < 150
f.text(290, 14, "threshold chosen by Otsu's method on 2,000 pixels (1,400 background + 600 object)", size=11, color=NAVY, bold=True)
a = Axes(f, 50, 28, 500, 170, (0, 256), (0, 600)); a.grid(32, 100).axes("grey level", "pixels")
for i, n in enumerate(bins):
    f.box(a.X(i * 16), a.Y(n), a.X(16) - a.X(0) - 1, a.Y(0) - a.Y(n), "", fill="#bfdbfe" if i * 16 + 8 <= T else "#fde68a", stroke=NAVY if i * 16 + 8 <= T else AMBER, r=0, sw=0.8)
a.vline(T + 0.5, color=RED, dash=True, sw=2)
f.text(a.X(T) + 6, 40, "T = %d" % T, size=11, color=RED, bold=True, anchor="start")
f.text(a.X(60), 56, "background", size=10, color=NAVY, bold=True)
f.text(a.X(190), 56, "object", size=10, color=AMBER, bold=True)
f.text(290, 244, "grey level above T becomes object: %d of 2,000 pixels fall on the wrong side (%.1f percent)" % (wrong, wrong / 20), size=10, color=SLATE)
```

```svgfig label="6.11" caption="Mean filter against median filter on one scan line of 16 pixels, computed. The spike 200 at position 4 becomes 73.3 on three neighbouring pixels under the mean filter and 10 under the median; the step from 10 to 60 becomes 26.7 and 43.3 under the mean but stays 10 and 60 under the median; the dropout 0 at position 12 becomes 40.0 under the mean and 60 under the median."
f = Fig(580, 262)
s = [10, 10, 10, 10, 200, 10, 10, 10, 60, 60, 60, 60, 0, 60, 60, 60]
n = len(s)
mean = [s[0]] + [sum(s[i - 1:i + 2]) / 3 for i in range(1, n - 1)] + [s[-1]]
med = [s[0]] + [sorted(s[i - 1:i + 2])[1] for i in range(1, n - 1)] + [s[-1]]
assert round(mean[4], 1) == 73.3 and med[4] == 10 and round(mean[7], 1) == 26.7 and round(mean[8], 1) == 43.3 and med[7] == 10 and med[8] == 60
assert round(mean[12], 1) == 40.0 and med[12] == 60
f.text(290, 14, "3-point mean filter against 3-point median filter on one scan line", size=11.5, color=NAVY, bold=True)
a = Axes(f, 44, 28, 340, 190, (0, 15), (0, 210)); a.grid(3, 50).axes("pixel position", "grey level")
def series(v, col, dash=False, r=3):
    for i in range(n - 1):
        f.line(a.X(i), a.Y(v[i]), a.X(i + 1), a.Y(v[i + 1]), color=col, sw=2, dash=dash)
    for i in range(n):
        f.circle(a.X(i), a.Y(v[i]), r, fill=col, stroke=col)
series(s, "#94a3b8", dash=True, r=2.5); series(mean, AMBER); series(med, TEAL)
f.text(410, 40, "raw: spike 200 at 4,", size=9.5, color=SLATE, bold=True, anchor="start")
f.text(410, 54, "dropout 0 at 12, step 10 to 60", size=9.5, color=SLATE, bold=True, anchor="start")
f.text(410, 84, "mean (amber)", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(410, 100, "spike smeared: 73.3 x 3", size=9.5, color=SLATE, anchor="start")
f.text(410, 114, "step becomes 26.7, 43.3", size=9.5, color=SLATE, anchor="start")
f.text(410, 128, "dropout becomes 40.0", size=9.5, color=SLATE, anchor="start")
f.text(410, 158, "median (teal)", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(410, 174, "spike removed: 10", size=9.5, color=SLATE, anchor="start")
f.text(410, 188, "step stays sharp: 10, 60", size=9.5, color=SLATE, anchor="start")
f.text(410, 202, "dropout repaired: 60", size=9.5, color=SLATE, anchor="start")
f.text(290, 246, "the median ignores one extreme value in a window; the mean smears it into its neighbours", size=10, color=SLATE)
```

```svgfig label="6.12" caption="A small convolutional network for 28 x 28 digit images, with sizes and parameters computed: 80 parameters in the first convolution, 1,168 in the second and 4,010 in the dense layer, 5,258 in all. A dense network 784-128-10 on the same input needs 101,770, which is 19.4 times more, because a filter reuses its 9 weights at every position."
f = Fig(580, 276)
conv1 = (3 * 3 * 1 + 1) * 8; conv2 = (3 * 3 * 8 + 1) * 16; dense = 5 * 5 * 16 * 10 + 10
cnn = conv1 + conv2 + dense
mlp = (784 * 128 + 128) + (128 * 10 + 10)
assert (conv1, conv2, dense, cnn, mlp) == (80, 1168, 4010, 5258, 101770)
f.text(290, 14, "a small convolutional network on a 28 x 28 digit image (sizes and parameters computed)", size=11, color=NAVY, bold=True)
st = [("input", "28 x 28 x 1", "0", BLUE, NAVY), ("conv 3 x 3\n8 filters", "26 x 26 x 8", "{:,}".format(conv1), MINT, TEAL), ("max pool\n2 x 2", "13 x 13 x 8", "0", SAND, AMBER),
      ("conv 3 x 3\n16 filters", "11 x 11 x 16", "{:,}".format(conv2), MINT, TEAL), ("max pool\n2 x 2", "5 x 5 x 16 = 400", "0", SAND, AMBER), ("dense", "10 classes", "{:,}".format(dense), ROSE, RED)]
for i, (t, sh, p, fc, sc) in enumerate(st):
    x = 6 + i * 96
    f.box(x, 34, 82, 44, t, fill=fc, stroke=sc, size=9.5, bold=True)
    f.text(x + 41, 94, sh, size=9.5, color=SLATE, bold=True)
    f.text(x + 41, 110, "params: " + p, size=9.5, color=NAVY)
    if i < 5:
        f.arrow([(x + 82, 56), (x + 96, 56)], color=SLATE)
f.text(290, 140, "total parameters of the convolutional network: {:,}".format(cnn), size=11, color=TEAL, bold=True)
f.text(8, 168, "conv network", size=10, color=TEAL, bold=True, anchor="start")
f.box(110, 156, 400 * cnn / mlp, 22, "", fill=MINT, stroke=TEAL)
f.text(120 + 400 * cnn / mlp, 167, "{:,}".format(cnn), size=10, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(8, 202, "dense 784-128-10", size=10, color=RED, bold=True, anchor="start")
f.box(110, 190, 400, 22, "", fill=ROSE, stroke=RED)
f.text(120, 201, "{:,}".format(mlp), size=10, color=RED, bold=True, anchor="start", vmid=True)
f.text(290, 238, "the same 3 x 3 filter slides over the whole image, so its 9 weights are reused everywhere:", size=10, color=SLATE)
f.text(290, 254, "%.1f times fewer parameters than a dense network on the same input" % (mlp / cnn), size=10, color=NAVY, bold=True)
```

```svgfig label="6.13" caption="Judging a vision system on 1,000 bottles of which 50 are cracked. The system finds 45 (TP), misses 5 (FN), raises 13 false alarms (FP) and passes 937 good bottles (TN): precision 0.7759, recall 0.90, F1 0.8333, accuracy 0.982. A system that never flags any bottle has accuracy 0.950 but recall 0.00, so accuracy alone is misleading when defects are rare."
f = Fig(580, 262)
TP, FP, FN, TN = 45, 13, 5, 937
assert TP + FP + FN + TN == 1000
prec = TP / (TP + FP); rec = TP / (TP + FN); acc = (TP + TN) / 1000; f1 = 2 * prec * rec / (prec + rec); never = 950 / 1000
f.text(150, 14, "inspecting 1,000 bottles, 50 truly cracked", size=11.5, color=NAVY, bold=True)
f.text(168, 36, "system says cracked", size=9.5, color=SLATE, bold=True)
f.text(268, 36, "system says fine", size=9.5, color=SLATE, bold=True)
f.text(40, 76, "really\ncracked", size=9.5, color=SLATE, bold=True)
f.text(40, 146, "really\nfine", size=9.5, color=SLATE, bold=True)
f.box(100, 46, 100, 62, "TP = %d" % TP, fill=MINT, stroke=TEAL, size=12, bold=True)
f.box(206, 46, 100, 62, "FN = %d\n(missed)" % FN, fill=ROSE, stroke=RED, size=11, bold=True)
f.box(100, 114, 100, 62, "FP = %d\n(false alarm)" % FP, fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(206, 114, 100, 62, "TN = %d" % TN, fill=BLUE, stroke=NAVY, size=12, bold=True)
f.text(150, 206, "precision = TP / (TP + FP) = %.4f" % prec, size=10, color=NAVY, bold=True)
f.text(150, 222, "recall = TP / (TP + FN) = %.2f" % rec, size=10, color=NAVY, bold=True)
f.text(150, 238, "F1 = 2PR / (P + R) = %.4f" % f1, size=10, color=NAVY, bold=True)
f.text(440, 14, "accuracy can mislead", size=11.5, color=NAVY, bold=True)
for i, (nm, v, c, fc) in enumerate([("this system", acc, TEAL, MINT), ("never flags a bottle", never, RED, ROSE)]):
    y = 40 + i * 62
    f.text(330, y, nm, size=10, color=c, bold=True, anchor="start")
    f.box(330, y + 8, 230 * v, 22, "", fill=fc, stroke=c)
    f.text(338, y + 19, "accuracy %.3f" % v, size=10, color=c, bold=True, anchor="start", vmid=True)
f.text(445, 176, "doing nothing scores 0.950 and finds", size=9.5, color=SLATE)
f.text(445, 190, "no cracked bottle: recall 0.00", size=9.5, color=SLATE)
f.text(445, 210, "with rare defects, report precision", size=9.5, color=NAVY, bold=True)
f.text(445, 224, "and recall, not accuracy", size=9.5, color=NAVY, bold=True)
```

```photogrid label="6.4" cols="3" ratio="1.0" caption="Vision from space. (a) Kathmandu Valley in true colour (NASA World Wind, public domain). (b) The same valley in false colour (public domain): bands are chosen to separate vegetation, which is green, from the built-up area, the purple and pink patch at the centre; this separation is segmentation by pixel values. (c) Two views of the Langtang Valley from NASA Earth Observatory (CC BY 2.0): an avalanche set off by the 25 April 2015 earthquake buried Langtang village, and a Landsat 8 image of 30 April 2015 shows the snow, ice and debris."
@ photo id="bca302/ktmtrue" cap="Kathmandu Valley, true colour"
fit 1.0
focus 0.5 0.5
@ photo id="bca302/ktmfalse" cap="Same valley, false colour"
fit 1.0
focus 0.5 0.5
@ photo id="bca302/langtang" cap="Langtang Valley after the 2015 avalanche"
fit 1.0
focus 0.5 0.5
```

```photogrid label="6.5" cols="2" ratio="1.15" caption="Medical images that vision software reads. (a) A chest radiograph (CC0): lungs appear dark, bone and heart bright, and a diseased region changes the grey levels. (b) A fundus photograph of the retina (CC BY 2.0) showing bleeding after a vein blockage; screening software looks for such red spots, a task for segmentation and classification. Both are images that a trained doctor must still confirm."
@ photo id="bca302/chestxray" cap="Chest radiograph"
fit 1.15
focus 0.5 0.5
@ photo id="bca302/fundus" cap="Retina photograph"
fit 1.15
focus 0.5 0.5
```

### 6.3.1 Eight uses of expert systems and machine vision in Nepal

1. **Loan and credit rules in banks.** A bank writes its lending policy as rules: if the income is above a limit and the loan is below a share of the collateral value, then the application passes to the next step. A rule engine applies these rules in the same way every time and can show which rule led to a refusal (Figure 6.1). Branch staff still decide the borderline cases, and the rules must be changed whenever Nepal Rastra Bank issues a new directive.
2. **Customs and tax rules.** Deciding the duty on an imported item means following many rules about its type, origin and value. A rule-based adviser at a customs office can walk an officer through the questions, like the backward chaining of Figure 6.3, and ask only the questions that matter. This gives similar answers at Birgunj and at Tatopani and leaves a written trail for appeals.
3. **Health protocols for health workers.** Child-illness guidelines used in Nepal's health posts are written as if-then charts: if there is fever and a stiff neck, send the child to the hospital at once. A phone program can hold such rules and ask the questions in order, much as MYCIN did for infections (Plate 6.1). It helps a health assistant who works alone, and it must say clearly when a case lies outside its rules.
4. **Crop and livestock advice.** A farmer describes the colour of the leaves, the weather and the crop stage, and a rule base suggests the likely problem and what to try first. The rules come from agricultural experts, and the certainty factors of Figure 6.4 can show when two symptoms strengthen a diagnosis. Local experts should check the rules for each region, because a rule that works in the Tarai may be wrong in the hills.
5. **Traffic cameras and number plates.** Cameras like those of Plate 6.3 read number plates and count vehicles at busy Kathmandu junctions. The software first finds the plate, then separates the characters and recognises each one, the steps of Figure 6.8. It can help to find a stolen vehicle or to record a red-light offence, but it must be tested in rain, dust and poor light, and the photographs must be stored safely.
6. **Fingerprints and photographs for identity.** The National ID, e-passports and the voters' list all use photographs and fingerprints. A fingerprint reader (Plate 6.3) turns the ridges into an image, finds their features and compares them with the stored record. A match that is not certain should lead to a second check by a person, because worn fingers of farmers and labourers often give poor images.
7. **Satellite maps of floods and landslides.** Images such as those of Plate 6.4 show where land has changed after an earthquake or a monsoon flood. A program separates water, snow, forest and built-up land by their pixel values, the thresholding of Figure 6.10, and compares images taken before and after. This helps agencies such as the Department of Hydrology and Meteorology and ICIMOD to plan relief when roads are cut and nobody can visit.
8. **Reading medical images.** Software can mark suspicious regions on a chest X-ray or an eye photograph (Plate 6.5) so that the doctor looks at those first. In a health camp with a single doctor this can save hours, especially for screening tuberculosis. Because the system can raise false alarms and miss cases, its precision and recall must be measured as in Figure 6.13, and the doctor makes the final decision.

## Formula and fact sheet

- Expert system = knowledge base + inference engine + working memory + explanation + interface; knowledge is separate from the engine.
- Certainty factors: CF(rule conclusion) = CF_r × min(premises); same sign: CF₁ + CF₂(1 − CF₁); opposite signs: (CF₁ + CF₂)/(1 − min|CF|).
- Development: identification, conceptualisation, formalisation, implementation, testing, maintenance.
- Vision pipeline: acquisition → preprocessing → segmentation → feature extraction → recognition → interpretation.
- Sobel: Gx, Gy kernels; edge strength √(Gx² + Gy²).

## Chapter summary

- An expert system captures a specialist's rules in a knowledge base used by a general inference engine, explains its reasoning and handles uncertainty with certainty factors; it is brittle outside its domain and costly to maintain.
- Development goes from identification through formalisation to testing and maintenance, with the knowledge engineer bridging expert and program.
- Machine vision turns pixels into decisions by acquisition, preprocessing, segmentation, feature extraction and recognition; edge detection is a convolution with kernels such as Sobel's.
- Both technologies serve real applications in industry, health and agriculture, with privacy, bias and accountability concerns.

## Practice

1. Define an expert system and list its main components.
2. Distinguish the roles of the domain expert, knowledge engineer and user.
3. Explain forward and backward chaining; run the rule base of Section 6.1 forward with the facts fever, cough, body_ache.
4. Combine certainty factors 0.6 and 0.5; and compute the conclusion CF for a rule with CF 0.9 whose premises have CF 0.8 and 0.6.
5. List the stages of expert-system development.
6. Give three advantages and three limitations of expert systems.
7. List the steps of machine vision with one operation for each.
8. What is a convolution kernel? Compute Gx for the vertical-edge example.
9. Name four applications of machine vision relevant to Nepal.
10. How many numbers are needed to store a 1920 × 1080 colour image?

::: note Answers and worked solutions
**1.** A program that solves problems in a narrow domain at expert level using an explicit knowledge base. Components: knowledge base, working memory, inference engine, user interface, explanation facility, knowledge acquisition module.
**2.** The domain expert supplies the knowledge, the knowledge engineer elicits and encodes it, the user poses cases and consumes the answers.
**3.** Forward: start from facts and fire rules until nothing new appears (data-driven). Backward: start from a goal and prove premises as subgoals (goal-driven). Forward run: R1 → flu_suspect; R2 → flu; R3 → advise_rest_and_fluids; R4 never fires.
**4.** 0.6 + 0.5 × (1 − 0.6) = 0.8. Rule: 0.9 × min(0.8, 0.6) = 0.54.
**5.** Identification, conceptualisation, formalisation, implementation, testing and evaluation, maintenance.
**6.** Advantages: consistency, availability, preservation of expertise, explanation. Limitations: knowledge-acquisition bottleneck, brittleness at the domain edge, no common sense or learning, maintenance cost.
**7.** Acquisition (capture an image), preprocessing (denoise, equalise), segmentation (threshold, edges), feature extraction (area, shape), recognition (classify), interpretation and action.
**8.** A small matrix slid over the image, summing kernel × pixel products. For a pixel with left neighbours 0 and right neighbours 10, Gx = (10 − 0)(1 + 2 + 1) = 40.
**9.** Devanagari OCR for documents and number plates; leaf-disease detection from farmers' phone photos; landslide and flood mapping from satellite images; quality inspection in small factories.
**10.** 1920 × 1080 × 3 = 6,220,800 numbers (2,073,600 pixels).
:::

## Model answers for Unit 6

**Q1. What is an expert system? Describe its architecture and characteristics, and compare it with a conventional program. (10 marks)**

**Introduction.** An **expert system** is a program that solves problems in a narrow field at the level of a human specialist, using knowledge that is written down in an explicit knowledge base. Well-known examples are DENDRAL (molecular structure from mass spectra), MYCIN (blood infections, about 600 rules) and XCON, which configured DEC computer orders (Plate 6.1).

**Architecture (Fig. 6.1).** The **knowledge base** holds the facts and the IF-THEN rules of the field. **Working memory** holds the facts of the case being solved. The **inference engine** matches rules against the facts and decides which rule fires, by forward or backward chaining. The **user interface** asks questions and shows advice. The **explanation facility** answers *why* a question was asked and *how* a conclusion was reached. The **knowledge acquisition module** helps the **knowledge engineer** to enter the rules that the **domain expert** supplies.

**Characteristics.** (1) It is limited to one domain. (2) Knowledge is kept apart from the engine, so rules can be edited without rewriting the program. (3) It explains its reasoning. (4) It can work with uncertain data through certainty factors. (5) It gives the same answer to the same case at any hour.

| Point | Conventional program | Expert system |
|---|---|---|
| Knowledge | mixed into the code | separate knowledge base |
| Method | fixed algorithm | search and inference over rules |
| Data | needs complete input | can work with partial or uncertain input |
| Explanation | none | shows the chain of rules |
| Change | edit and recompile | add or edit a rule |

**Conclusion.** An expert system copies a scarce specialist's rules into a general engine. It is strong where decisions follow clear rules and must be explained, and weak outside its domain.

**Q2. Distinguish forward chaining from backward chaining with an example. (5 marks)**

In **forward chaining** (data-driven) the engine starts from the known facts and fires every rule whose conditions are true, adding new facts until nothing new appears. In **backward chaining** (goal-driven) it starts from a goal and tries to prove it by proving the conditions of a rule that concludes it, asking the user only when a fact is unknown.

**Example (Figs. 6.2 and 6.3).** The rules are R1 IF fever AND cough THEN flu_suspect; R2 IF flu_suspect AND body_ache THEN flu; R3 IF flu THEN advise_rest; R4 IF rash AND fever THEN measles_suspect. With the facts fever, cough and body_ache, forward chaining fires R1, R2 and R3 in three cycles and ends with 6 facts; R4 never fires. With rash added, 4 rules fire and the run ends with 8 facts. Backward chaining with the goal flu asks about fever, cough and body_ache, 3 questions; if the patient has no fever it stops after 1 question.

| Point | Forward | Backward |
|---|---|---|
| Start | facts | goal |
| Best for | monitoring, diagnosis from symptoms | testing one hypothesis |
| Questions | may collect many facts first | only those needed |

**Q3. What are certainty factors? Show how they are combined. (5 marks)**

A **certainty factor** (CF) is a number from −1 (certainly false) through 0 (no evidence) to +1 (certainly true), used in MYCIN to describe how strongly the evidence supports a conclusion when knowledge is uncertain. Each rule also has its own CF, which says how much the rule is trusted.

**Three combination rules (Fig. 6.4).**

1. *One rule with several conditions:* CF(conclusion) = CF of the rule × the minimum CF of the conditions (the maximum for OR). With a rule CF of 0.9 and conditions 0.8 and 0.6 we get 0.9 × 0.6 = **0.54**.
2. *Two rules, same sign:* CF = CF₁ + CF₂ (1 − CF₁). With 0.6 and 0.5 this gives 0.6 + 0.5 × 0.4 = **0.80**. Independent evidence strengthens the belief but the result never passes 1.
3. *Opposite signs:* CF = (CF₁ + CF₂) / (1 − min(|CF₁|, |CF₂|)). With 0.6 and −0.4 this gives 0.2 / 0.6 = **0.333**.

**Remark.** Certainty factors are heuristics, not true probabilities; Bayesian networks are the principled alternative.

**Q4. Explain the stages of expert-system development. State the advantages and limitations of expert systems. (10 marks)**

**Introduction.** Building an expert system is a team effort of the domain expert, the knowledge engineer and the user. It follows six stages, and the work is repeated until the system agrees with the expert (Fig. 6.5).

1. **Identification:** define the problem, the expert, the resources and the goals, and decide that an expert system suits the task: a narrow field with a real, available expert.
2. **Conceptualisation:** find the key concepts, their relations and the problem-solving strategy.
3. **Formalisation:** choose a representation (rules or frames) and a tool or shell such as CLIPS or Drools.
4. **Implementation:** write the knowledge base and interface, and build a quick prototype.
5. **Testing and evaluation:** compare the answers with the expert's and with real cases, and correct the rules.
6. **Maintenance:** update the rules when the field changes; stale knowledge is dangerous.

**Advantages.** Consistent decisions; available at any hour; rare expertise is preserved; reasoning can be explained; useful for training.

**Limitations.** The **knowledge-acquisition bottleneck**: experts find it hard to say what they know. **Brittleness**: the system does not know when a case lies outside its field. No common sense and no learning unless added. **Maintenance cost**: for n rules there are n(n−1)/2 pairs that may clash, which is 179,700 for 600 rules and 1,999,000 for 2,000 (Fig. 6.6).

| Aspect | Advantage | Limitation |
|---|---|---|
| Knowledge | kept and shared | hard to collect |
| Decisions | consistent | fail at the edge of the domain |
| Change | edit rules | large rule bases clash |

**Conclusion.** Expert systems remain useful where rules are clear and decisions must be explained, such as loan policy and health protocols, while learning methods have taken over perception tasks.

**Q5. Describe the steps of machine vision with a small example. (10 marks)**

**Introduction.** **Machine vision** extracts information from images so that a machine can act. A digital image is a grid of pixels, each a number (Fig. 6.7): a grey pixel is 0 to 255, and a colour pixel has three numbers for red, green and blue. A full-HD colour image has 2,073,600 pixels and 6,220,800 numbers, about 5.93 MiB uncompressed.

**Steps (Fig. 6.8).**

1. **Image acquisition:** a camera or scanner captures the scene; lighting and lens matter as much as software (Plate 6.3).
2. **Preprocessing:** remove noise (median filter) and improve contrast. In the example a 3 × 3 median filter removes five bad pixels.
3. **Segmentation:** split the image into regions by thresholding, edges or region growing. Thresholding at 120 turns the 12 × 12 image into object and background.
4. **Feature extraction:** measure each region: area, perimeter, shape, colour. The example finds two regions of 12 and 16 pixels.
5. **Classification and recognition:** decide what each object is with rules, k-NN or a convolutional network.
6. **Interpretation and action:** use the result: count, reject a part, open a gate.

| Level | Input to output | Examples |
|---|---|---|
| Low | pixels to pixels | filtering, edges |
| Middle | pixels to regions | segmentation, shape, motion |
| High | regions to meaning | object recognition, scene understanding |

Without the median filter, thresholding of the raw example gave 5 regions (three single-pixel specks and two objects with holes), so the later steps would be wrong.

**Conclusion.** Each step prepares the next, so an error early in the chain, such as noise, spreads to the final decision.

**Q6. What is a convolution kernel? Detect a vertical edge with the Sobel filter. (5 marks)**

An **edge** is a place where brightness changes quickly. A **kernel** is a small matrix that is slid over the image; at each position the products of the kernel and the pixels under it are added, which is called **convolution**. The Sobel kernels are Gx = [[−1, 0, 1], [−2, 0, 2], [−1, 0, 1]] for changes from left to right and Gy = [[−1, −2, −1], [0, 0, 0], [1, 2, 1]] for changes from top to bottom. The edge strength is √(Gx² + Gy²).

**Example (Fig. 6.9).** Take a 5 × 5 image in which every row is 0, 0, 10, 10, 10. For the pixel in column 1 the left column holds 0 and the right column holds 10, so Gx = 10 × (1 + 2 + 1) − 0 = **40**. In column 2 the left column is 0 and the right is 10, so Gx = **40**. In column 3 both sides are 10 so Gx = **0**. Every column is constant from top to bottom, so Gy = 0. The result [40, 40, 0] marks the edge, two pixels wide because the 3 × 3 window sees it from both sides.

On a bright 4 × 4 square on a dark background the same filters give 40 along the sides, up to 42.4 at the corner pixels and 0 in flat areas, so the outline of the square appears.

**Q7. Explain noise removal and thresholding in preprocessing and segmentation. (5 marks)**

**Noise removal.** Sensors add random errors such as salt (white) and pepper (black) pixels. A **mean filter** replaces a pixel by the average of its neighbours, which reduces noise but also blurs edges. A **median filter** replaces it by the middle value of the sorted neighbours, which ignores one extreme value.

**Example (Fig. 6.11).** On a scan line with a spike of 200 among values of 10, the 3-point mean gives 73.3 on three pixels, while the median gives 10. At a step from 10 to 60 the mean produces the blurred values 26.7 and 43.3, but the median keeps 10 and 60, so the edge stays sharp. A dropout of 0 among 60s becomes 40.0 under the mean and 60 under the median.

**Thresholding.** A pixel above a threshold T becomes object, the others background. Otsu's method tries every level and keeps the one that separates the two groups best. In Fig. 6.10, for 2,000 pixels, it chooses T = 124; the groups overlap, so 110 pixels (5.5 percent) are still on the wrong side.

**Use.** Filter first, then threshold, because noise would otherwise create false regions.

**Q8. Discuss applications and challenges of machine vision, and say how a convolutional network helps. (10 marks)**

**Introduction.** Machine vision turns pixels into decisions. Cameras, scanners and satellites supply the images (Plates 6.3 and 6.4), and software finds edges, regions and objects.

**Applications.** (1) *Factory inspection* finds cracks and missing parts at line speed. (2) *Character recognition* reads documents and number plates. (3) *Biometrics* match fingerprints and faces. (4) *Medical imaging* marks suspicious regions on X-rays and retina photographs (Plate 6.5). (5) *Traffic monitoring* counts and classifies vehicles. (6) *Agriculture* detects leaf disease from phone photos. (7) *Satellite mapping* finds floods, snow and landslides, such as the Langtang avalanche of 2015. (8) *Robots and vehicles* navigate by seeing.

**Challenges.** Changes of light, viewpoint and scale; objects hidden by others; many object classes; recovering 3-D shape from a flat image; the need for large labelled sets; adversarial images with tiny changes that fool a classifier; and privacy and bias, because face systems can be less accurate for some groups.

**Convolutional networks (Fig. 6.12).** A convolutional network learns its own filters. In the figure a 28 × 28 image goes through a 3 × 3 convolution with 8 filters (26 × 26 × 8, 80 parameters), pooling (13 × 13 × 8), a second convolution with 16 filters (11 × 11 × 16, 1,168 parameters), pooling (5 × 5 × 16 = 400) and a dense layer of 10 outputs (4,010 parameters): 5,258 parameters in all. A dense network 784-128-10 needs 101,770, which is 19.4 times more, because a filter reuses the same 9 weights at every position.

| Method | Features | Strength | Weakness |
|---|---|---|---|
| Classical (edges, thresholds) | designed by hand | fast, needs little data | fails when conditions change |
| Convolutional network | learned from data | robust, accurate | needs many labelled images |

**Conclusion.** Vision succeeds when images are controlled and tested, and humans must stay in charge of high-stakes decisions.

**Q9. A vision system inspects 1,000 bottles, of which 50 are cracked. It finds 45 and raises 13 false alarms. Evaluate it. (5 marks)**

**Confusion matrix (Fig. 6.13).** True positives TP = 45 (cracked and flagged). False negatives FN = 50 − 45 = 5 (cracked and missed). False positives FP = 13 (good but flagged). True negatives TN = 1000 − 45 − 5 − 13 = 937.

**Measures.**

- **Precision** = TP / (TP + FP) = 45 / 58 = **0.7759**: of the bottles flagged, 77.6 percent are really cracked.
- **Recall** = TP / (TP + FN) = 45 / 50 = **0.90**: the system finds 90 percent of the cracked bottles.
- **F1** = 2PR / (P + R) = **0.8333**, a single score that balances the two.
- **Accuracy** = (45 + 937) / 1000 = **0.982**.

**Why accuracy alone misleads.** A system that never flags a bottle has accuracy 950 / 1000 = 0.950 but recall 0, because it finds no cracked bottle. When defects are rare, report precision and recall.

**Judgement.** The system is good: it catches 9 of 10 defects, and 13 false alarms per 1,000 bottles cost only a second look. If a cracked bottle is dangerous, the threshold should be changed to raise recall even if more false alarms appear.
