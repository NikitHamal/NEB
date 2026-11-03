# BCA polish status (5 Quality Pillars)
Legend: [ ] pending, [~] in progress, [x] done. Toolchain: AGENTS.md "BCA polish session 10".

## BCA 101 computer-fundamentals (semester-1/computer-fundamentals) -- [x] DONE, 100 pp, qa fails=0
Real units (NOT the brief's guess): U1 Intro, U2 Software, U3 OS, U4 DBMS, U5 Networks, U6 Internet/Web, U7 Contemporary Tech.
- [x] U1: SVG 1.1-1.6; Plates 1.1 (5-up generations), 1.2 (ENIAC/IBM 1401/punch card), 1.3 (labelled micro-ATX board + CPU), 1.4 (2x2 SRAM/DRAM/NVMe/pen drive with callouts), 1.5 (3-up HDD platter/arm/DVD with numbered key).
- [x] U2 Software: SVG 2.1 classification, 2.2 compile/link/load vs interpret, 2.3 flowchart; 3 medium + 2 long model answers (Q3, Q7, Q5; Q13, Q14).
- [x] U3 OS: SVG 3.1-3.2, Plate 3.1 (CLI vs GUI 4-up). Existing long answers OK.
- [x] U4 DBMS: SVG 4.1 file vs DBMS, 4.2 three-schema, 4.3 college ER; 8-point DBMS applications (4.1.1); 3 medium (Q2, Q12, Q4) + 2 long (Q13, Q14). No photo (not applicable). Do NOT run fill_script_outputs.py on this book.
- [x] U5 Networks: SVG 5.1-5.2, Plate 5.1 (cables 4-up), Plate 5.2 (devices 3-up).
- [x] U6 Internet: SVG 6.1 DNS, 6.2 HTTPS cycle; Q9 (5 marks), Q12, Q13, Q14 long. TODO optional: GIS/IoT photos, 7-8 point application lists.
- [x] U7 Contemporary Tech: SVG 7.1 IaaS/PaaS/SaaS, 7.2 digital signature, 7.3 e-governance models; Plate 7.1 (VR, Raspberry Pi, PIR, 3D print); Q10 (5 marks), Q14, Q15, Q16 long.
- Session 11: U1 memory/storage plates done; BCA 101 closed.

## BCA 103 digital-logic (semester-1/digital-logic) -- [x] DONE (session 11), 45 pp, qa fails=0
- U1: SVG 1.2 voltage bands, 1.3 clock waveform; Plate 1.1 (scope photo + sampling/quantisation SVG pair), Plate 1.2 (7447 ceramic DIP + HC00 die photo + 7400 pinout SVG, 3-up); 8-point advantages (1.5); 2 medium + 1 long answers.
- U2: SVG 2.1 conversion, 2.2 two's complement ring, 2.3 IEEE-754 layout; Plate 2.1 (7-segment LED photo + segment/BCD SVG); 8 reasons (2.6); 2 medium + 1 long.
- U3: SVG 3.1 gate symbols, 3.2 K-map with groups, 3.3 full adder; Plate 3.1 (breadboard + HP logic analyzer photos); 8 applications (3.7); 2 medium + 1 long.
- U4: SVG 4.1 ripple counter + timing, 4.2 shift register; 8 uses (4.4); 1 medium + 1 long.
- U5: SVG 5.1 101-detector state diagram; 1 medium + 1 long (design).
- Photos (bca103/): scope, ic7447, hc00, breadboard, seg7, logican (all licence-gated via assets.py).
- Not done: Unit 5 has no photo (abstract topic); units 2-5 only have the new model answers listed above (old short Practice answers kept).

## BCA 102 programming-in-c (semester-1/programming-in-c) -- [x] DONE (session 12), 78 pp, qa fails=0
- U1: Plate 1.1 (3-up: Thompson+Ritchie 1973, PDP-11/20, UNIX V5 screenshot; bca102/ photos), SVG 1.1 build pipeline; 8 features of C (1.5.1); 1 medium + 1 long answer.
- U2: SVG 2.1 type sizes to scale, SVG 2.2 operator precedence; 8 common mistakes (2.7); medium (data types) + long (operators, evaluated expression).
- U3: SVG 3.1 flowcharts if-else/while/do-while; 8 uses of loops/decisions (3.5); medium (if ladder vs switch + program) + long (loops).
- U4: SVG 4.1 array/string/2-D memory layout, SVG 4.2 bubble sort passes; 8 uses of arrays/strings (4.5); medium (bubble sort, program run) + long (strings, program run).
- U5: SVG 5.1 call stack of factorial(3), SVG 5.2 storage classes; 8 advantages of functions (5.5); medium (value vs address, run) + long (recursion + storage classes, run).
- U6: SVG 6.1 pointer/array arithmetic, SVG 6.2 malloc/realloc/free; 8 uses of pointers (6.6); medium (dynamic allocation) + long (pointers, program run).
- U7: Plate 7.1 (4-up punched card / HDD head / NVMe / pen drive, bca101 photos reused), SVG 7.1 struct vs union, SVG 7.2 file life cycle; 8 uses (7.5); medium (struct vs union) + long (file handling, binary file program run).
- All C programs in the new answers were compiled with gcc -Wall and the printed output pasted from the real run.

## BCA 106 hardware-workshop (semester-1/hardware-workshop) -- [x] DONE (session 12), 40 pp, qa fails=0
- Photos (bca106/, all licence-gated): strap, meter, crimpkit, psu, gpu, jpanel, paste, postcard, tester, toner, gparted (+ bca101 mobo/cpu-i7/ram/nvme/rj45/ubuntu/win10b reused).
- U1: Plate 1.1 (3-up tools with callouts), Plate 1.2 (3-up PSU/GPU/motherboard), SVG 1.1 PC block diagram; 8 safety rules (1.6); medium (safety/ESD) + long (components, compatibility, PSU calc).
- U2: Plate 2.1 (4-up CPU/DIMM/M.2/cooler), Plate 2.2 (front-panel header photo + SVG pin pairs), SVG 2.1 assembly order, SVG 2.2 no-boot decision tree; 8 assembly mistakes (2.5); medium (CPU/cooler/RAM) + long (assembly + POST).
- U3: Plate 3.1 (GParted + Ubuntu + Windows desktops), SVG 3.1 boot sequence, SVG 3.2 MBR vs GPT layout; 8 install tips (3.6); medium (MBR vs GPT, 2 TiB calc) + long (BIOS/UEFI, dual boot).
- U4: Plate 4.1 (4-up POST card/tester/patch cables/toner), SVG 4.1 T568B colours, SVG 4.2 troubleshooting cycle; 8 maintenance tasks (4.6); medium (straight cable) + long (troubleshooting method + fault table).

## BCA 104 mathematics-1 (semester-1/mathematics-1) -- [x] DONE (session 13), 56 pp, qa fails=0
- New helper: `Axes` class in `notes/pipeline/svgkit.py` (grid/axes/curve/area/bars/pt/hline/vline/tag) for plotted graphs inside ```svgfig / `@ svg` cells. Photos (bca104/, all licence-gated): dish, arch, newton, leibniz, cauchy, weier, speedo, taylor, riemann, archimedes, kgdam, coffee, ecoli, spring (+ bca103/scope reused).
- U1 Functions: Fig 1.1 gallery of 6 standard graphs, Plate 1.1 (3-up dish/arch/oscilloscope), Fig 1.2 inverse (e^x, ln x, y=x), Fig 1.3 transformations; 8 uses (1.6); 2 medium + 1 long.
- U2 Limits: Fig 2.1 hole/jump/infinite, Plate 2.1 (Cauchy, Weierstrass + eps-delta SVG), Fig 2.2 squeeze, Fig 2.3 IVT; 8 uses (2.5); 2 medium + 1 long.
- U3 Differentiation: Fig 3.1 secant to tangent + table, Plate 3.1 (speedometer, Newton, Leibniz), Fig 3.2 f and f', Fig 3.3 implicit circle; 8 uses (3.7); 2 medium + 1 long.
- U4 Applications: Fig 4.1 ladder, Fig 4.2 can optimisation, Fig 4.3 MVT, Plate 4.1 (Taylor portrait + Maclaurin sin x + e^0.1 error); 8 uses (4.8); 2 medium + 1 long.
- U5 Integration: Plate 5.1 (Archimedes, Riemann, Kaligandaki dam), Fig 5.1 Riemann sums, Fig 5.2 area between curves + disc volume, Fig 5.3 improper integrals; 8 uses (5.8); 2 medium + 1 long.
- U6 Differential equations: Fig 6.1 slope field, Fig 6.2 method decision chain, Fig 6.3 damping cases, Fig 6.4 cooling + logistic, Plate 6.1 (coffee, E. coli, spring); 8 uses (6.8); 2 medium + 1 long.
- Every numeric claim in the new answers was recomputed with SymPy; `check_math1.py --verify` prints ALL OK.

## BCA 105 professional-communication-ethics (semester-1/professional-communication-ethics) -- [x] DONE (session 13), 48 pp, qa fails=0
- Photos (bca105/, licence-gated): phone (candlestick telephone), speaker (conference talk), pen (handwritten letter), scrum (team stand-up briefing). Abstract topics (ethics, IP law) have no suitable photo; SVG used instead. Rejected after viewing: Morse key texture, GPO search hit, CC icon graphic with black alpha artefacts.
- U1: Fig 1.1 communication process (noise + feedback), Plate 1.1 (3-up telephone/speaker/letter channels); 8 reasons (1.7); medium (verbal vs non-verbal) + long (process, barriers, 7 Cs).
- U2: Fig 2.1 10-minute talk timeline to scale, Plate 2.1 (speaker photo + poor/good slide SVG); 8 habits (2.6); medium (active listening) + long (presentation).
- U3: Fig 3.1 annotated email anatomy, Plate 3.1 (letter photo + full-block layout SVG); 8 rules (3.8); medium (plagiarism) + long (email vs letter).
- U4: Plate 4.1 (team stand-up photo + Tuckman curve SVG), Fig 4.1 Eisenhower matrix; 8 team characteristics (4.7); medium (Tuckman) + long (teamwork, conflict, SBI, time).
- U5: Fig 5.1 ethical decision flow, Fig 5.2 IP types and licence spectrum; 8 responsibilities (5.8); medium (MIT vs GPL) + long (ethics, IP, ETA 2063; no penalty figures given).

## BCA 256 project-1 (semester-4/project-1) -- [x] DONE (session 14), qa fails=0
Project I has no TU topic list, so this is a reconstructed companion handbook (README says so) built around one running example, CampusShelf (invented college library book-issue system). 5 units, 16,401 raw words (gen_status count, code listings included), 49 pp.
- Photos (bca256/, licence-gated, all viewed): pitch (hackathon pitch), kanban (3-column board), scrum (task board), pair (pair programming), poster (poster-session presenter).
- U1 Scoping: Plate 1.1 (pitch photo + idea-funnel SVG), Fig 1.2 life cycle; feasibility score script (executed); 8 reasons projects fail (1.7); 2 medium + 1 long answers.
- U2 Planning: Fig 2.1 Gantt to scale (matches critical-path script), Plate 2.1 (3-up kanban/scrum/pair photos with callouts), Fig 2.2 Git branches; critical-path script + real `git` run output; 8 team practices (2.6); 2 medium + 1 long.
- U3 Analysis/design: Fig 3.1 use case, 3.2 DFD level 0, 3.3 DFD level 1, 3.4 ER; sqlite schema script (FK rejection shown); Plate 3.1 (3 wireframe SVGs); 8 benefits (3.6); 2 medium + 1 long.
- U4 Build/test: Fig 4.1 three layers, 4.2 V-model, 4.3 bug life cycle; full `campusshelf.py` listing run by fill_script_outputs; `unittest` file (fence tag `py`, NOT `python`, so fill_script_outputs does not wipe its hand-pasted output; regenerate with /tmp/cs recipe in AGENTS.md); 8 reasons (4.7); 2 medium + 1 long.
- U5 Report/viva: Fig 5.1 report map, Plate 5.1 (poster photo + clean-slide SVG), report-budget script, 12 viva Q&A, illustrative rubric (flagged as not official); 8 habits (5.8); 2 medium + 1 long.
- Known cosmetic: the Level-1 DFD labels render at about 6 pt (qa warn only).

## BCA 306 project-2 (semester-5/project-2) -- [x] DONE (session 15), 47 pp, qa fails=0
Companion handbook (README says the structure is reconstructed; no TU topic list). Running example **ClinicQ** (invented health-post token queue; REST API + security + deployment), different from Project I's CampusShelf. 5 units, 15,586 raw words.
- Photos (bca306/, licence-gated, all viewed): rack (NERSC server rack, CC0), switch (rack switch + patch panels), tech (technician at server rack, CC0), padlock, code (code on monitor, CC0).
- U1 Scope/architecture: Fig 1.1 three-tier, Plate 1.1 (3-up rack/switch/technician with callouts); stack table, REST table, user stories; 8 reasons web projects fail (1.7); 2 medium + 1 long.
- U2 API/database: Fig 2.1 ER, Fig 2.2 request life; 78-line stdlib REST API (http.server + sqlite3) run over a real local port; race-condition script (barrier forces duplicates; UNIQUE + retry fixes; output deterministic); 8 reasons (2.6); 2 medium + 1 long.
- U3 Security: Fig 3.1 login flow, Plate 3.1 (padlock photo + defence-in-depth SVG); executed PBKDF2 salt demo, HMAC token (issue/verify/expiry/forgery), SQL injection bad vs placeholder, brute-force arithmetic; attack table; 8 practices (3.7); 2 medium + 1 long.
- U4 Testing/deploy: Plate 4.1 (code photo + test pyramid SVG), Fig 4.1 pipeline; 9-test unittest suite (per-test PASS lines, deterministic), 10-row test-case table, Little's-law capacity script, systemd + Nginx files (not executed); 8 practices (4.6); 2 medium + 1 long.
- U5 Docs/demo/viva: Fig 5.1 report map, Plate 5.1 (technician photo + demo timeline SVG); generated API-doc script, demo-plan script; 12 viva Q&A; 8 habits (5.5); 2 medium + 1 long.
- Gotchas: `Fig.arrow` takes a list of points (`f.arrow([(x1,y1),(x2,y2)], color=)`), not four numbers; literal `<role>` in prose is stripped as HTML (use square brackets); the Unit 2 API deliberately has no login (Unit 3 adds it conceptually; routes table in 5.2 shows the protected version).
- Not done: Unit 2 has no photo; Unit 3 login/hash code is not wired into the Unit 2 server (separate self-contained demos).

## BCA 356 project-3 (semester-6/project-3) -- [x] DONE (session 16)
Companion handbook (README says the structure is reconstructed; no TU topic list). Running example **KhetSense** (invented soil-moisture and weather monitor for a hill-farm cooperative; ESP32 nodes, MQTT-style messages, SQLite analysis, Android offline-first client), different from CampusShelf (Project I) and ClinicQ (Project II). 5 units.
- Photos (bca356/, licence-gated, all viewed): esp32, rpi, uno, soil, dht22, drip, terrace, phone.
- U1 Scope/architecture: Fig 1.1 four-layer IoT, Plate 1.1 (3-up ESP32/Pi/Uno), Plate 1.2 (3-up soil probe/DHT22/drip); BOM script (v1 Rs 34,900 over budget, v2 Rs 26,700); 8 reasons sensor projects fail (1.6); 2 medium + 1 long.
- U2 Sensors/data path: Plate 2.1 (ESP32 photo + wiring SVG), Fig 2.1 calibration plot (Axes); calibration, median filter, QoS0 vs QoS1 loss simulation and battery scripts all executed; 8 rules (2.6); 2 medium + 1 long.
- U3 Storage/analysis: Fig 3.1 pipeline, Plate 3.1 (terrace photo + advice bands SVG); SQLite constraints script, MAD cleaning, anomaly rules, drying-curve forecast vs persistence (executed); 8 uses (3.7); 2 medium + 1 long.
- U4 Mobile client: Plate 4.1 (phone photo + 2 wireframe SVGs), Fig 4.1 sync sequence; offline-first sync simulation, stale-label tests (executed); 8 features (4.7); 2 medium + 1 long.
- U5 Field test/report/viva: Fig 5.1 report map, Plate 5.1 (Pi photo + demo timeline SVG); field-test PASS/FAIL table script (O1 honestly FAILS), report page budget; 12 viva Q&A, illustrative rubric, 8 habits (5.7); 2 medium + 1 long.
- Gotchas: python fences need a closing ``` (an unclosed fence swallows the unit); no `fill_script_outputs` problems since every block is self-contained; numbers in prose were copied from real runs (seeded, so re-runs match). Calibration figure is drawn with ideal positions (caption says so). No unit-5 real field photo exists (no real deployment).

## BCA 404 project-4 (semester-7/project-4) -- [x] DONE (session 17), 64 pp, qa fails=0
Companion handbook (README says the structure is reconstructed; no TU topic list). Running example **SikshyaSignal** (invented early-warning tool ranking 600 simulated first-year students by risk of failing; NumPy logistic regression written from scratch, seed 404). Different from CampusShelf (P1), ClinicQ (P2), KhetSense (P3). 5 units, 24,169 raw words.
- Photos (bca404/, licence-gated, all viewed): students (Sankhu school building, CC BY-SA), gpu (Radeon card), datacenter (CERN hall). Reused: bca306/code, bca306/tech, bca256/poster.
- U1 Framing/ethics: Fig 1.1 pipeline, Plate 1.1 (3-up school/GPU/datacentre), Fig 1.2 accuracy trap bars, Fig 1.3 should-we-use-ML chart; dataset + baseline script; 8 reasons (1.6); 2 medium + 1 long.
- U2 Data: Fig 2.1 histogram, 2.2 split, 2.3 leakage timeline, Plate 2.1 (code photo + cleaning flow SVG); cleaning, features/correlation/split, leakage-AUC scripts; 8 habits (2.6); 2 medium + 1 long.
- U3 Modelling: Fig 3.1 logistic regression, 3.2 learning curve (Axes), 3.3 confusion matrix, 3.4 precision-recall trade-off; training log, threshold sweep + test report, 5-fold CV + group fairness + bootstrap; 8 ways models mislead (3.5); 2 medium + 1 long. No photo (abstract topic).
- U4 Deployment: Fig 4.1 request life, 4.2 PSI + AUC bars, Plate 4.1 (technician photo + deployment-levels SVG); model.json + predict service, 8 PASS-line tests, PSI drift on 3 batches (covariate vs concept drift); privacy table, Dockerfile (fence tag `text`, not run); 8 habits (4.6); 2 medium + 1 long.
- U5 Defence: Fig 5.1 report map, 5.2 talk timeline, Plate 5.1 (poster photo + results-slide SVG); report page budget, 15-minute plan, shingle-similarity, rubric scripts; 12 viva Q&A; 8 habits (5.7); 2 medium + 1 long.
- Gotchas: `Axes.tag(x, y, s)` takes DATA coordinates (not ax.X/ax.Y pixels); `Axes.axes(xl, yl)` writes labels inside the plot corners and collides with tick labels, so pass empty strings and draw labels with `f.text` outside; every python block repeats a 12-line data generator (blocks must be self-contained for fill_script_outputs); text near-empty p3 warning is only the TOC overflow (warn, not fail).

## Queue
- [x] BCA 103 digital-logic DONE ( need DIP 74xx / breadboard photos via notes/pipeline/assets.py search)
- [x] programming-in-c DONE (session 12)
- [x] hardware-workshop DONE (session 12)
- [x] mathematics-1 (BCA 104) DONE (session 13)
- [x] professional-communication-ethics (BCA 105) DONE (session 13)
- [x] BCA 256 Project I DONE (session 14)
- [x] BCA 306 Project II DONE (session 15)
- [x] BCA 356 Project III DONE (session 16)
- [x] BCA 404 Project IV DONE (session 17)
- [ ] (NEXT SESSION STARTS HERE) BCA 452 Internship (semester-8/internship; books.json code BCA 452, 3 credits; handbook: placement search, workplace conduct, daily log, report, presentation; use a fifth running example)
- [ ] remaining non-core slots (BCA 356, 404 projects, 402 SPM if not a core book, 452 internship, 4 electives), then polish semesters II-VIII one book at a time
