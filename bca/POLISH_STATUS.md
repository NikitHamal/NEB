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

## BCA 452 internship (semester-8/internship) -- [x] DONE (session 18), 49 pp, qa fails=0
Companion handbook (README says the structure is reconstructed; no TU topic list). Running example **InternTrail**: invented 8-week placement of Anisha Gurung at the invented Lalitpur agency Himal Digital; different from CampusShelf, ClinicQ, KhetSense, SikshyaSignal. 5 units, 17,628 raw words.
- Photos (bca452/, licence-gated, all viewed): berlin (open-plan office), cowork (lounge), handshake, interview (career-fair table), lanyard (ID badge). Rejected after viewing: NIH "Interns" (black-and-white lab). Reused: bca256/kanban, bca256/pair, bca256/poster, bca306/code, bca306/tech, bca105/speaker, bca105/pen.
- U1 Placement search: Fig 1.1 12-week search timeline, Fig 1.2 CV anatomy, Plate 1.1 (3-up office/interview/handshake); weighted shortlist script (Himal 4.25, sensitivity 4.10); 8 reasons (1.6); 2 medium + 1 long.
- U2 Conduct: Fig 2.1 four information levels, Fig 2.2 15-minute rule, Plate 2.1 (lounge + badge photos + channel-guide SVG); secrets-scanner script (4 findings, masked); 8 habits (2.5); 2 medium + 1 long.
- U3 Weeks: Fig 3.1 hours-per-week stacked bars (from script output), Fig 3.2 8-week plan chart, Plate 3.1 (kanban + pair photos + log-card SVG); simulated 40-day log analysis (276.5 h, 33 of 40 days >= 6 h so L3 honestly fails); 8 rules (3.5); 2 medium + 1 long.
- U4 Technical: Fig 4.1 ticket life cycle, Plate 4.1 (code + technician photos + review-request SVG); HD-31 VAT rounding bug reproduced (float 0.565 -> 55.25 vs Decimal 55.26, 2 of 4 invoices) and a 6-test suite (6 passed); 8 practices (4.7); 2 medium + 1 long.
- U5 Report/viva: Fig 5.1 report map, Fig 5.2 skills before/after bars, Plate 5.1 (speaker + letter + poster photos); report page budget script (40 pp, ch 4+5 = 40%), skills self-assessment script (2.25 -> 4.00); 12 viva Q&A; 8 habits (5.7); 2 medium + 1 long.
- Gotchas: square `@ svg` cells inside photogrid need font size >= 12.5 on a 300 px canvas (scale ~0.53) or text drops below 6 pt; always close python fences; heredoc with quoted EOF keeps `\"` literally (run `sed -i 's/\\"/"/g'` on the file); `fill_script_outputs.py` can leave a duplicate trailing fence, check fence count is even.

## BCA 154 mathematics-2 (semester-2/mathematics-2) -- [x] POLISHED (session 18), 34 pp (was 23), qa fails=0
Math-heavy, so SVG figures and worked answers rather than photographs (no suitable real photo; none claimed).
- U1: Fig 1.1 determinant as area (det 5 vs singular det 0); 1.5 eight uses of matrices; Q1 (5 marks) adjoint inverse of a 3x3, Q2 (10 marks) matrix operations, determinant properties.
- U2: Fig 2.1 three line pictures (unique / none / infinite) via Axes; 2.7 eight uses of linear systems; Q1 Gaussian elimination (1,2,3), Q2 rank test + Cramer.
- U3: Fig 3.1 four subspaces; 3.7 eight uses; Q1 rank/nullity/bases of a 3x3, Q2 independence, basis, dimension, linear maps, kernel/image.
- U4: Fig 4.1 circle to ellipse with eigen-axes; 4.5 eight uses; Q1 eigen-decomposition of [[2,1],[1,2]] and A^5, Q2 diagonalisation + Markov steady state (5/6, 1/6).
- U5: Fig 5.1 plane, normal, distance; 5.6 eight uses; Q1 line through two points, Q2 plane through three points, distance 5/7, triangle area 3.5.
- Every number in the new answers was recomputed with SymPy; `check_math2.py` still prints ALL OK. Not done: no photographs; units 1 to 5 keep their original short Practice answers.

## BCA 151 discrete-structure (semester-2/discrete-structure) -- [x] POLISHED (sessions 18-19): all 6 units; 49 pp, qa fails=0
Math-heavy: SVG figures and worked answers, no photographs (none claimed).
- U1: Fig 1.1 proof-technique decision chain; 1.7 eight uses of logic; Q1 contrapositive truth table, Q2 proof techniques with examples.
- U2: Fig 2.1 injective / surjective / bijective mapping diagrams; 2.6 eight uses; Q1 equivalence relation mod 3, Q2 function types, composition, inverse, 2^n subsets.
- U3: Fig 3.1 Pascal's triangle; 3.9 eight uses; Q1 KATHMANDU arrangements (181,440; A's together 40,320), Q2 counting toolkit (74, 67, D4 = 9).
- U4: Fig 4.1 merge-sort recursion tree; 4.6 eight uses; Q1 induction (sum of odd numbers), Q2 recurrence a(n)=2*3^n-2^n verified numerically, Hanoi 1,023, merge sort.
- U5 (session 19): Fig 5.1 weighted graph with MST (thick teal) and Dijkstra distances (red); 5.7 eight uses; Q1 Kruskal MST (13), Q2 Dijkstra table + BFS/MST comparison.
- U6 (session 19): Fig 6.1 clock arithmetic mod 12 + toy RSA message path; 6.7 eight uses; Q1 extended Euclid (gcd 21 = 5*105 - 2*252), Q2 RSA + group/ring/field. `check_discrete.py` ALL OK.

