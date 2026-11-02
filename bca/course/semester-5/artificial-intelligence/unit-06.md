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