## BCA 153 oop-in-java (semester-2/oop-in-java) -- [x] POLISHED (session 19), 66 pp (was 41), qa fails=0
- Photos (bca153/, licence-gated, all viewed): gosling (James Gosling portrait), simchip (smart-card chip die, Java Card context), socdie (SoC die, threads/cores), dcrack (data-centre aisle, JDBC servers).
- U1: Plate 1.1 (Gosling + SIM-chip die), Fig 1.1 write-once-run-anywhere pipeline, Fig 1.2 four pillars on an Account class diagram; 1.7 eight features; Q1 JDK/JRE/JVM, Q2 pillars + BankDemo run.
- U2: Fig 2.1 stack vs heap references; 2.8 eight benefits; Q1 pass-by-value (PassDemo run), Q2 Student class with equals/hashCode in HashSet (StudentDemo run).
- U3: Fig 3.1 payroll interface/abstract/subclass design; 3.7 eight uses; Q1 abstract class vs interface (PayDemo run), Q2 overloading/overriding/dispatch (DispatchDemo run).
- U4: Fig 4.1 Throwable family, Fig 4.2 string pool; 4.5 eight benefits; Q1 exceptions (ExcDemo run), Q2 String/StringBuilder (StringDemo run).
- U5: Fig 5.1 collections map, Fig 5.2 stream pipeline; 5.7 eight uses; Q1 List/Set/Map (CollDemo run), Q2 lambdas/streams/generics (StreamDemo run).
- U6: Plate 6.1 (SoC die + data-centre aisle), Fig 6.1 thread states, Fig 6.2 JDBC architecture; 6.6 eight uses; Q1 threads/race/executor (RaceDemo run), Q2 JDBC on H2 in-memory (JdbcDemo run).
- All new Java programs compiled and run with JDK 17 (`fill_java_outputs.py`); needs `sudo apt-get install openjdk-17-jdk-headless libh2-java libslf4j-java libservlet-api-java`. After fill, run `/tmp/fixblank.py`-style pass: add a blank line after every closing ```output fence when text follows directly (otherwise tables/paragraphs may merge into the code placeholder).
- Not done: old short Practice answers kept; no photograph for abstract units 2-5 (none claimed).

## System Analysis and Design (semester-3/system-analysis-and-design) -- [x] POLISHED (session 19), 51 pp (was 33), qa fails=0
Had ZERO figures before. Photos are reuses of already-licensed assets (no new downloads): bca256 kanban/scrum/pair, bca452 interview, bca101 atm-nepal/android, bca306 rack, bca404 datacenter.
- U1: Fig 1.1 SDLC waterfall with cost multipliers, Plate 1.1 (3-up agile practice photos); 1.11 eight reasons; Q1 SDLC phases, Q2 model comparison + recommendation.
- U2: Fig 2.1 cumulative discounted net benefit (payback 2.35 yr), Fig 2.2 Gantt to scale; 2.7 eight reasons; Q1 six feasibility types, Q2 library NPV/ROI/payback/BCR (all recomputed in Python: NPV 125,229; BCR 1.30; IRR 30.7%; discounted payback 2.64 yr).
- U3: Plate 3.1 (interview photo + techniques SVG), Fig 3.1 context diagram, 3.2 level-0 DFD, 3.3 ER with LOAN associative entity; 3.5 eight benefits; Q1 DFD symbols/rules, Q2 library models.
- U4: Fig 4.1 normalisation 1NF-3NF, Plate 4.1 (ATM + smartphone UI), Fig 4.2 annotated admission form; 4.6 eight rules; Q1 normalise ORDER_FORM, Q2 form/report/interface guidelines.
- U5: Fig 5.1 V-model testing, 5.2 installation strategies timeline, 5.3 maintenance 2x2, Plate 5.1 (rack + data-centre photos); 5.4 eight reasons; Q1 test levels, Q2 installation + maintenance types.
- Not done: old short Practice answers kept; no checks script exists for this book (numbers verified ad hoc).

## BCA 205 probability-and-statistics (semester-3/probability-and-statistics) -- [x] POLISHED (session 20), 57 pp (was 35), qa fails=0 warns=1 (p3 near-empty, pre-existing)
- Photos (bca205/, licence-gated, all viewed): hollerith (CHM replica, CC0), pearson (public domain), galton (Galton board, CC BY-SA), gosset (1908 portrait, PD), guinness (Gosset plaque, CC BY-SA). Fisher snapshot rejected (family photo, no value).
- U1: Fig 1.1 data-type tree, Plate 1.1 (Hollerith photo + 5-step study pipeline SVG); 8 reasons (1.6); 2 medium + 1 long.
- U2: Fig 2.1 grouped histogram with mean/median/mode, Fig 2.2 skewness trio, Fig 2.3 box plot; 8 uses (2.4); 2 medium (grouped averages, CV compare) + 1 long (six dispersion measures, computed).
- U3: Fig 3.1 three scatter plots (r = +0.98, -0.19, -0.96), Plate 3.1 (Pearson portrait + least-squares residual SVG), Fig 3.2 two regression lines; 8 uses (3.4); 2 medium (r + regression; Spearman) + 1 long.
- U4: Fig 4.1 Bayes natural-frequency tree, Plate 4.1 (Galton board photo + 68-95-99.7 SVG), Fig 4.2 binomial and Poisson bars, Fig 4.3 normal areas; 8 uses (4.6); 2 medium (Bayes, normal) + 1 long (binomial vs Poisson, approximation compared).
- U5: Fig 5.1 survey life cycle with error entry points, Fig 5.2 sample size vs margin, Fig 5.3 bias-vs-scatter targets (no photo: no suitable free Nepal survey photo found); 8 rules (5.6); 2 medium + 1 long.
- U6: Fig 6.1 four sampling designs on a 10x10 grid, Plate 6.1 (Gosset portrait + Guinness plaque + t vs z SVG, 3-up), Fig 6.2 CLT, Fig 6.3 chi-square tail; 8 designs/tools (6.10); 2 medium (SRSWOR, Neyman) + 1 long (t-test with CI, z compared).
- U7: Fig 7.1 variation split (strip plot + stacked SS bar), Fig 7.2 F(2,12) tail, Fig 7.3 randomised block layout, Fig 7.4 two-way SS partition (no photo: abstract topic); 8 uses (7.7); 2 medium + 1 long (two-way ANOVA).
- All new numbers recomputed with numpy/scipy before writing; `check_stats.py --assert` still passes. No fill_script_outputs run needed (no code blocks).

## BCA 206 applied-economics (semester-3/applied-economics) -- [x] POLISHED (session 21), 66 pp (was 34), qa fails=0 warns=1 (p3 near-empty, pre-existing)
Had ZERO figures before (graphs "described in words"). 27 figures/plates, 10 photos (bca206/, licence-gated, all viewed): smith, marshall, keynes (portraits), asan (vegetable seller), spice (Asan spice lane), kalimati (wholesale market street), ntc (Nepal Telecom head office), note (old NRB banknote), nrb (Thapathali), dryport (Birgunj customs). Rejected after viewing: Kulekhani (lake shot, no dam).
- U1: Fig 1.1 PPF with U/X points and growth shift, Fig 1.2 equilibrium + ceiling | demand shift + tax, Plate 1.1 (3-up Smith/Marshall/Asan); 8 applications (1.7); 2 medium + 1 long (equilibrium, CS 1,156, DWL 15).
- U2: Fig 2.1 five elasticity cases, Fig 2.2 linear demand elasticity zones + revenue curve, Plate 2.1 (spice photo + bumper-harvest SVG); 8 uses (2.6); 2 medium + 1 long.
- U3: Fig 3.1 TU/MU, Fig 3.2 equi-marginal bars, Fig 3.3 IC + budget + Hicks A->C->B; 8 uses (3.5); 2 medium + 1 long. No photo (abstract).
- U4: Fig 4.1 total and unit cost curves from the schedule, Fig 4.2 LAC envelope, Fig 4.3 revenue curves (3 panels); 8 uses (4.6); 2 medium + 1 long. No photo (abstract).
- U5: Plate 5.1 (3-up Kalimati/spice/NTC), Fig 5.1 price-taker cases, 5.2 monopoly + DWL 800, 5.3 price discrimination, 5.4 kinked demand + prisoner's-dilemma pay-offs; 8 lessons (5.8); 3 medium + 1 long.
- U6: Fig 6.1 four-sector circular flow, 6.2 Keynesian cross + multiplier chain, 6.3 GDP->DI waterfall, Plate 6.1 (Keynes/Kalimati/Asan); 8 uses (6.6); 2 medium + 1 long.
- U7: Plate 7.1 (note/NRB/dry port), Fig 7.1 deposit creation, 7.2 AD-AS demand-pull and cost-push, 7.3 policy transmission chain, 7.4 BoP waterfall; 8 roles (7.6); 2 medium + 2 long.
- All new numbers recomputed with Python (check_economics.py still passes). No fill_script_outputs needed (no code blocks).

## BCA 354 technical-writing (semester-6/technical-writing) -- [x] POLISHED (session 22), 59 pp (was 36), qa fails=0 warns=1 (p3 near-empty, pre-existing)
- Photos (bca354/, licence-gated, all viewed): typewriter (Olympia Simplex 1935), manual (car owner's manual), warning (tsunami hazard sign), library (Graz reading room). Reused: bca306 code/rack, bca105 scrum/pen, bca452 handshake/interview.
- U1: Plate 1.1 (3-up typewriter/manual/sign), Fig 1.1 inverted pyramid, Fig 1.2 writing-process loop; 1.8.1 eight habits; Q1, Q2 (5 marks), Q3 (10 marks).
- U2: Fig 2.1 FK/Fog bars from the executed program numbers, Fig 2.2 sentence surgery; 2.5.1 eight benefits of plain language; Q1, Q2 (FRE 64.71, FK 7.96 computed), Q3.
- U3: Plate 3.1 (code/rack/briefing), Fig 3.1 Diataxis 2x2, Fig 3.2 requirement anatomy + postmortem timeline; 3.7.1 eight reasons to document; Q1-Q3.
- U4: Plate 4.1 (library photo + IMRaD hourglass SVG), Fig 4.1 APA vs IEEE anatomy; 4.6.1 eight habits; Q1-Q3.
- U5: Fig 5.1 lie factor 20 vs 1, Fig 5.2 chart chooser, Fig 5.3 WCAG contrast swatches; 5.7.1 eight rules; Q1-Q3.
- U6: Plate 6.1 (letter/handshake/career fair), Fig 6.1 four editing levels, Fig 6.2 concision 44 to 22 words; 6.6.1 eight habits; Q1-Q3 (e-mail specimen).
- No code was added or changed, so fill_script_outputs.py was NOT run; existing executed outputs untouched.

## BCA 403 financial-accounting (semester-7/financial-accounting) -- [x] POLISHED (session 22), 65 pp (was 37), qa fails=0 warns=1 (p3 near-empty, pre-existing)
- Photos (bca403/, licence-gated, all viewed): ledger2 (1855 merchant ledger page), ledger (bound account book), register (antique cash register, Darjeeling), cheque (1909 cheque), note (old Nepal Rastra Bank 5-rupee note), warehouse (racked cartons). Reused bca306/code.
- Section numbering: new "seeing the ideas" section is inserted BEFORE the old "Summary and exercises", which is renumbered (+1). Helper `/tmp/ins3.py` (recreate: regex on `## U.K Summary and exercises`, `@S@` placeholder for U.K).
- U1: Plate 1.1 (ledger/register/cheque), Fig 1.1 equation in 3 transactions, Fig 1.2 accounting cycle; 1.7.1 eight uses of accounting information; Q1-Q3 (Q3 10 marks).
- U2: Plate 2.1 (note photo + tax-invoice SVG), Fig 2.1 Dr/Cr rules, Fig 2.2 Cash T-account (4,92,000); 2.8.1 eight controls; Q1-Q3 with trial balance 7,31,000.
- U3: Plate 3.1 (account book + three-column cash book SVG), Fig 3.1 subsidiary books, Fig 3.2 transposition hunt (900); 3.7.1 eight habits; Q1-Q3 (suspense).
- U4: Plate 4.1 (cheque + anatomy SVG), Fig 4.1 reconciliation bridge (49,050), Fig 4.2 sorting differences; 4.7.1 eight benefits; Q1-Q3.
- U5: Plate 5.1 (warehouse + FIFO layers SVG), Fig 5.1 SLM vs WDV curves, Fig 5.2 disposal (gain 24,000); 5.7.1 eight reasons; Q1-Q3 (FIFO 14,900 vs WAC 15,555.56).
- U6: Fig 6.1 profit waterfall, Fig 6.2 balance sheet to scale (7,69,000), Fig 6.3 adjustments double effect (no photo: abstract); 6.8.1 eight checks; Q1-Q3.
- U7: Plate 7.1 (code photo + ledger-tables SVG), Fig 7.1 ratio dashboard, Fig 7.2 DuPont tree; 7.9.1 eight uses; Q1-Q3.
- All figures use numbers already produced by the book's executed programs (no code changed, fill_script_outputs.py NOT run). Gotcha: a heading directly above a figure can be stranded at a page bottom (qa FAIL): add one sentence under the heading.

## BCA 451 cloud-computing (semester-8/cloud-computing) -- [x] POLISHED (session 23), 65 pp (was 37), qa fails=0 warns=0
- Photos (bca451/, licence-gated, all viewed): facebook (data-centre aisle), xeon (Broadwell-EP die), meter (kWh meter), containers (Chittagong port), tape (tape library), hsm (nCipher HSM), queue (station ticket queue). Reused: bca101 hdd-platter/nvme/fibre-cable/router, bca306 padlock/switch, bca403 register.
- U1: Plate 1.1 (3-up aisle/Xeon die/meter), Fig 1.1 NIST 5-4-3, 1.2 who-manages-what grid, 1.3 elasticity vs fixed fleet (430 vs 1,200 server-hours); 1.8.1 eight benefits; Q1-Q3.
- U2: Plate 2.1 (container yard + image-layer SVG), Fig 2.1 type-1/type-2/containers stacks, 2.2 nested paging; 2.8.1 eight benefits; Q1-Q3.
- U3: Plate 3.1 (tape/HDD/NVMe), Fig 3.1 replication vs RS(4,2), 3.2 hash ring, 3.3 quorum; 3.5.1 eight features; Q1-Q3.
- U4: Plate 4.1 (fibre/switch/router), Fig 4.1 VPC two-AZ, 4.2 VXLAN packet to scale, 4.3 CDN + LB path; 4.7.1 eight benefits; Q1-Q3.
- U5: Plate 5.1 (queue photo + M/M/1 curve SVG), Fig 5.1 Kubernetes architecture, 5.2 HPA 4->8->5, 5.3 monolith vs microservices; 5.6.1 eight benefits; Q1-Q4 (M/M/1 lambda 90, mu 100 recomputed).
- U6: Plate 6.1 (padlock + HSM), Fig 6.1 shared responsibility, 6.2 IAM evaluation, 6.3 envelope encryption (600 MB vs 10 TB); 6.6.1 eight practices; Q1-Q4.
- U7: Plate 7.1 (meter/register/aisle), Fig 7.1 pricing index, 7.2 break-even 5,256 h, 7.3 series vs parallel availability, 7.4 nines (log bars); 7.7.1 eight FinOps practices; Q1-Q4.
- No code was changed, so fill_script_outputs.py was NOT run. Helper `/tmp/ins2.py` inserts figures before "K Summary and exercises" (renumbers it) and appends answers.

## BCA 252 numerical-methods (semester-4/numerical-methods) -- [x] POLISHED (session 23), 66 pp (was 43), qa fails=0 warns=1 (p3 near-empty, pre-existing)
- Photos (bca204/, licence-gated, all viewed): gauss (Jensen 1840), lagrange (LoC portrait), euler (Handmann), runge (Weierstrass album), planimeter (K&E polar planimeter). Reused: bca104 newton, coffee.
- New sections are numbered after the last numbered section (e.g. 1.10, 2.8, 3.5) and inserted before the unnumbered "Formula and fact sheet"; helper `/tmp/ins3.py`.
- U1: Plate 1.1 (Newton portrait + tangent-steps SVG), Fig 1.1 bisection, Fig 1.2 convergence speeds (iteration counts from a real run: bisection 19, false position 13, fixed point 6, secant 6, Newton 2); 1.10.1 eight reasons; Q1 bisection x^3-5x+1, Q2 Newton cos x - x, Q3 method comparison (10 marks).
- U2: Plate 2.1 (Lagrange/Newton/Gauss), Fig 2.1 ln x cubic, 2.2 divided-difference table, 2.3 Runge phenomenon, 2.4 least-squares line; 2.8.1 eight uses; Q1 (ln 3 = 1.12344), Q2 (y = 0.05 + 1.99x), Q3.
- U3: Plate 3.1 (planimeter + trapezoid SVG), Fig 3.1 Simpson, 3.2 Romberg table, 3.3 derivative errors; 3.5.1 eight uses; Q1 trapezoid 1.89612 vs Simpson 2.00456, Q2 forward vs central, Q3 Romberg.
- U4: Plate 4.1 (Gauss + conditioning SVG), Fig 4.1 elimination, 4.2 Jacobi vs Gauss-Seidel; 4.7.1 eight uses; Q1-Q3 (all numbers from numpy runs).
- U5: Plate 5.1 (Euler/Runge/Euler-step SVG), Fig 5.1 Euler vs exact, 5.2 RK4 slopes, 5.3 error bars; 5.9.1 eight uses; Q1 Euler table, Q2 RK4 step, Q3 comparison (Euler 1.72102, Heun 1.794894, RK4 1.797441 vs exact 1.797443).
- U6: Plate 6.1 (coffee photo + stencil SVG), Fig 6.1 solved plate (42.857, 52.679, ...), 6.2 Gauss-Seidel progress; 6.6.1 eight uses; Q1-Q3 (symmetry solution verified).
- All numbers recomputed in Python before writing. check_numerical.py was not needed (no code changed); fill_script_outputs.py not run.

## BCA 401 cyber-security-and-ethical-hacking (semester-7/cyber-security-and-ethical-hacking) -- [x] POLISHED (session 24), 73 pp (was 48), qa fails=0 warns=1 (p31 = short unit-3 tail, natural unit end)
- Photos (bca401/, 13 new, licence-gated, all viewed): yubikey, fingerprint, enigma, writeblocker, pix, metrocard, ap, cctv, tpm, serverroom, imager, switch, singha (13 files; 25 SVG figures in total, not 27). Reused across units where a physical device repeats (pix, ap, serverroom, cctv).
- New sections are numbered after the last numbered section (1.7, 2.7, 3.6, 4.7, 5.7, 6.6, 7.6); Summary renumbered by /tmp/ins.py. Each has "x.y.1 Eight ..." (8 points, 3-4 sentences, Nepali examples).
- U1: Plate 1.1 (server room / Enigma-K / CCTV), Fig 1.1 CIA triad, 1.2 STRIDE on a DFD, 1.3 5x5 risk matrix; 8 secure-design principles; Q1 CIA, Q2 STRIDE, Q3 (10) risk ranking + CVSS 9.8 arithmetic (ISS 0.9148, impact 5.873, exploitability 3.887).
- U2: Plate 2.1 (PIX firewall + access point), Fig 2.1 TCP header to scale, 2.2 handshake ladder (2000/1000/2001/1001), 2.3 flag byte (0x12, 0x03); 8 uses of protocol analysis; Q1 handshake, Q2 flags, Q3 (10) service inventory + governance (ports 25, 5432 unapproved).
- U3: Plate 3.1 4-up (YubiKey, fingerprint, RFID card, TPM chip), Fig 3.1 factor families + strength ladder, 3.2 entropy bars (37.6/47.6/51.7/77.5/78.7), 3.3 DAC/MAC/RBAC/ABAC; 8 authentication practices; Q1 MFA, Q2 entropy (26^8 = 208,827,064,576; 7776^6), Q3 (10) access control models.
- U4: no photo (software unit, none claimed). Fig 4.1 secure SDLC, 4.2 concatenation vs parameterised query (no payloads), 4.3 cookie flags, 4.4 validate-encode pipeline; 8 secure coding practices; Q1 injection, Q2 cookies and CSRF, Q3 (10) secure SDLC + OWASP Top 10.
- U5: Plate 5.1 (switches/patch panels, PIX, AP), Fig 5.1 zones/DMZ, 5.2 DNSSEC chain, 5.3 WPA2 key hierarchy, 5.4 token bucket (run accepted 59 of 1000, bound 60); 8 network defence practices; Q1 DNSSEC, Q2 token bucket, Q3 (10) defended network + first-match ACL table.
- U6: Plate 6.1 (write blocker + disk imager), Fig 6.1 sensor placement, 6.2 confusion matrix (99/1/999/98,901, precision 9.02%), 6.3 NIST IR cycle, 6.4 hash-chained custody log; 8 IR/forensics practices; Q1 base-rate, Q2 IR lifecycle, Q3 (10) forensics.
- U7: Plate 7.1 (Singha Durbar, server room, CCTV), Fig 7.1 audit cycle, 7.2 ALE/ROSI (50,000 -> 10,000, ROSI 100%), 7.3 pen-test ROE gate (7 of 9 fields), 7.4 ETA 2063 penalties; 8 audit benefits; Q1 audit vs VA vs pentest vs red team, Q2 ALE/ROSI, Q3 (10) ROE, ethics and Nepal law.
- check_cybersec.py --verify: 39 tokens, 0 missing. No code was changed. Figure-fit gotchas: svgfig text does not wrap; keep a line under about 17 chars per 90 px box; do not put long labels in 90-px boxes; poly labels need a diamond about 100 px wide.

## BCA 3xx society-and-technology (semester-5/society-and-technology) -- [x] POLISHED (sessions 24-25): all 7 units, 74 pp (was 44), qa fails=0 warns=4 (p3 pre-existing; p38, p44, p55 are short tail pages of the still-unpolished units 4, 5, 7)
- Photos (bca-st/ new: gutenberg, nokia1100, intel4004; reused bca101: vacuum-tube, android, atm-nepal, fibre-cable, router). Sections end with unnumbered "Chapter summary" + "Practice", so new sections go before "## Chapter summary" (ins.py `sec ... "## Chapter summary" x` leaves the heading unchanged); the new section is numbered after the last numbered section (1.6, 2.6, 3.6).
- [x] U1: Plate 1.1 4-up (printing press, vacuum tube, Intel 4004, smartphone), Fig 1.1 timeline of information technologies, 1.2 Moore's law log chart (2^25 = 33,554,432; 77,175,193,600); 1.6.1 eight social impacts; Q1 Moore's law, Q2 determinism vs social shaping, Q3 (10) information revolutions and impacts.
- [x] U2: Plate 2.1 (feature phone, smartphone, ATM), Fig 2.1 TAM, 2.2 Rogers categories, 2.3 logistic S-curve (14.2%, 85.8%, 22.5 pts/yr), 2.4 Bass new adopters (peak year 7 = 56,968; t* = 6.02); 2.6.1 eight barriers; Q1 TAM, Q2 logistic calculation, Q3 (10) Bass model.
- [x] U3: Plate 3.1 4-up (fibre, router, feature phone, smartphone), Fig 3.1 three levels, 3.2 Lorenz curve (Gini 0.171, re-checked in Python 0.1707), 3.3 composite index bars; 3.6.1 eight ways to close the divide; Q1 three levels, Q2 gap/ratio (0.731, 56.8%, 2.93x), Q3 (10) min-max index for Madhesh = 0.181.
- [x] U4 Cyber and IT Law (session 25): Plate 4.1 3-up (Cyber Bureau signboard CC0, Supreme Court of Nepal, gavel), Fig 4.1 offence-to-court path, 4.2 ETA penalty ceilings to scale (16 yr / Rs 8,00,000), 4.3 CA trust chain, 4.4 first hour after fraud; 4.7.1 eight duties; Q1 recognition + CA, Q2 offences (11 yr / Rs 5,00,000 case), Q3 (10) framework.
- [x] U5 e-Governance (session 25): Plate 5.1 3-up (KMC office gate, ward office, ATM), Fig 5.1 G2C/G2B/G2G/G2E, 5.2 maturity ladder, 5.3 EGDI 0.520 bars, 5.4 benefit/cost (Rs 4.59 crore net, 11.2:1), 5.5 toy-RSA signature with the executed numbers; 5.5.1 eight benefits; Q1-Q3.
- [x] U6 Cyberethics and fairness (session 25): Plate 6.1 3-up (Buolamwini portrait, face-recognition gate, live-recognition van), Fig 6.1 six bias entry points, 6.2 confusion matrices, 6.3 rate bars (DI 0.533), 6.4 impossibility (FPR 0.148); 6.6.1 eight practices; Q1 bias sources, Q2 hiring screen recomputed (sel 0.5/0.2, TPR .667/.5, FPR .25/.071, DI 0.400), Q3 (10) bank loan model.
- [x] U7 E-waste and green computing (session 25): Plate 7.1 3-up (informal cable burning, shredded scrap, data-centre aisle bca451), Fig 7.1 life cycle, 7.2 waste hierarchy, 7.3 1,000 kg flow, 7.4 PUE 1.50 -> 1.30, 7.5 laptop footprint by service life; 7.6.1 eight practices; Q1-Q3 (Q2 PUE 1.60, 8,40,960 kWh, saving 1,83,960 kWh = Rs 22,07,520, recomputed).
- New bca-st photos (session 25, licence-gated, all viewed): cyberbureau, supremecourt, gavel, kmc, wardoffice, ewaste-burn, ewaste-sort, buolamwini, facegate, facevan. Society and Technology is now POLISHED: 74 pp (was 44), qa fails=0 warns=1 (p3 pre-existing). New numbered section in each unit is x.7 (U4), 5.5, 6.6, 7.6, inserted before Chapter summary by /tmp/ins2.py (recreate: insert A before "## Chapter summary", append B).

## BCA 351 computer-graphics (semester-6/computer-graphics) -- [x] POLISHED (sessions 25-26): all 7 units, 79 pp (was 44), qa fails=0 warns=1 (p3 pre-existing)
Had ZERO figures before. Photos (bca-cg/, licence-gated, all viewed): lcd (RGB sub-pixels), crt (colour CRT cutaway), phosphor (1984 green monitor), radeon (graphics card), sketchpad (Sutherland at TX-2), teapot (Utah teapot render), shading (flat vs Gouraud spheres, split into two cells with `crop`), phong (Phong sphere), horse (Muybridge The Horse in Motion, left half via `crop`).
- [x] U1: Plate 1.1 4-up (LCD, CRT, phosphor monitor, GPU card), Fig 1.1-1.3; 1.5.1 eight applications; Q1-Q3.
- [x] U2: Plate 2.1 (Sketchpad photo + Bresenham grid SVG), Fig 2.1-2.3; 2.7.1; Q1-Q3 (tables generated by Python).
- [x] U3 (abstract): Fig 3.1-3.4; 3.6.1; Q1-Q3. U4 (abstract): Fig 4.1-4.3; 4.5.1; Q1-Q3.
- [x] U5 (session 26): Plate 5.1 (Utah teapot photo + right-handed axes SVG), Fig 5.1 rotation about a vertical line (top view, P(4,1,3) -> (3,1,-2)), 5.2 similar triangles, 5.3 orthographic vs perspective cube to scale, 5.4 view frustum (60 deg, near 2, far 8), 5.5 viewing pipeline with the point (1,2,3) followed to pixel (457,286), 5.6 back-face detection; 5.5.1 eight applications; Q1 rotation about a line, Q2 perspective projection of a triangle (area 2 vs 0.167), Q3 back-face with viewer at (0,0,10) (N.V = 30 and -36), Q4 (10) parallel vs perspective + pipeline.
- [x] U6 (session 26): Plate 6.1 3-up (flat | Gouraud | Phong sphere with highlight call-out), Fig 6.1 Z-buffer trace computed in the figure code, 6.2 painter's algorithm + cyclic overlap, 6.3 Phong vectors + stacked intensity bars (0.8200, 0.6311, 0.5046), 6.4 specular fall-off curves, 6.5 Gouraud vs Phong along an edge (0.68 vs peak 1.30); 6.5.1 eight applications; Q1 Z-buffer 3x3 trace (11 tests), Q2 Phong intensity, Q3 flat/Gouraud/Phong, Q4 (10) hidden-surface methods, Q5 (10) illumination + shading.
- [x] U7 (session 26): Plate 7.1 (Muybridge horse photo + de Casteljau SVG), Fig 7.1 Bernstein weights + curve, 7.2 Bezier vs B-spline, 7.3 C0/G1/C1 joins, 7.4 linear vs smoothstep, 7.5 morphing triangles, 7.6 production stages + storage arithmetic; 7.6.1 eight applications; Q1 Bezier B(0.25) = (0.9063, 1.125) both ways, Q2 Bezier vs B-spline table, Q3 easing + morph (20..320 in 30 frames), Q4 (10) curves, Q5 (10) animation.
- Numbers recomputed in Python with numpy before writing. No code in this book: fill_script_outputs.py not needed. Helper `/tmp/ins2.py FILE A.md B.md` (insert A before "## Chapter summary", append B) - recreate if /tmp is wiped.

## BCA 352 mobile-programming (semester-6/mobile-programming) -- [x] POLISHED (session 27), 90 pp (was 44), qa fails=0 warns=1 (p3 pre-existing)
Had ZERO figures before. 11 new licence-gated `bca352/` photos fetched (all viewed in a contact sheet): tabboard (Galaxy Tab main board), amoled (Nexus One AMOLED pixels at 200x), droids (Android version statues), foldable, studio (Android Studio 3.1 screenshot), mpu6050, gps (NOAA constellation), microsd, mast (base-station mast), nfc (phone payment), lock (lock-screen notifications). Reused: bca101 nvme/pendrive/router/pir, bca401 tpm/fingerprint/yubikey, cs8/ict-nt-tower.
New section in each unit is x.7 (U1 1.7 ... U7 7.7, U3 is 3.6, U5 5.6, U6 6.6) inserted before "## Chapter summary" by /tmp/ins2.py; each has "x.y.1 Eight ..." (8 points of 3-4 sentences) and a "Model answers" block appended at the end of the unit.
- [x] U1: Plate 1.1 (board photo with 3 numbered marks + Android stack SVG), Plate 1.2 3-up (AMOLED / foldables / version statues), Fig 1.1 48 dp on six buckets in real px, 1.2 image memory bars (4,80,00,000 -> 7,50,000 B), 1.3 native/hybrid/web layers; 8 mobile constraints; Q1 native/hybrid/cross, Q2 1080x2340 @ 440 dpi (392.73 x 850.91 dp, 132 px, 64x), Q3 (10) Android architecture + sandbox vs iOS.
- [x] U2: Plate 2.1 (lock-screen photo + nested lifetimes SVG), Fig 2.1 state machine, 2.2 back stack in the 4 scenarios (3/6/6/7 callbacks), 2.3 intent resolution, 2.4 what survives what, 2.5 launch modes; 8 lifecycle rules; Q1 intents, Q2 callback sequence (15 total), Q3 (10) lifecycle + state saving, Q4 launch modes.
- [x] U3: Plate 3.1 (full-width Android Studio screenshot with 4 marks), Plate 3.2 3-up (foldables + phone/tablet pane SVGs; svg cells at font >= 13), Fig 3.1 view tree, 3.2 login screen to scale (379.43 dp = 996 px), 3.3 RecyclerView recycling (13 + 2 = 15, 667x), 3.4 DiffUtil LCS, 3.5 Compose data flow; 8 layout rules; Q1-Q2 (5), Q3 fragments (10), Q4 View vs Compose (10).
- [x] U4: Plate 4.1 3-up flash (microSD / NVMe / USB), Plate 4.2 (TPM photo + Keystore path SVG), Fig 4.1 storage areas, 4.2 GROUP BY results (1,450 / 8,000 / 320; 9,070 / 700), 4.3 index vs scan, 4.4 transaction rollback, 4.5 Room layers; 8 storage rules; Q1 choose storage, Q2 transaction, Q3 Room (10), Q4 EMI Rs 8,884.88 recomputed.
- [x] U5: Plate 5.1 3-up (mast / Nepal Telecom tower / router), Fig 5.1 request-response, 5.2 JSON tree (Rs 1,570), 5.3 UiState, 5.4 status classes and retry, 5.5 backoff bars (91 s), 5.6 main-thread frames (48 skipped), 5.7 WorkManager waits (930 s); 8 networking practices; Q1-Q3 (5), Q4 (10) background work, Q5 (10) WorkManager vs foreground service vs alarm.
- [x] U6: Plate 6.1 3-up (MPU-6050 / PIR / fingerprint), Plate 6.2 (GPS constellation + 3-circle trilateration SVG), Fig 6.1 permission flowchart, 6.2 accelerometer curve with threshold (20 steps from 500 samples), 6.3 haversine triangle (54.75 km N, 131.45 km W, 142.4 km), 6.4 accuracy ladder, 6.5 notification anatomy; 8 guidelines; Q1-Q3 (5), Q4 (10) sensors/location, Q5 (10) notifications.
- [x] U7: Plate 7.1 3-up (YubiKey / phone payment / version statues), Fig 7.1 four build approaches, 7.2 testing pyramid, 7.3 AAB split APKs (illustrative 17.8 vs 30 MB, labelled as example), 7.4 v2 signing chunks (1,048,576 + 1,048,576 + 402,848), 7.5 versionCode ordering, 7.6 release pipeline; 8 pre-publish checks; Q1-Q3 (5), Q4 (10) signing, Q5 (10) publishing.
- check_mobile.py --verify: 34 tokens, 0 missing. No executed code changed.
- svgfig gotchas this session: a 3-up photogrid `@ svg` cell needs font >= 13 on a 300 px canvas (qa flags 5 pt text); long arrow labels must fit the gap between boxes (about 9 px per char at size 10); right-hand text columns anchored at x >= 440 run off a 580 px canvas; `f.raw('<text transform="rotate(-90 ...)">')` gives clean vertical bracket labels; keep a circle's centre +/- radius inside the canvas (Fig(300, 300) for trilateration).

## BCA 203 web-technology-1 (semester-3/web-technology-1) -- [~] IN PROGRESS (session 28): units 1-4 polished
14 new licence-gated `bca203/` photos fetched and all viewed in a contact sheet: firstserver (NeXT), imp (ARPANET IMP), racks, tbl, mosaic, netscape, eich, crockford, hakon, inspector, bray, resig, braille, ishihara. Unused so far: tbl, bray, resig, braille, ishihara (reserved for U5-U7).
- [x] U1: Plate 1.1 3-up (IMP / NeXT first web server / rack aisle with numbered keys), Fig 1.1 page-load waterfall (220 ms), 1.2 URL anatomy, 1.3 DNS hierarchy, 1.4 HTTP request/response, 1.5 IPv4 /24 vs /26 binary (Python-checked); 1.7.1 eight applications in Nepal; Q1-Q2 (5), Q3 (10) HTTP.
- [x] U2: Plate 2.1 3-up (Mosaic / Netscape 3 / Firefox inspector screenshots), Fig 2.1 DOM tree, 2.2 semantic layout, 2.3 colspan/rowspan table, 2.4 form controls, 2.5 canvas coordinates; 2.8.1 eight HTML rules; Q1-Q2 (5), Q3 (10) forms.
- [x] U3: Plate 3.1 (Eich + Crockford + milestones SVG), Fig 3.1 event loop (A D C B, run in Node 22), 3.2 scope chain, 3.3 coercion table, 3.4 event flow, 3.5 array pipeline (56), 3.6 Nepali mobile regex; 3.9.1 eight uses; Q1-Q2 (5), Q3 (10) validation program. Node-verified outputs in `output` fences.
- [x] U4: Plate 4.1 (Hakon Wium Lie + CSS timeline), Fig 4.1 box model (310 x 210 / 260), 4.2 specificity, 4.3 justify-content arithmetic, 4.4 grid areas (200+180+180+2x20), 4.5 position, 4.6 breakpoints; 4.8.1 eight CSS rules; Q1-Q2 (5), Q3 (10) responsive layout.
- [ ] U5 XML, U6 jQuery, U7 Layout and design issues: pending (photos reserved: bray, resig, braille, ishihara, racks, tbl).
- QA gotcha: qa_pdf.py FAILS on any `$` or double backslash in non-monospace text (captions, svg text). Put regex with `$` in backticks (code span) and say "dollar anchor" in prose/figures.

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
- [x] BCA 452 Internship DONE (session 18)
- [x] BCA 154 Mathematics II polished (session 18, SVG + answers, no photos)
- [x] BCA 151 Discrete Structure units 5-6 (session 19)
- [x] BCA 153 OOP in Java (session 19, 66 pp)
- [x] BCA 153 OOP in Java and System Analysis and Design polished (session 19)
- [x] Probability and Statistics polished (session 20, 35 -> 57 pp)
- [x] Applied Economics polished (session 21, 34 -> 66 pp)
- [x] Technical Writing polished (session 22, 36 -> 59 pp)
- [x] Financial Accounting polished (session 22, 37 -> 65 pp)
- [x] Cloud Computing polished (session 23, 37 -> 65 pp)
- [x] Numerical Methods polished (session 23, 43 -> 66 pp)
- [x] Cyber Security and Ethical Hacking polished (session 24, 48 -> 73 pp)
- [x] Society and Technology units 4-7 finished (session 25, 44 -> 74 pp)
- [x] Computer Graphics and Animation units 5-7 finished (session 26, 60 -> 79 pp)
- [x] BCA 352 Mobile Programming polished (session 27, 44 -> 90 pp)
- [~] (NEXT SESSION STARTS HERE) finish Web Technology I units 5-7 (units 1-4 done, 69 pp so far); then polish remaining thin core books by page count: (was 45), MIS and e-Business (45), Cryptography and Network Security (45), then the rest of Semesters II-VIII; apply the 5 pillars (photos where physical, SVGs, 8-point sections, 5/10-mark answers)
- [ ] 3 remaining non-core slots: BCA 402 (SPM, if not core), Elective I/II (BCA 405/406), Elective III/IV (BCA 453/454); the elective subjects are not named in CURRICULUM.md, pick from the TU list there; then polish semesters II-VIII one book at a time
